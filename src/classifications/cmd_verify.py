from src.config import Config
from src.functions.def_regex import Regex


class CmdVerify(Regex):
    def _verify(self, target, value):
        return [f"""check.equal({self.re_variable_value(target, True, True)}, {self.re_variable_value(value)})"""]

    def _verify_title(self, target, value):
        return [f"""check.equal(self.driver.title, {self.re_variable_value(target)})"""]

    def _verify_text(self, target, value):
        return [f"""check.equal(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text, {self.re_variable_value(value)})"""]

    def _verify_not_text(self, target, value):
        return [f"""check.not_equal(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text, {self.re_variable_value(value)})"""]

    def _verify_value(self, target, value):
        return [f"""check.equal(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).get_attribute(\"value\"), {self.re_variable_value(value)})"""]

    def _verify_checked(self, target, value):
        return [f"""check.is_true(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_selected())"""]

    def _verify_not_checked(self, target, value):
        return [f"""check.is_false(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_selected())"""]

    def _verify_element_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""check.greater(len(self.driver.find_elements(*self.re_by({self.re_variable_value(target)}))), 0)""",
            f"""self.driver.implicitly_wait(30)"""
        ]

    def _verify_element_not_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""check.equal(len(self.driver.find_elements(*self.re_by({self.re_variable_value(target)}))), 0)""",
            f"""self.driver.implicitly_wait(30)"""
        ]

    def _verify_editable(self, target, value):
        return [f"""check.is_true(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_enabled())"""]

    def _verify_not_editable(self, target, value):
        return [f"""check.is_false(self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_enabled())"""]

    def _verify_selected_label(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.all_selected_options.__len__() == 1:""",
            f"""{Config.space(1)}check.equal(select.first_selected_option.text.strip(), {self.re_variable_value(value)}.strip())""",
            f"""else:""",
            f"""{Config.space(1)}raise WebDriverException("The verify selected label method only handles one selected option.")""",
        ]

    def _verify_selected_value(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.is_multiple:""",
            f"""{Config.space(1)}raise WebDriverException("The verify selected value method can not be used on multiple selections.")""",
            f"""else:""",
            f"""{Config.space(1)}check.equal(select.first_selected_option.get_attribute(\"value\").strip(), {self.re_variable_value(value)}.strip())""",
        ]

    def _verify_not_selected_value(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.is_multiple:""",
            f"""{Config.space(1)}raise WebDriverException("The verify not selected value method can not be used on multiple selections.")""",
            f"""else:""",
            f"""{Config.space(1)}check.not_equal(select.first_selected_option.get_attribute(\"value\").strip(), {self.re_variable_value(value)}.strip())""",
        ]
