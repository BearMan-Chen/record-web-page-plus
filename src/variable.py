from json import load
from multiprocessing import Process
from os.path import exists

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer
from src.functions.def_open import open_r


class Variable:
    run_test_info: dict = {
        EnumKey.START_DATETIME.name_: "",
        EnumKey.END_DATETIME.name_: "",
        EnumKey.STATUS.name_: 1,
        EnumKey.PROGRESS.name_: 0,
        EnumKey.PROGRESS_RESULT.name_: {},
        EnumKey.TEST_VARIABLE.name_: load(open_r(EnumServer.URL_JSON__FILE_PATH.value)) if exists(EnumServer.URL_JSON__FILE_PATH.value) else {EnumKey.MAIN_URL.name_: "", EnumKey.VARIABLE.name_: []},
        EnumKey.DOWNLOADS_FOLDER_PATH.name_: EnumServer.DOWNLOADS__FOLDER_PATH.value,
        EnumKey.SPEED_TIME.name_: float(open_r(EnumServer.SPEED_TIME__FILE_PATH.value).read()) if exists(EnumServer.SPEED_TIME__FILE_PATH.value) else 1000,
    }
    disable_assertions_condition: bool = False
    control_pytest_running: bool = False
    allure_result_folders_and_info: dict = {}
    test_cases: list = []
    task_main: Process = Process()
