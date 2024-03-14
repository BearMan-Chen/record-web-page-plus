from src.functions.def_regex import Regex


class CmdSelection(Regex):
    def _select(self, target, value):
        return [
            f"""is_value, option_value = self.re_select({self.re_variable_value(value)})""",
            f"""getattr(Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)}))), \"select_by_value\" if is_value else \"select_by_visible_text\")(option_value)"""
        ]

    def _add_selection(self, target, value):
        return [
            f"""is_value, option_value = self.re_select({self.re_variable_value(value)})""",
            f"""getattr(Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)}))), \"select_by_value\" if is_value else \"select_by_visible_text\")(option_value)"""
        ]

    def _remove_selection(self, target, value):
        return [
            f"""is_value, option_value = self.re_select({self.re_variable_value(value)})""",
            f"""getattr(Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)}))), \"deselect_by_value\" if is_value else \"deselect_by_visible_text\")(option_value)"""
        ]

    def _select_frame(self, target, value):
        return [f"""self.select_frame({self.re_variable_value(target)})"""]

    def _check(self, target, value):
        return [f"""self.driver.execute_script(\"arguments[0].checked = true;\", self.driver.find_element(*self.re_by({self.re_variable_value(target)})))"""]

    def _uncheck(self, target, value):
        return [f"""self.driver.execute_script(\"arguments[0].checked = false;\", self.driver.find_element(*self.re_by({self.re_variable_value(target)})))"""]
