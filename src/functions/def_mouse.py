from typing import Literal
from src.functions.def_regex import Regex


class Mouse:
    @staticmethod
    def dragdrop(target: str, value: str) -> list:
        return [
            f"""rect = self.driver.execute_script(\"\"\"return arguments[0].getBoundingClientRect();\"\"\", self.driver.find_element(*self.re_by({Regex.re_variable_value(value)})))""",
            f"""ActionChains(self.driver).drag_and_drop_by_offset(self.driver.find_element(*self.re_by({Regex.re_variable_value(target)})), rect[\"width\"] / 2, rect[\"height\"] / 2).perform()"""
        ]

    @staticmethod
    def mouse_event(target: str, value: str, mouse_event_type: Literal["click", "dblclick", "mouseup", "mousedown", "mousemove", "dragdrop", "mouseover", "mouseout"], with_at: bool = False) -> list:
        if mouse_event_type == "dragdrop":
            return [
                f"""re_search = self.re_by({Regex.re_variable_value(target)})""",
                f"""x, y = self.re_fetch_xy(self.driver.execute_script(\"\"\"return arguments[0].getBoundingClientRect();\"\"\", self.driver.find_element(*re_search)), True)""",
                """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mousedown\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                f"""re_search = self.re_by({Regex.re_variable_value(value)})""",
                f"""x, y = self.re_fetch_xy(self.driver.execute_script(\"\"\"return arguments[0].getBoundingClientRect();\"\"\", self.driver.find_element(*re_search)))""",
                """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mousemove\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mouseup\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
            ]
        else:
            mouse_event: list = []
            if mouse_event_type == "click":
                mouse_event = [
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mousedown\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mouseup\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                ]
            elif mouse_event_type == "dblclick":
                mouse_event = [
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mousedown\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mouseup\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mousedown\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                    """self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"mouseup\", {bubbles:true,clientX:arguments[1],clientY:arguments[2]}));\"\"\", self.driver.find_element(*re_search), x, y)""",
                ]
            mouse_event += [f"""self.driver.execute_script(\"\"\"arguments[0].dispatchEvent(new MouseEvent(\"{mouse_event_type}\", {{bubbles:true,clientX:arguments[1],clientY:arguments[2]}}));\"\"\", self.driver.find_element(*re_search), x, y)"""]
            return [
                f"""re_search = self.re_by({Regex.re_variable_value(target)})""",
                f"""x, y = self.re_fetch_xy(self.driver.execute_script(\"\"\"return arguments[0].getBoundingClientRect();\"\"\", self.driver.find_element(*re_search)), {with_at}, {mouse_event_type in ["mousedown", "mouseup"] and not with_at}, {Regex.re_variable_value(value)})""",
            ] + mouse_event
