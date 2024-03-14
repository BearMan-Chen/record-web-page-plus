from datetime import datetime
from os.path import exists
from re import search, sub, findall
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.config import Config


class Regex:
    @staticmethod
    def re_url(value: str, original: str) -> str:
        groups_value = search(r"^([^/:]+?)?(:)?(/*)?([^/:]+?)?(/.*)?$", value.strip()).groups("")
        groups_original = search(r"^([^/:]+?)?(:)?(/*)?([^/:]+?)?(/.*)?$", original.strip()).groups("")
        if not value:
            result_url = original
        elif groups_value[0] and groups_value[1]:
            result_url = value
        elif not groups_value[0] and not groups_value[1] and len(groups_value[2]):
            result_url = f"""{groups_original[0]}{groups_original[1]}{groups_original[2]}{groups_original[3] if len(groups_value[2]) == 1 else ""}{value}"""
        else:
            result_url = f"""{groups_original[0]}{groups_original[1]}{groups_original[2]}{groups_original[3]}{sub(r"/[^/]*$", "", groups_original[4])}/{value}"""
        return result_url

    @staticmethod
    def re_by(value: str) -> tuple:
        re_search = search(rf"({'|'.join(Config.by.keys())})=(.+)", value) if isinstance(value, str) else None
        return [group if idx else Config.by[group] for idx, group in enumerate(re_search.groups())] if re_search else (By.XPATH if search(r"^//.*?$", value) else By.ID, value)

    @staticmethod
    def re_replace(value: str) -> str:
        return rf"{value}".strip()

    @staticmethod
    def re_variable_key(value: str) -> str:
        return f"""self.save_value_by_vars(r\'\'\' {value} \'\'\'[1:-1])"""

    @staticmethod
    def re_variable_value(value: str, add_braces: bool = False, to_str: bool = False, for_script: bool = False) -> str:
        if add_braces:
            return f"""self.get_variable(r\'\'\' {value} \'\'\'[1:-1], {add_braces}, {to_str}, {for_script})"""
        return f"""self.get_value_by_vars(r\'\'\' {value} \'\'\'[1:-1], {for_script})"""

    def re_script(self, value: str, with_return: str = "return ") -> str:
        if not isinstance(with_return, str) or with_return != "return ":
            with_return = ""
        return f"""self.driver.execute_script(r\"{with_return}\" + {self.re_variable_value(value, False, False, True)})"""

    def re_async_script(self, value: str, with_return: str = "return ") -> str:
        return f"""self.driver.execute_async_script(f\"\"\"var callback = arguments[arguments.length - 1];{with_return}{{{self.re_variable_value(value, False, False, True)}}}.then(callback).catch(callback);\"\"\")"""

    @staticmethod
    def re_send_key(value: str) -> str:
        re_findall = findall(r"\${.*?}", value)
        for re_find in re_findall:
            replace_search = sub(r"\${KEY_(.*?)}", r"\1", re_find)
            value = value.replace(re_find, getattr(Keys, replace_search) if hasattr(Keys, replace_search) else re_find, 1)
        return value

    @staticmethod
    def re_replace_backslash(value: str) -> str:
        return value.replace("\\", "\\\\")

    def re_select(self, value: str) -> [bool, str]:
        re_groups = search(r"^(.*=)?(.*)$", value).groups()
        return [re_groups[0] == "value=", re_groups[1].strip()]

    @staticmethod
    def re_window(value: str) -> any:
        return findall(r"^handle=(\w+)$", value)[0]

    @staticmethod
    def re_id(value: str) -> str:
        return sub(r"[^0-9a-zA-Z]", r"_", value).lower()

    @staticmethod
    def re_rm_underline(value: str) -> str:
        return sub(r"_", r"", value)

    @staticmethod
    def re_convert_file_and_folder_name(name: str) -> str:
        return sub(r"""[\\/:*?"<>|]""", "_", name.strip().rstrip(". "))

    @staticmethod
    def re_handel_text_for_windows_cmd(text: str) -> str:
        if isinstance(text, str):
            return sub(r"""([\\])""", r"""\\\1""", text)
        return ""

    @staticmethod
    def fetch_birth_datetime(text: (str, bytes)) -> float:
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        if isinstance(text, str):
            return datetime.strptime(" ".join(search(r"Birth: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\d{3} (\+\d{4})(?:\n|$)", text).groups()), "%Y-%m-%d %H:%M:%S.%f %z").timestamp()
        return 0.0

    @staticmethod
    def check_video_file_finish(video_file_path: str) -> bool:
        if exists(video_file_path):
            final_video_io = open(video_file_path, "rb")
            final_video_io.seek(-20, 2)
            if b"Lavf" in final_video_io.read():
                return True
        return False

    @staticmethod
    def re_fetch_xy(rect: dict, with_at: bool = False, is_zero: bool = False, value: str = "") -> tuple[int, int]:
        x: int = 0
        y: int = 0
        if not is_zero:
            if with_at:
                x = rect["x"]
                y = rect["y"]
                xy = search(r"^([^,]+?)(?:,([^,]+?))?(?:,|$)", value)
                if xy:
                    groups = xy.groups()
                    try:
                        x += int(float(groups[0]))
                    except:
                        x = 0
                    try:
                        y += int(float(groups[1]))
                    except:
                        y = 0
            else:
                x = rect["x"] + rect["width"] / 2
                y = rect["y"] + rect["height"] / 2
        return x, y

    @staticmethod
    def re_select_frame(value: str) -> str:
        frame = search(r"^(?:relative|index)=(.+?)$", value)
        if frame:
            return frame.groups()[0].strip()
        else:
            raise f"Failed: Invalid argument【{value}】"
