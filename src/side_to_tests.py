from base64 import b64encode
from copy import deepcopy
from glob import glob
from hashlib import sha1
from json import load, dump
from os import makedirs
from os.path import join, exists, basename, splitext
from re import search
from shutil import rmtree

from src.classifications.cmd_assert import CmdAssert
from src.classifications.cmd_browser import CmdBrowser
from src.classifications.cmd_conditional import CmdConditional
from src.classifications.cmd_input import CmdInput
from src.classifications.cmd_loop import CmdLoop
from src.classifications.cmd_mouse import CmdMouse
from src.classifications.cmd_popup_window import CmdPopupWindow
from src.classifications.cmd_script import CmdScript
from src.classifications.cmd_selection import CmdSelection
from src.classifications.cmd_store import CmdStore
from src.classifications.cmd_test_tools import CmdTestTools
from src.classifications.cmd_verify import CmdVerify
from src.classifications.cmd_wait import CmdWait
from src.config import Config
from src.constants.enum_command import EnumCommand
from src.constants.enum_server import EnumPytest, EnumServer
from src.constants.enum_other import EnumSideToTests, EnumScriptJson, EnumSide, EnumSideSuites, EnumSideTests, EnumSideTestsCommands
from src.functions.def_open import open_r, open_w
from src.functions.def_regex import Regex


class SideToTests(CmdAssert, CmdBrowser, CmdConditional, CmdInput, CmdLoop, CmdMouse, CmdPopupWindow, CmdScript, CmdSelection, CmdStore, CmdTestTools, CmdVerify, CmdWait):
    def __init__(self, renew_json=False):
        self.renew_json = renew_json
        self.side = None
        self.url = ""
        self.opens_window = False
        self.window_handle_name = ""
        self.window_timeout = 0
        self.default_space: int = 0
        self.command_path = None
        self.command_object = {
            # CmdAssert
            EnumCommand.ASSERT.value: self.command_object_handle(self._assert),
            EnumCommand.ASSERT_TITLE.value: self.command_object_handle(self._assert_title),
            EnumCommand.ASSERT_TEXT.value: self.command_object_handle(self._assert_text),
            EnumCommand.ASSERT_NOT_TEXT.value: self.command_object_handle(self._assert_not_text),
            EnumCommand.ASSERT_VALUE.value: self.command_object_handle(self._assert_value),
            EnumCommand.ASSERT_CHECKED.value: self.command_object_handle(self._assert_checked),
            EnumCommand.ASSERT_NOT_CHECKED.value: self.command_object_handle(self._assert_not_checked),
            EnumCommand.ASSERT_ELEMENT_PRESENT.value: self.command_object_handle(self._assert_element_present),
            EnumCommand.ASSERT_ELEMENT_NOT_PRESENT.value: self.command_object_handle(self._assert_element_not_present),
            EnumCommand.ASSERT_EDITABLE.value: self.command_object_handle(self._assert_editable),
            EnumCommand.ASSERT_NOT_EDITABLE.value: self.command_object_handle(self._assert_not_editable),
            EnumCommand.ASSERT_SELECTED_LABEL.value: self.command_object_handle(self._assert_selected_label),
            EnumCommand.ASSERT_SELECTED_VALUE.value: self.command_object_handle(self._assert_selected_value),
            EnumCommand.ASSERT_NOT_SELECTED_VALUE.value: self.command_object_handle(self._assert_not_selected_value),
            EnumCommand.ASSERT_ALERT.value: self.command_object_handle(self._assert_alert),
            EnumCommand.ASSERT_CONFIRMATION.value: self.command_object_handle(self._assert_confirmation),
            EnumCommand.ASSERT_PROMPT.value: self.command_object_handle(self._assert_prompt),
            # CmdBrowser
            EnumCommand.OPEN.value: self.command_object_handle(self._open),
            EnumCommand.CLOSE.value: self.command_object_handle(self._close),
            EnumCommand.SET_WINDOW_SIZE.value: self.command_object_handle(self._set_window_size),
            EnumCommand.STORE_WINDOW_HANDLE.value: self.command_object_handle(self._store_window_handle),
            EnumCommand.SELECT_WINDOW.value: self.command_object_handle(self._select_window),
            # CmdConditional
            EnumCommand.IF.value: self.command_object_handle(self._if, Config.add_space),
            EnumCommand.ELSE_IF.value: self.command_object_handle(self._else_if, 0, -Config.add_space),
            EnumCommand.ELSE.value: self.command_object_handle(self._else, 0, -Config.add_space),
            EnumCommand.END.value: self.command_object_handle(self._end, -Config.add_space, -Config.add_space),
            # CmdInput
            EnumCommand.TYPE.value: self.command_object_handle(self._type),
            EnumCommand.SEND_KEYS.value: self.command_object_handle(self._send_keys),
            EnumCommand.SUBMIT.value: self.command_object_handle(self._submit),
            EnumCommand.EDIT_CONTENT.value: self.command_object_handle(self._edit_content),
            # CmdLoop
            EnumCommand.WHILE.value: self.command_object_handle(self._while, Config.add_space),
            EnumCommand.TIMES.value: self.command_object_handle(self._times, Config.add_space),
            EnumCommand.FOR_EACH.value: self.command_object_handle(self._for_each, Config.add_space),
            EnumCommand.DO.value: self.command_object_handle(self._do, Config.add_space),
            EnumCommand.REPEAT_IF.value: self.command_object_handle(self._repeat_if, -Config.add_space),
            # Command.end_:  self.command_object_handle(self._end, -2),
            # CmdMouse
            EnumCommand.CLICK.value: self.command_object_handle(self._click),
            EnumCommand.CLICK_AT.value: self.command_object_handle(self._click_at),
            EnumCommand.DOUBLE_CLICK.value: self.command_object_handle(self._double_click),
            EnumCommand.DOUBLE_CLICK_AT.value: self.command_object_handle(self._double_click_at),
            EnumCommand.MOUSE_DOWN.value: self.command_object_handle(self._mouse_down),
            EnumCommand.MOUSE_DOWN_AT.value: self.command_object_handle(self._mouse_down_at),
            EnumCommand.MOUSE_MOVE_AT.value: self.command_object_handle(self._mouse_move_at),
            EnumCommand.MOUSE_UP.value: self.command_object_handle(self._mouse_up),
            EnumCommand.MOUSE_UP_AT.value: self.command_object_handle(self._mouse_up_at),
            EnumCommand.DRAG_AND_DROP_TO_OBJECT.value: self.command_object_handle(self._drag_and_drop_to_object),
            EnumCommand.MOUSE_OVER.value: self.command_object_handle(self._mouse_over),
            EnumCommand.MOUSE_OUT.value: self.command_object_handle(self._mouse_out),
            # CmdPopupWindow
            EnumCommand.ANSWER_ON_NEXT_PROMPT.value: self.command_object_handle(self._answer_on_next_prompt),
            EnumCommand.CHOOSE_CANCEL_ON_NEXT_PROMPT.value: self.command_object_handle(self._choose_cancel_on_next_prompt),
            EnumCommand.CHOOSE_OK_ON_NEXT_CONFIRMATION.value: self.command_object_handle(self._choose_ok_on_next_confirmation),
            EnumCommand.CHOOSE_CANCEL_ON_NEXT_CONFIRMATION.value: self.command_object_handle(self._choose_cancel_on_next_confirmation),
            EnumCommand.WEBDRIVER_ANSWER_ON_VISIBLE_PROMPT.value: self.command_object_handle(self._webdriver_answer_on_visible_prompt),
            EnumCommand.WEBDRIVER_CHOOSE_CANCEL_ON_VISIBLE_PROMPT.value: self.command_object_handle(self._webdriver_choose_cancel_on_visible_prompt),
            EnumCommand.WEBDRIVER_CHOOSE_OK_ON_VISIBLE_CONFIRMATION.value: self.command_object_handle(self._webdriver_choose_ok_on_visible_confirmation),
            EnumCommand.WEBDRIVER_CHOOSE_CANCEL_ON_VISIBLE_CONFIRMATION.value: self.command_object_handle(self._webdriver_choose_cancel_on_visible_confirmation),
            # CmdScript
            EnumCommand.RUN_SCRIPT.value: self.command_object_handle(self._run_script),
            EnumCommand.EXECUTE_SCRIPT.value: self.command_object_handle(self._execute_script),
            EnumCommand.EXECUTE_ASYNC_SCRIPT.value: self.command_object_handle(self._execute_async_script),
            # CmdSelection
            EnumCommand.SELECT.value: self.command_object_handle(self._select),
            EnumCommand.ADD_SELECTION.value: self.command_object_handle(self._add_selection),
            EnumCommand.REMOVE_SELECTION.value: self.command_object_handle(self._remove_selection),
            EnumCommand.SELECT_FRAME.value: self.command_object_handle(self._select_frame),
            EnumCommand.CHECK.value: self.command_object_handle(self._check),
            EnumCommand.UNCHECK.value: self.command_object_handle(self._uncheck),
            # CmdStore
            EnumCommand.STORE.value: self.command_object_handle(self._store),
            EnumCommand.STORE_TITLE.value: self.command_object_handle(self._store_title),
            EnumCommand.STORE_JSON.value: self.command_object_handle(self._store_json),
            EnumCommand.STORE_TEXT.value: self.command_object_handle(self._store_text),
            EnumCommand.STORE_VALUE.value: self.command_object_handle(self._store_value),
            EnumCommand.STORE_ATTRIBUTE.value: self.command_object_handle(self._store_attribute),
            EnumCommand.STORE_XPATH_COUNT.value: self.command_object_handle(self._store_xpath_count),
            # Command.storeWindowHandle_:  self.command_object_handle(self._store_window_handle),
            # CmdTestTools
            EnumCommand.ECHO.value: self.command_object_handle(self._echo),
            EnumCommand.PAUSE.value: self.command_object_handle(self._pause),
            EnumCommand.SET_SPEED.value: self.command_object_handle(self._set_speed),
            EnumCommand.DEBUGGER.value: self.command_object_handle(self._debugger),
            EnumCommand.RUN.value: self.command_object_handle(self._run),
            # CmdVerify
            EnumCommand.VERIFY.value: self.command_object_handle(self._verify),
            EnumCommand.VERIFY_TITLE.value: self.command_object_handle(self._verify_title),
            EnumCommand.VERIFY_TEXT.value: self.command_object_handle(self._verify_text),
            EnumCommand.VERIFY_NOT_TEXT.value: self.command_object_handle(self._verify_not_text),
            EnumCommand.VERIFY_VALUE.value: self.command_object_handle(self._verify_value),
            EnumCommand.VERIFY_CHECKED.value: self.command_object_handle(self._verify_checked),
            EnumCommand.VERIFY_NOT_CHECKED.value: self.command_object_handle(self._verify_not_checked),
            EnumCommand.VERIFY_ELEMENT_PRESENT.value: self.command_object_handle(self._verify_element_present),
            EnumCommand.VERIFY_ELEMENT_NOT_PRESENT.value: self.command_object_handle(self._verify_element_not_present),
            EnumCommand.VERIFY_EDITABLE.value: self.command_object_handle(self._verify_editable),
            EnumCommand.VERIFY_NOT_EDITABLE.value: self.command_object_handle(self._verify_not_editable),
            EnumCommand.VERIFY_SELECTED_LABEL.value: self.command_object_handle(self._verify_selected_label),
            EnumCommand.VERIFY_SELECTED_VALUE.value: self.command_object_handle(self._verify_selected_value),
            EnumCommand.VERIFY_NOT_SELECTED_VALUE.value: self.command_object_handle(self._verify_not_selected_value),
            # CmdWait
            EnumCommand.WAIT_FOR_TEXT.value: self.command_object_handle(self._wait_for_text),
            EnumCommand.WAIT_FOR_ELEMENT_PRESENT.value: self.command_object_handle(self._wait_for_element_present),
            EnumCommand.WAIT_FOR_ELEMENT_NOT_PRESENT.value: self.command_object_handle(self._wait_for_element_not_present),
            EnumCommand.WAIT_FOR_ELEMENT_VISIBLE.value: self.command_object_handle(self._wait_for_element_visible),
            EnumCommand.WAIT_FOR_ELEMENT_NOT_VISIBLE.value: self.command_object_handle(self._wait_for_element_not_visible),
            EnumCommand.WAIT_FOR_ELEMENT_EDITABLE.value: self.command_object_handle(self._wait_for_element_editable),
            EnumCommand.WAIT_FOR_ELEMENT_NOT_EDITABLE.value: self.command_object_handle(self._wait_for_element_not_editable),
        }

    @staticmethod
    def command_object_handle(function, after: int = None, before: int = None):
        value: dict = {
            EnumSideToTests.AFTER.name_: after if isinstance(after, int) else 0,
            EnumSideToTests.BEFORE.name_: before if isinstance(before, int) else 0,
        }
        return {EnumSideToTests.FUNCTION.name_: function, EnumSideToTests.VALUE.name_: value}

    def main(self, side_files: list = None):
        file_project_object = []
        if side_files is None:
            side_files = []
        for side_file_path in side_files:
            self.side = load(open_r(side_file_path))
            self.url = self.side[EnumSide.URL.name_]
            side_file_name = self.filename(side_file_path)
            side_file_id = self.sha1(side_file_name)
            side_name = self.side[EnumSide.NAME.name_]
            side_id = self.re_rm_underline(self.sha1(f"{side_file_id}{Regex.re_id(self.side[EnumSide.ID.name_])}"))
            suite_py: list = self.join(
                deepcopy(Config.default_test_main_import) +
                [f"""from {self.add_command_text(side_id)} import Command"""] +
                deepcopy(Config.default_test_self_import) +
                deepcopy(Config.default_test_log_import)
            )
            side_folder_path = join(EnumServer.TESTS__FOLDER_PATH.value, f"test_{side_file_id}")
            if exists(side_folder_path):
                rmtree(side_folder_path)
            side_path = join(side_folder_path, f"test_{side_id}.py")
            makedirs(side_folder_path, exist_ok=True)
            tests = {test[EnumSideTests.NAME.name_]: test[EnumSideTests.ID.name_] for test in self.side[EnumSide.TESTS.name_]}
            self.command_path = join(side_folder_path, f"{self.add_command_text(side_id)}.json")
            dump(tests, open_w(self.command_path))
            self.command_path = rf""".{search(rf"[{chr(92)}{chr(92)}/]tests[{chr(92)}{chr(92)}/].+?$", self.command_path).group()}"""
            self.build_command_py(side_folder_path, side_id)
            self.side[EnumSide.TESTS.name_] = {test[EnumSideTests.ID.name_]: test for test in self.side[EnumSide.TESTS.name_]}
            suites = []
            for suite in self.side[EnumSide.SUITES.name_]:
                suite_name = suite[EnumSideSuites.NAME.name_]
                suite_id = Regex.re_id(suite[EnumSideSuites.ID.name_])
                class_suite_id = suite_id.replace("_", "").upper()
                suites.append({
                    EnumScriptJson.SUITE_ID.name_: class_suite_id,
                    EnumScriptJson.SUITE_NAME.name_: suite_name,
                    EnumScriptJson.CHECK.name_: True,
                    EnumScriptJson.TESTS.name_: [{
                        EnumScriptJson.TEST_ID.name_: Regex.re_id(test_id),
                        EnumScriptJson.TEST_NAME.name_: self.side[EnumSide.TESTS.name_][test_id][EnumSideTests.NAME.name_],
                        EnumScriptJson.CHECK.name_: True,
                    } for test_id in suite[EnumSideSuites.TESTS.name_]]
                })
                suite_py_class = [
                    f"""{self.space}@allure.parent_suite(r\"{side_file_name}\")""",
                    f"""{self.space}@allure.epic(r\"{side_file_name}\")""",
                    f"""{self.space}@allure.suite(r\"{side_name}\")""",
                    f"""{self.space}@allure.feature(r\"{side_name}\")""",
                    f"""{self.space}@allure.sub_suite(r\"{suite_name.title()}\")""",
                    f"""{self.space}@allure.story(r\"{suite_name.title()}\")""",
                    f"""{self.space}class Test{class_suite_id}(Command, DefaultPytest):"""
                ]
                self.default_space += Config.add_space
                suite_py_class += [
                    f"""{self.space}# Test Suites ID: {suite_id}""",
                    f"""{self.space}# Test Suites Name: {suite_name}""",
                    f"""{self.space}def setup_class(self):""",

                ]
                self.default_space += Config.add_space
                suite_py_class += [
                    f"""{self.space}log.info(r\"\"\"# Test Suite Name：『{suite_name.strip()}』\"\"\")""",
                    f"""{self.space}super().setup_class(self)""",
                    f""""""
                ]
                self.default_space -= Config.add_space
                test_suite_folder_name = self.re_convert_file_and_folder_name(suite_name)
                for test_id in suite[EnumSideSuites.TESTS.name_]:
                    test = self.side[EnumSide.TESTS.name_][test_id]
                    test_id = Regex.re_id(test[EnumSideTests.ID.name_])
                    test_name = test[EnumSideTests.NAME.name_]
                    suite_py_def = [
                        f"""{self.space}@allure.title(r\"{test_name}\")""",
                        f"""{self.space}@allure.description(r\".{search(rf"[{chr(92)}{chr(92)}/]tests[{chr(92)}{chr(92)}/].+?$", side_path).group()} class=\\\"Test{class_suite_id}\\\" def=\\\"test_{test_id}\\\"\")""",
                        f"""{self.space}def test_{test_id}(self, {EnumPytest.TEST_VIDEO_FOLDER_ABSPATH.name_}):"""
                    ]
                    self.default_space += Config.add_space
                    comment_class = [
                        f"""{self.space}# Test name: {test_name}""",
                        f"""{self.space}# Step # | name | target | value | comment""",
                        f"""{self.space}self.create_video_folder({EnumPytest.TEST_VIDEO_FOLDER_ABSPATH.name_}, r\"{test_suite_folder_name}\", r\"{self.re_convert_file_and_folder_name(test_name)}\")""",
                        f"""{self.space}self.original = r\"\"\" {self.side[EnumSide.URL.name_]} \"\"\".strip()""",
                    ]
                    suite_py_def += deepcopy(comment_class)

                    suite_py_def += [f"""{self.space}self._{test_id}_()"""]
                    suite_py_class += suite_py_def + [""]
                    self.default_space -= Config.add_space
                self.default_space -= Config.add_space
                suite_py += self.join(suite_py_class)

            file_project_object.append({
                EnumScriptJson.FILE_ID.name_: side_file_id,
                EnumScriptJson.FILE_NAME.name_: side_file_name,
                EnumScriptJson.PROJECT_ID.name_: side_id,
                EnumScriptJson.PROJECT_NAME.name_: side_name,
                EnumScriptJson.SUITES.name_: suites,
                EnumScriptJson.CHECK.name_: True,
            })
            open_w(side_path).writelines(self.join(suite_py, 2))
        if len(file_project_object):
            if exists(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value):
                file_project_object = self.marge_json(load(open_r(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value)), file_project_object)
            dump(file_project_object, open_w(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value))

    def build_command_py(self, side_folder_path, side_id):
        command_py: list = self.join(deepcopy(Config.default_test_command_import) + deepcopy(Config.default_test_log_import))
        command_py_class = [f"""{self.space}class Command:"""]
        self.default_space += Config.add_space
        if not len(self.side[EnumSide.TESTS.name_]):
            command_py_class += self.add_pass
        for test in self.side[EnumSide.TESTS.name_]:
            test_id = Regex.re_id(test[EnumSideTests.ID.name_])
            test_name = test[EnumSideTests.NAME.name_]
            command_py_def = [f"""{self.space}@disable_assertions""", f"""{self.space}def _{test_id}_(self):"""]
            self.default_space += Config.add_space
            command_py_def += [
                f"""{self.space}# Test name: {test_name}""",
                f"""{self.space}log.info(r\"\"\"# Test Name：【{test_name.strip()}】\"\"\")""",
                f"""{self.space}# Step # | name | target | value | comment"""
            ]
            temp_command = False
            for idx, command in enumerate(test[EnumSideTests.COMMANDS.name_]):
                re_search = search(r"^//(.+)$", command[EnumSideTestsCommands.COMMAND.name_])
                comment_out = ""
                if re_search:
                    comment_out = "# "
                    command[EnumSideTestsCommands.COMMAND.name_] = re_search.groups()[0]
                if command[EnumSideTestsCommands.COMMAND.name_] in self.command_object:
                    self.opens_window = EnumSideTestsCommands.OPENS_WINDOW.name_ in command and command[EnumSideTestsCommands.OPENS_WINDOW.name_]
                    # self.opens_window = True if EnumCommands.OPENS_WINDOW.name_ in command and command[EnumCommands.OPENS_WINDOW.name_] is True else False
                    if self.opens_window:
                        self.window_handle_name = Regex.re_replace(command[EnumSideTestsCommands.WINDOW_HANDLE_NAME.name_])
                        self.window_timeout = Regex.re_replace(command[EnumSideTestsCommands.WINDOW_TIMEOUT.name_])
                    comment_def = f"""# 【{test_name.strip()}】{idx + 1} | {comment_out.replace("# ", "//")}{command[EnumSideTestsCommands.COMMAND.name_]} | {command[EnumSideTestsCommands.TARGET.name_]} | {command[EnumSideTestsCommands.VALUE.name_]} | {command[EnumSideTestsCommands.COMMENT.name_]}"""
                    before_command = [comment_def]
                    after_command = []
                    if command[EnumSideTestsCommands.COMMAND.name_] not in EnumCommand.TO_AFTER_COMMAND.value:
                        before_command.append(f"""self.run_before_step(r\"\"\" {comment_def} \"\"\")""")
                    if self.opens_window:
                        before_command += self._window_handles(None, None)
                        after_command += self._opens_window(self.window_handle_name, self.window_timeout)
                    if temp_command and command[EnumSideTestsCommands.COMMAND.name_] in EnumCommand.NEXT_COMMAND_TO_PASS.value:
                        command_py_def.append(f"""{self.space}pass """)
                    else:
                        temp_command = False
                    command_py_def += self.typesetting(
                        comment_out,
                        before_command,
                        after_command,
                        self.command_object[command[EnumSideTestsCommands.COMMAND.name_]][EnumSideToTests.FUNCTION.name_](Regex.re_replace(command[EnumSideTestsCommands.TARGET.name_]), Regex.re_replace(command[EnumSideTestsCommands.VALUE.name_])),
                        self.command_object[command[EnumSideTestsCommands.COMMAND.name_]][EnumSideToTests.VALUE.name_]
                    )
                    if command[EnumSideTestsCommands.COMMAND.name_] in EnumCommand.CONDITIONALS.value and not comment_out:
                        temp_command = True
            self.default_space -= Config.add_space
            command_py_class += command_py_def + [""]
        self.default_space -= Config.add_space
        command_py += self.join(command_py_class)
        open_w(join(side_folder_path, f"{self.add_command_text(side_id)}.py")).writelines(self.join(command_py, 2))

    def typesetting(self, comment_out: str, before_command: list, after_command: list, contents: list, change: dict):
        result: list = []
        for content in before_command + contents:
            result.append(f"""{" " * (self.default_space + change[EnumSideToTests.BEFORE.name_])}{comment_out}{content}""" if isinstance(content, str) else content)
        if not comment_out:
            self.default_space += change[EnumSideToTests.AFTER.name_]
        for content in after_command:
            result.append(f"""{" " * self.default_space}{comment_out}{content}""" if isinstance(content, str) else content)
        return result

    @property
    def space(self) -> str:
        return " " * self.default_space

    @property
    def add_pass(self) -> list:
        return [f"""{self.space}pass """]

    @staticmethod
    def join(value: list, count=1) -> list:
        return [(count * "\n").join(value)]

    @staticmethod
    def sha1(value):
        return Regex.re_id(b64encode(sha1(value.encode()).digest()).decode("ascii").replace("=", ""))

    @staticmethod
    def filename(value: str):
        filename, _ = splitext(basename(value.strip()))
        return filename

    @staticmethod
    def add_command_text(value):
        return f"""command_{value}"""

    @staticmethod
    def list_2_dict(datas: list) -> dict:
        return {
            _[EnumScriptJson.SUITE_ID.name_] if EnumScriptJson.SUITE_ID.name_ in _
            else _[EnumScriptJson.TEST_ID.name_] if EnumScriptJson.TEST_ID.name_ in _
            else f"{_[EnumScriptJson.FILE_ID.name_]}{_[EnumScriptJson.PROJECT_ID.name_]}": _ for _ in datas
        }

    def marge_json(self, old_list: list, new_list: list, append_old: bool = True):
        old_dict = self.list_2_dict(old_list)
        new_dict = self.list_2_dict(new_list)
        result = []
        for old_key, old_value in old_dict.items():
            temp_new_value = new_dict.get(old_key)
            if temp_new_value is not None:
                need_recursive_key = EnumScriptJson.SUITES.name_ if EnumScriptJson.SUITES.name_ in old_value else EnumScriptJson.TESTS.name_ if EnumScriptJson.TESTS.name_ in old_value else None
                if need_recursive_key is not None:
                    temp_new_value[need_recursive_key] = self.marge_json(old_value[need_recursive_key], temp_new_value[need_recursive_key], False)
                temp_new_value[EnumScriptJson.CHECK.name_] = old_value[EnumScriptJson.CHECK.name_]
                result.append(temp_new_value)
            elif not self.renew_json and append_old:
                result.append(old_value)
        for new_key, new_value in new_dict.items():
            if old_dict.get(new_key) is None:
                result.append(new_value)
        return result


def main() -> None:
    for command in EnumCommand:
        if isinstance(command.value, str):
            assert command.name_ == command.value, f"""name({command.name_}) != value({command.value})"""

    if exists(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value):
        side_to_tests = SideToTests(True)
        side_to_tests.main(glob(join(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value, "*.side")))
