from src.functions.def_regex import Regex


class CmdInput(Regex):
    def _type(self, target, value):
        return [
            f"""element = self.driver.find_element(*self.re_by({self.re_variable_value(target)}))""",
            f"""element.send_keys(Keys.CONTROL, \"a\")""",
            f"""element.send_keys({self.re_variable_value(value)})"""
        ]

    def _send_keys(self, target, value):
        return [f"""self.driver.find_element(*self.re_by({self.re_variable_value(target)})).send_keys(self.re_send_key({self.re_variable_value(value)}))"""]

    def _submit(self, target, value):
        return [f"""self.driver.find_element(*self.re_by({self.re_variable_value(target)})).submit()"""]

    def _edit_content(self, target, value):
        return [
            f"""element = self.driver.find_element(*self.re_by({self.re_variable_value(target)}))""",
            f"""assert element.get_attribute(\"contenteditable\") == \"true\"""",
            f"""element.send_keys(Keys.CONTROL, \"a\")""",
            f"""element.send_keys({self.re_variable_value(value)})""",
        ]
