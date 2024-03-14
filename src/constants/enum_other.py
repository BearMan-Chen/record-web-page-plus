from src.constants.my_enum import MyEnumPY, MyEnumJS, unique, auto


@unique
class EnumKey(MyEnumJS):
    # run_tests_api
    TEST_VARIABLE = auto()
    MAIN_URL = auto()
    VARIABLE = auto()
    KEY = auto()
    VALUE = auto()
    TEST_CASES = auto()
    SWITCH_MERGE_IMAGE_TO_VIDEO = auto()
    # view_and_download_api
    ID = auto()
    NAME = auto()
    FINISH_COUNT = auto()
    TOTAL_COUNT = auto()
    FINISH_RATE = auto()
    PASS_RATE = auto()
    # socket_api
    STATUS = auto()  # allure json file
    PROGRESS = auto()
    END_DATETIME = auto()
    START_DATETIME = auto()
    PROGRESS_RESULT = auto()
    SPEED_TIME = auto()
    DOWNLOADS_FOLDER_PATH = auto()
    SID = auto()


@unique
class EnumSideToTests(MyEnumPY):
    FUNCTION = auto()
    VALUE = auto()
    AFTER = auto()
    BEFORE = auto()


@unique
class EnumScriptJson(MyEnumJS):
    FILE_ID = auto()
    FILE_NAME = auto()
    PROJECT_ID = auto()
    PROJECT_NAME = auto()
    SUITE_ID = auto()
    SUITE_NAME = auto()
    SUITES = auto()
    CHECK = auto()
    TESTS = auto()
    TEST_ID = auto()
    TEST_NAME = auto()


@unique
class EnumSide(MyEnumJS):
    ID = auto()
    VERSION = auto()
    NAME = auto()
    URL = auto()
    TESTS = auto()
    SUITES = auto()
    URLS = auto()
    PLUGINS = auto()


@unique
class EnumSideSuites(MyEnumJS):
    ID = auto()
    NAME = auto()
    PERSIST_SESSION = auto()
    PARALLEL = auto()
    TIMEOUT = auto()
    TESTS = auto()


@unique
class EnumSideTests(MyEnumJS):
    ID = auto()
    NAME = auto()
    COMMANDS = auto()


@unique
class EnumSideTestsCommands(MyEnumJS):
    ID = auto()
    COMMENT = auto()
    COMMAND = auto()
    TARGET = auto()
    TARGETS = auto()
    VALUE = auto()
    OPENS_WINDOW = auto()
    WINDOW_HANDLE_NAME = auto()
    WINDOW_TIMEOUT = auto()


@unique
class EnumElTreeProps(MyEnumJS):
    LABEL = auto()
    CHILDREN = auto()
    PATH = auto()


@unique
class EnumDialogs(MyEnumJS):
    ACCEPT = auto()
    ANSWER = auto()
