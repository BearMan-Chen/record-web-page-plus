from src.functions.def_regex import Regex
from src.functions.def_mouse import Mouse


class CmdMouse(Regex, Mouse):
    def _click(self, target, value):
        return self.mouse_event(target, "", "click")

    def _click_at(self, target, value):
        return self.mouse_event(target, value, "click", True)

    def _double_click(self, target, value):
        return self.mouse_event(target, "", "dblclick")

    def _double_click_at(self, target, value):
        return self.mouse_event(target, value, "dblclick", True)

    def _mouse_down(self, target, value):
        return self.mouse_event(target, "", "mousedown")

    def _mouse_down_at(self, target, value):
        return self.mouse_event(target, value, "mousedown", True)

    def _mouse_move_at(self, target, value):
        return self.mouse_event(target, value, "mousemove", True)

    def _mouse_up(self, target, value):
        return self.mouse_event(target, "", "mouseup")

    def _mouse_up_at(self, target, value):
        return self.mouse_event(target, value, "mouseup", True)

    def _drag_and_drop_to_object(self, target, value):
        return self.mouse_event(target, value, "dragdrop", False)

    def _mouse_over(self, target, value):
        return [
            f"""ActionChains(self.driver).move_to_element(self.driver.find_element(*self.re_by({self.re_variable_value(target)}))).perform()"""
        ]

    def _mouse_out(self, target, value):
        return [
            f"""ActionChains(self.driver).move_to_element_with_offset(self.driver.execute_script("return document.documentElement"), *self.driver.execute_script(\"\"\"return [-Math.min(document.documentElement.getBoundingClientRect()["width"], window.innerWidth)/2, -Math.min(document.documentElement.getBoundingClientRect()["height"], window.innerHeight)/2]\"\"\")).perform()"""
        ]
