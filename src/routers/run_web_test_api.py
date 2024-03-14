import psutil
import sys

from allure_combine import combine_allure
from allure_pytest import plugin as allure_pytest_plugin
from calendar import monthrange
from copy import deepcopy
from datetime import datetime
from flask import Blueprint, request
from glob import glob
from json import load, dump
from multiprocessing import Process, Lock
from os import makedirs, replace
from os.path import join, isfile, exists
from pytest import main
from pytest_check import plugin as pytest_check_plugin
from re import sub, findall
from shutil import rmtree

from src.constants.enum_other import EnumKey, EnumScriptJson
from src.constants.enum_server import EnumServer, EnumFlask, EnumFlaskRoute, EnumPytest
from src.routers.edit_test_plan_api import all_script
from src.routers.socket_api import emit_reset, update_run_test_info
from src.side_to_tests import SideToTests
from src.functions.def_report import Report
from src.functions.def_requests import Requests
from src.functions.def_open import open_r, open_w
from src.variable import Variable as Var

run_tests = Blueprint(EnumFlask.RUN_TESTS.name_, __name__)
look = Lock()


def diff_datetime(start_datetime: datetime, end_datetime: datetime) -> str:
    if isinstance(start_datetime, datetime) and isinstance(end_datetime, datetime):
        if start_datetime > end_datetime:
            end_datetime, start_datetime = start_datetime, end_datetime
        diff_keys = ["year", "month", "day", "hour", "minute", "second"]
        max_value = {"year": 0, "month": 12, "day": monthrange, "hour": 23, "minute": 59, "second": 59}
        diff_result = {"year": 0, "month": 0, "day": 0, "hour": 0, "minute": 0, "second": 0}
        for idx, key in enumerate(diff_keys):
            diff = end_datetime.__getattribute__(key) - start_datetime.__getattribute__(key)
            if diff < 0:
                diff_result[diff_keys[idx - 1]] -= 1
                if isinstance(max_value[key], int):
                    diff = max_value[key] + diff
                elif max_value[key] == monthrange:
                    diff = monthrange(start_datetime.year, start_datetime.month)[1] + diff
            diff_result[key] = diff
        return ", ".join([f"{v} {k}" for k, v in diff_result.items()])
    return ""


@run_tests.get(EnumFlaskRoute.TEST_CASES.route)
def fetch_test_cases() -> list:
    if not len(Var.test_cases):
        result_all_script = []
        for script in all_script():
            if script[EnumScriptJson.CHECK.name_]:
                temp_script: dict = deepcopy(script)
                result_suites = []
                for suite in script[EnumScriptJson.SUITES.name_]:
                    if suite[EnumScriptJson.CHECK.name_]:
                        temp_suite = deepcopy(suite)
                        temp_suite[EnumScriptJson.TESTS.name_] = [
                            test for test in temp_suite[EnumScriptJson.TESTS.name_] if test[EnumScriptJson.CHECK.name_]
                        ]
                        if len(temp_suite[EnumScriptJson.TESTS.name_]):
                            result_suites.append(temp_suite)
                temp_script[EnumScriptJson.SUITES.name_] = result_suites
                if len(temp_script[EnumScriptJson.SUITES.name_]):
                    result_all_script.append(temp_script)
        return result_all_script
    return Var.test_cases


def check_test_cases(test_cases: list) -> bool:
    if len(test_cases):
        current: list = all_script()
        current_dict: dict = SideToTests.list_2_dict(current)
        test_cases_dict: dict = SideToTests.list_2_dict(test_cases)
        for test_case_key, test_case_value in test_cases_dict.items():
            if test_case_key not in current_dict:
                return False
            temp_current_suite = SideToTests.list_2_dict(current_dict[test_case_key][EnumScriptJson.SUITES.name_])
            for suite_key, suite_value in SideToTests.list_2_dict(test_case_value[EnumScriptJson.SUITES.name_]).items():
                if suite_key not in temp_current_suite:
                    return False
        return True
    return False


def update_progress(allure_result_folders_and_info: dict, update: bool = True) -> None | dict:
    process_generate_single_file(allure_result_folders_and_info)
    results_json_path: list = glob(join(allure_result_folders_and_info[EnumServer.ALLURE_FOR_SERVE.name_], "*-result.json"))
    tests_progress_result = {}
    for result_json_path in results_json_path:
        result_json = load(open_r(result_json_path))
        temp_result = tests_progress_result
        for *keys, last_key in [[sub(r"test_|Test", "", test_id) for test_id in findall(r"(?:test_|Test)\w+", result_json["fullName"])]]:
            for key in keys:
                temp_result = temp_result.setdefault(key, {})
        temp_result.setdefault(last_key, result_json[EnumKey.STATUS.name_].upper())
    result = {
        EnumKey.PROGRESS_RESULT.name_: tests_progress_result,
        EnumKey.PROGRESS.name_: len(results_json_path) / allure_result_folders_and_info[EnumServer.ALLURE_TOTAL__FILE.name_] * 100
    }
    if update:
        Requests.post_update_run_test_info(result)
    else:
        return result


def process_generate_single_file(allure_result_folders_and_info: dict) -> None:
    Process(target=generate_single_file, args=(allure_result_folders_and_info,)).start()


def generate_single_file(allure_result_folders_and_info: dict):
    Report.run_popen([
        r"allure",
        r"generate",
        rf"{allure_result_folders_and_info[EnumServer.ALLURE_FOR_SERVE.name_]}",
        r"-c",
        r"-o",
        rf"{allure_result_folders_and_info[EnumServer.ALLURE_FOR_OPEN.name_]}",
    ])
    combine_allure(
        allure_result_folders_and_info[EnumServer.ALLURE_FOR_OPEN.name_],
        allure_result_folders_and_info[EnumServer.ALLURE_OUTPUT.name_],
        True,
        True,
        True
    )
    complete_path: str = join(str(allure_result_folders_and_info[EnumServer.ALLURE_OUTPUT.name_]), EnumServer.COMPLETE_HTML_FILE.value)
    complete_text = open_r(complete_path).read()
    open_w(complete_path).write(sub(r"&lt;/?p&gt;", "", complete_text))
    replace(complete_path, allure_result_folders_and_info[EnumServer.ALLURE_SINGLE_HTML.name_])
    Requests.get_update_report_history()


def run_pytest(paths: list, allure_result_folders_and_info: dict):
    main(
        [
            rf"""--alluredir={allure_result_folders_and_info[EnumServer.ALLURE_FOR_SERVE.name_]}""",
            r"-s",
            r"-v",
            r"-W",
            r"ignore:Module already imported:pytest.PytestWarning",
            r"--color=no",
            rf"{EnumPytest.LOG_FILE_ABSPATH.value}={allure_result_folders_and_info[EnumServer.ALLURE_LOG.name_]}",
            rf"{EnumPytest.TEST_VIDEO_FOLDER_ABSPATH.value}={allure_result_folders_and_info[EnumServer.ALLURE_TEST_VIDEOS.name_]}",
        ] + paths,
        plugins=[allure_pytest_plugin, pytest_check_plugin] if getattr(sys, "frozen", False) else []
    )
    progress_result: dict = update_progress(allure_result_folders_and_info, False)
    clear_download_files_during_testing()
    Requests.post_update_run_test_info(
        {
            EnumKey.END_DATETIME.name_: Report.datetime_tz8_str(),
            EnumKey.STATUS.name_: 4
        } | progress_result
    )


def clear_download_files_during_testing() -> None:
    if not EnumServer.IS_WINDOWS.value:
        if exists(EnumServer.DOWNLOADS__FOLDER_PATH.value):
            rmtree(EnumServer.DOWNLOADS__FOLDER_PATH.value)


def start_task(test_cases) -> None:
    result_test_cases_path = [
        join(
            EnumServer.TESTS__FOLDER_PATH.value,
            f"test_{test_case[EnumScriptJson.FILE_ID.name_]}",
            f"""test_{test_case[EnumScriptJson.PROJECT_ID.name_]}.py::Test{suite[EnumScriptJson.SUITE_ID.name_]}::test_{test[EnumScriptJson.TEST_ID.name_]}""",
        ) for test_case in test_cases for suite in test_case[EnumScriptJson.SUITES.name_] for test in suite[EnumScriptJson.TESTS.name_]
    ]
    datetime_tz8: str = Report.datetime_tz8_str()
    Var.allure_result_folders_and_info = Report.create_allure_result_folders_and_info(datetime_tz8, len(result_test_cases_path))
    Var.task_main = Process(target=run_pytest, args=(result_test_cases_path, Var.allure_result_folders_and_info,), daemon=False)
    Var.task_main.start()
    update_run_test_info({
        EnumKey.START_DATETIME.name_: datetime_tz8,
        EnumKey.STATUS.name_: 2
    })


@run_tests.get(EnumFlaskRoute.TEST_STATUS.route)
def test_info() -> dict:
    return Var.run_test_info


@run_tests.post(EnumFlaskRoute.START_TEST_CASES.route)
def start_test_cases() -> (str, int):
    with look:
        if Var.run_test_info[EnumKey.STATUS.name_] == 1:
            datas = request.json
            if check_test_cases(datas[EnumKey.TEST_CASES.name_]):
                Var.control_pytest_running = True
                Var.test_cases = datas[EnumKey.TEST_CASES.name_]
                update_run_test_info({
                    EnumKey.TEST_VARIABLE.name_: datas[EnumKey.TEST_VARIABLE.name_]
                })
                dump(datas[EnumKey.TEST_VARIABLE.name_], open_w(EnumServer.URL_JSON__FILE_PATH.value))
                start_task(datas[EnumKey.TEST_CASES.name_])
                return ""
            return "Test cases is changed", 202
        return "Other users have started", 202


@run_tests.get(EnumFlaskRoute.STOP_TEST_CASES.route)
def stop_test_cases() -> (str, int):
    with look:
        if Var.run_test_info[EnumKey.STATUS.name_] == 2 and Var.control_pytest_running is True:
            Var.control_pytest_running = False
            update_run_test_info({
                EnumKey.STATUS.name_: 3
            })
            return ""
        return "Other users have stopped", 202


@run_tests.get(EnumFlaskRoute.TEST_RESET.route)
def reset() -> (str, int):
    if Var.run_test_info[EnumKey.STATUS.name_] == 4:
        Var.test_cases.clear()
        kill_task(Var.task_main)
        update_run_test_info({
            EnumKey.STATUS.name_: 1,
            EnumKey.PROGRESS.name_: 0,
            EnumKey.PROGRESS_RESULT.name_: {},
            EnumKey.START_DATETIME.name_: "",
            EnumKey.END_DATETIME.name_: "",
        })
        emit_reset()
        return ""
    return "Can't reset, test running.", 202


@run_tests.get(EnumFlaskRoute.SHOW_FOLDER_FILES.route)
def show_folder_files() -> list:
    return [file for file in glob(join(EnumServer.DOWNLOADS__FOLDER_PATH.value, "*")) if isfile(file)] if exists(EnumServer.DOWNLOADS__FOLDER_PATH.value) else []


@run_tests.post(EnumFlaskRoute.UPLOAD_FILES_FOR_TEST.route)
def upload_files_for_test() -> (str, int):
    if EnumServer.DOWNLOADS__FOLDER_PATH.value:
        if not exists(EnumServer.DOWNLOADS__FOLDER_PATH.value):
            makedirs(EnumServer.DOWNLOADS__FOLDER_PATH.value, exist_ok=True)
        for file in request.files.values():
            file.save(join(EnumServer.DOWNLOADS__FOLDER_PATH.value, file.filename))
        return "Upload Completed"
    return "Upload Folder Not Found", 202


def kill_task(task: Process):
    if task.is_alive():
        children = psutil.Process(pid=task.pid).children(True)
        task.terminate()
        for child in children:
            if psutil.pid_exists(child.pid):
                child.terminate()
