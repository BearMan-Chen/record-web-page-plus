import base64
import requests
from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer, EnumFlaskRoute


class Requests:
    @staticmethod
    def post_base64_screenshot(base64_screenshot: base64) -> None:
        requests.post(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.BASE64_SCREENSHOT.route}", json={EnumServer.BASE64.name_: base64_screenshot})

    @staticmethod
    def post_update_run_test_info(json: dict) -> None:
        requests.post(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.UPDATE_RUN_TEST_INFO.route}", json=json)

    @staticmethod
    def post_update_speed_time(speed_time: float) -> None:
        requests.post(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.UPDATE_SPEED_TIME.route}", json={EnumKey.SPEED_TIME.name_: speed_time})

    @staticmethod
    def get_update_report_history() -> None:
        requests.get(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.UPDATE_REPORT_HISTORY.route}")

    @staticmethod
    def get_update_progress_for_test() -> None:
        requests.get(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.UPDATE_PROGRESS_FOR_TEST.route}")

    @staticmethod
    def fetch_control_pytest_running() -> bool:
        return requests.get(f"{EnumServer.LOCAL_URL.value}/{EnumFlaskRoute.FETCH_CONTROL_PYTEST_RUNNING.route}").text == "True"
