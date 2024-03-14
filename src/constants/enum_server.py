from src.constants.my_enum import MyEnumPY, unique, auto
from os import name, environ
from os.path import abspath, join, expanduser


@unique
class EnumServer(MyEnumPY):
    IS_WINDOWS = name == "nt"
    HOSTNAME = "127.0.0.1"
    PORT = 9527
    PROTOCOL = "http"
    LOCAL_URL = f"{PROTOCOL}://{HOSTNAME}:{PORT}"
    LOG__FORMAT = "log"
    IMAGE__FORMAT = "jpeg"
    VIDEO__FORMAT = "mp4"
    SUBTITLE__FORMAT = "vtt"
    VIDEO_SUBTITLE_SEP__FORMAT = "→"
    DATETIME__FORMAT = "%Y-%m-%d_%H-%M-%S"
    ABSPATH = abspath("")
    TESTS__FOLDER_PATH = join(ABSPATH, "tests")
    LOG__FOLDER_PATH = join(ABSPATH, LOG__FORMAT)
    RESOURCES__FOLDER_PATH = join(ABSPATH, "resources")
    UPLOAD_SIDE__FOLDER_PATH = join(RESOURCES__FOLDER_PATH, "upload_side")
    BACKUP_VERSION__FOLDER_PATH = join(RESOURCES__FOLDER_PATH, "backup_version")
    RUN_DATA__FOLDER_PATH = join(RESOURCES__FOLDER_PATH, "run_data")
    URL_JSON__FILE_PATH = join(RUN_DATA__FOLDER_PATH, "url.json")
    ALL_SCRIPT_JSON__FILE_PATH = join(RUN_DATA__FOLDER_PATH, "all_script.json")
    TEMPLATES__FOLDER_PATH = join("", "templates")
    STATIC__FOLDER_PATH = join(TEMPLATES__FOLDER_PATH, "static")
    ALLURE_RESULTS__FOLDER_PATH = join(ABSPATH, "allure_results")
    ALLURE_TOTAL__FILE = "total.txt"
    ALLURE_OUTPUT = auto()
    ALLURE_FOR_OPEN = auto()
    ALLURE_FOR_SERVE = auto()
    ALLURE_TEST_VIDEOS = auto()
    ALLURE_LOG = auto()
    ALLURE_SINGLE_HTML = auto()
    COMPLETE_HTML_FILE = "complete.html"
    DOWNLOADS__FOLDER_PATH = join(environ["USERPROFILE"] if IS_WINDOWS else expanduser("~"), "Downloads", "")
    FILE_LIST__FILE = "filelist.txt"
    SPEED_TIME__FILE_PATH = join(RUN_DATA__FOLDER_PATH, "speedTime.txt")
    BASE64 = auto()


@unique
class EnumPytest(MyEnumPY):
    LOG_FILE_ABSPATH = "--log_file_abspath"
    TEST_VIDEO_FOLDER_ABSPATH = "--test_video_folder_abspath"


@unique
class EnumFlask(MyEnumPY):
    HOME_FILE = "index.html"
    ICON_FILE = "favicon.ico"
    RUN_TESTS = auto()
    EDIT_SIDES = auto()
    VIEW_AND_DOWNLOAD = auto()
    SIDE_SCRIPT_MANAGEMENT = auto


@unique
class EnumFlaskRoute(MyEnumPY):
    # web_test_fusion_server
    HOME = "/"
    ICON = "/favicon.ico"
    DISK_USAGE = auto()
    BASE64_SCREENSHOT = auto()
    UPDATE_RUN_TEST_INFO = auto()
    UPDATE_SPEED_TIME = auto()
    UPDATE_REPORT_HISTORY = auto()
    UPDATE_PROGRESS_FOR_TEST = auto()
    FETCH_CONTROL_PYTEST_RUNNING = auto()
    # side_script_management_api
    CURRENT_ALL_SIDE = auto()
    UPLOAD_SIDE_FILES = auto()
    DOWNLOAD_SIDE_FILE = auto()
    DELETE_SIDE_FILES = auto()
    # edit_sides_api
    ALL_SCRIPT = auto()
    REWRITE_ALL_SCRIPT = auto()
    # run_tests_api
    TEST_RESET = auto()
    TEST_STATUS = auto()
    TEST_CASES = auto()
    START_TEST_CASES = auto()
    STOP_TEST_CASES = auto()
    SHOW_FOLDER_FILES = auto()
    UPLOAD_FILES_FOR_TEST = auto()
    # view_and_download_api
    REPORT_HISTORY = auto()
    VIEW_ALLURE = auto()
    DELETE_ALLURES = auto()
    DOWNLOAD_ALLURE = auto()
    TEST_CASE_VIDEO = auto()
    TEST_CASE_SUBTITLE = auto()
    TEST_CASE_MERGE_VIDEO_SUBTITLE = auto()
    TEST_CASES_VIDEO = auto()


@unique
class EnumSocket(MyEnumPY):
    CONNECT = auto()
    DISCONNECT = auto()
    BEAR_ROOM = auto()
    JOIN_ROOM = auto()
    LEAVE_ROOM = auto()
    SERVER_ON_SPEED_TIME = auto()
    SERVER_ON_VARIABLE_CHANGE = auto()
    SERVER_EMIT_RESET = auto()
    SERVER_EMIT_SPEED_TIME = auto()
    SERVER_EMIT_VARIABLE_CHANGE = auto()
    SERVER_EMIT_TEST_STATUS = auto()
    SERVER_EMIT_TEST_SCREENSHOT = auto()
    SERVER_EMIT_TEST_PLAN_CHANGE = auto()
    SERVER_EMIT_SIDE_FILES_CHANGE = auto()
    SERVER_EMIT_TEST_RESULT_CHANGE = auto()
