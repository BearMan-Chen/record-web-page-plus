import pytest
import psutil
import re
import signal

from base64 import b64encode
from csv import writer
from io import BytesIO
from json import load, dumps
from logging import getLogger
from multiprocessing import Process, Value, Manager
from os import makedirs
from os.path import exists, join
from PIL.ImageGrab import grab
from psutil import pid_exists
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver, WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from subprocess import Popen, PIPE
from time import sleep, time

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer
from src.functions.def_open import open_r, open_a
from src.functions.def_report import Report
from src.functions.def_requests import Requests
from src.functions.def_regex import Regex
from src.functions.def_popup import Popup
from src.variable import Variable as Var

if EnumServer.IS_WINDOWS.value:
    from subprocess import CREATE_NEW_PROCESS_GROUP
else:
    from os import setpgrp
    from pyvirtualdisplay.display import Display

log = getLogger(__name__)


class DefaultPytest(Regex, Popup):
    def setup_class(self) -> None:
        self.driver: WebDriver
        self.display = None
        self.frames: list[int] = []
        self.test_case_video_path: str = ""
        self.test_case_subtitle_path: str = ""
        self.switch_list: list = []
        self.process_list: list = []
        self.control_pytest_running: bool = Requests.fetch_control_pytest_running()
        if self.control_pytest_running:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--ignore-certificate-errors-spki-list")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("log-level=3")
            options.add_argument('--charset=utf-8')
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self.bytes_for_socket_emit = Manager().Value(bytes, b"")
            if not EnumServer.IS_WINDOWS.value:
                self.display = Display(visible=False, size=(1920, 1080))
                self.display.start()
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(30)
            self.popen: Popen = None
            self.popen_list: list[str] = [
                "ffmpeg.exe" if EnumServer.IS_WINDOWS.value else "ffmpeg",
                "-y", "-r", "24", "-f",
                "gdigrab" if EnumServer.IS_WINDOWS.value else "x11grab",
                "-i", "desktop" if EnumServer.IS_WINDOWS.value else ":0.0",
                "-c:v", "libx264", "-crf", "33",
                "-pix_fmt", "yuv420p", "-an", "-sn"]
            self.create_and_start_process(self, self.send_screenshot, ())
            self.speed_time: float = float(open_r(EnumServer.SPEED_TIME__FILE_PATH.value).read()) if exists(EnumServer.SPEED_TIME__FILE_PATH.value) else 0
            self.vars = {}
            self.window_handles = []
            self.next_popup = None
            self.popup_text = None
            self.last_popup_text = None
            self.popup_send_text = None
            url_json: dict = load(open_r(EnumServer.URL_JSON__FILE_PATH.value)) if exists(EnumServer.URL_JSON__FILE_PATH.value) else {}
            self.url: str = url_json[EnumKey.MAIN_URL.name_].strip() if url_json else ""
            self.original: str = ""
            self.variable: dict = {f"${{{row[EnumKey.KEY.name_]}}}": row[EnumKey.VALUE.name_] for row in url_json[EnumKey.VARIABLE.name_]} if url_json else {}

    def teardown_class(self) -> None:
        if self.switch_list:
            for switch in self.switch_list:
                switch.value = False
            while not all(True if switch.value or not self.process_list[idx].is_alive() else False for idx, switch in enumerate(self.switch_list)):
                sleep(.05)
        if self.process_list:
            for process in self.process_list:
                process.terminate()
            while not all(not process.is_alive() for process in self.process_list):
                sleep(.05)
        if self.driver is not None:
            all_children: list[psutil.Process] = psutil.Process(self.driver.service.process.pid).children(True)
            self.driver.quit()
            for child in all_children:
                if pid_exists(child.pid):
                    child.terminate()
        if self.display is not None:
            self.display.stop()

    def setup_method(self, method) -> None:
        self.frames.clear()
        self.test_case_video_path = ""
        self.test_case_subtitle_path = ""
        self.check_pytest_running_status()
        Requests.get_update_progress_for_test()
        try:
            log.info(f"""# Main Url：{f"※{self.url}※" if self.url else "Use Default Url"}""")
            self.driver.get("data:,")
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 1).until(expected_conditions.alert_is_present())
            self.dismiss_popup()
        except:
            pass

    def teardown_method(self, method) -> None:
        if self.test_case_video_path and self.test_case_subtitle_path:
            sleep(1)
            if EnumServer.IS_WINDOWS.value:
                self.popen.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                self.popen.send_signal(signal.SIGINT)
            Report.csv_to_vtt(self.test_case_subtitle_path, self.test_case_video_path)

    def create_video_folder(self, *folders_name: str) -> None:
        test_case_folder_path = join(*folders_name).__str__()
        makedirs(test_case_folder_path, exist_ok=True)
        self.test_case_video_path = Report.get_final_video_file_path(folders_name[0], test_case_folder_path)
        self.popen = Popen(
            self.popen_list + [self.test_case_video_path],
            shell=EnumServer.IS_WINDOWS.value, stdin=PIPE, stdout=PIPE,
            preexec_fn=None if EnumServer.IS_WINDOWS.value else setpgrp,
            creationflags=CREATE_NEW_PROCESS_GROUP if EnumServer.IS_WINDOWS.value else 0)
        self.test_case_subtitle_path = Report.get_final_subtitle_file_path(folders_name[0], test_case_folder_path)
        while not exists(self.test_case_video_path):
            pass

    def append_subtitle(self, text: str = "") -> None:
        test_case_subtitle_path = self.test_case_subtitle_path
        if test_case_subtitle_path:
            writer(open_a(test_case_subtitle_path, newline="")).writerow([time(), text])

    @staticmethod
    def create_and_start_process(self, target, args: tuple):
        self.switch_list.append(Value('b', True))
        args = (self.switch_list[-1],) + args
        self.process_list.append(Process(target=target, args=args, daemon=True))
        self.process_list[-1].start()

    @staticmethod
    def send_screenshot(switch) -> None:
        bytes_io = BytesIO()
        while switch.value:
            bytes_io.seek(0)
            grab().save(bytes_io, format=EnumServer.IMAGE__FORMAT.value)
            Requests.post_base64_screenshot(b64encode(bytes_io.getvalue()).decode("utf-8"))
            sleep(.1)
        switch.value = True

    def check_pytest_running_status(self) -> None:
        if self.control_pytest_running:
            self.control_pytest_running: bool = Requests.fetch_control_pytest_running()
        if not self.control_pytest_running:
            pytest.skip("手動停止測試")

    def wait_for_window(self, timeout=1):
        sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.window_handles
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def get_value_by_vars(self, value: str, for_script: bool = False) -> str:
        find_multi_variable = re.sub(r"}.*?\${", f"}}{self.re_replace_backslash(value)}${{", value)
        if value == find_multi_variable:
            re_findall = re.findall(r"\${.*?}", value)
        else:
            re_findall = [variable for multi_variable in find_multi_variable.split(self.re_replace_backslash(value)) for variable in re.findall(r"\${.*?}", multi_variable)]
        for re_find in re_findall:
            value = value.replace(re_find, f"{self.get_variable(re_find, for_script=for_script)}", 1)
        return value

    def save_value_by_vars(self, value: str) -> str:
        return f"${{{self.get_value_by_vars(value)}}}"

    def get_variable(self, value: str, add_braces: bool = False, to_str: bool = False, for_script: bool = False) -> str:
        if add_braces:
            temp_value = f"${{{value}}}"
        else:
            temp_value = value
        have_square_brackets = re.search(r"\${(.+?)((?:\[\d+])+)}", temp_value)
        if have_square_brackets:
            temp_value = rf"""${{{have_square_brackets[1]}}}"""
        if temp_value in self.variable:
            result = self.variable[temp_value]
        elif temp_value in self.vars:
            result = self.vars[temp_value]
        else:
            result = self.get_json(self.vars, [v if idx else f"${{{v}}}" for idx, v in enumerate(temp_value[2:-1].split("."))])
        if have_square_brackets and result is not None:
            find_variables = re.findall(r"\[(.+?)]", have_square_brackets[2])
            for variable in find_variables:
                try:
                    if isinstance(result, list) or isinstance(result, dict):
                        result = result[int(variable)]
                    else:
                        result = None
                        break

                except:
                    result = None
                    break

        if add_braces and to_str:
            if result is None:
                return "null"
            elif isinstance(result, bool):
                return f"{result}".lower()
            elif isinstance(result, int):
                return f"{result}"
            else:
                return result
        else:
            if for_script:
                return dumps(result, ensure_ascii=False)
            return value if result is None else result

    def get_json(self, temp_vars: dict, keys: list = None) -> any:
        if len(keys) > 1:
            return self.get_json(temp_vars[keys[0]], keys[1:]) if keys[0] in temp_vars else None
        elif len(keys) == 1:
            return temp_vars[keys[0]] if keys[0] in temp_vars else None
        return None

    def open(self, value: str) -> None:
        open_url = self.re_url(value, self.url if self.url else self.original)
        try:
            self.driver.get(open_url)
        except WebDriverException as ex:
            log.warning(ex.msg)
        for frame in self.frames:
            self.driver.switch_to.frame(frame)
        log.info(rf"""# Open：※{open_url}※""")

    def sleep(self) -> None:
        if exists(EnumServer.SPEED_TIME__FILE_PATH.value):
            self.speed_time = float(open_r(EnumServer.SPEED_TIME__FILE_PATH.value).read())
        sleep(min(self.speed_time / 1000, 3))

    def set_speed(self, value: str) -> None:
        try:
            self.speed_time = min(float(value) / 1000, 3)
            Requests.post_update_speed_time(min(float(value), 3000))
        except:
            pass

    def run_commands(self, test_case: str, path: str, value: str) -> None:
        tests = load(open_r(path))
        if test_case in tests:
            Var.disable_assertions_condition = value.strip() == "--disable-assertions"
            self.__getattribute__(f"""_{self.re_id(tests[test_case])}_""")()
            Var.disable_assertions_condition = False

    def select_frame(self, value: str) -> None:
        frame: str = self.re_select_frame(value)
        if frame == "top":
            self.driver.switch_to.default_content()
            self.frames.clear()
        elif frame == "parent":
            self.driver.switch_to.parent_frame()
            self.frames.pop()
        else:
            frame_int = int(frame)
            self.driver.switch_to.frame(frame_int)
            self.frames.append(frame_int)

    def run_before_step(self, step_info: str):
        self.check_pytest_running_status()
        self.popup_handle()
        self.sleep()
        step_info = step_info.strip()
        log.info(step_info)
        self.append_subtitle(step_info)
