from src.config import Config
from src.functions.def_regex import Regex


class CmdAssert(Regex):
    def _assert(self, target, value):
        return [f"""assert {self.re_variable_value(target, True, True)} == {self.re_variable_value(value)}, f\"\"\"{{{self.re_variable_value(target, True, True)}}} != {{{self.re_variable_value(value)}}}\"\"\""""]

    def _assert_title(self, target, value):
        return [f"""assert self.driver.title == {self.re_variable_value(target)}, f\"\"\"{{self.driver.title}} != {{{self.re_variable_value(target)}}}\"\"\""""]

    def _assert_text(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text == {self.re_variable_value(value)}, f\"\"\"{{self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text}} != {{{self.re_variable_value(value)}}}\"\"\""""]

    def _assert_not_text(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text != {self.re_variable_value(value)}, f\"\"\"{{self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text}} == {{{self.re_variable_value(value)}}}\"\"\""""]

    def _assert_value(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).get_attribute(\"value\") == {self.re_variable_value(value)}, f\"\"\"{{self.driver.find_element(*self.re_by({self.re_variable_value(target)})).get_attribute(\"value\")}} != {{{self.re_variable_value(value)}}}\"\"\""""]

    def _assert_checked(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_selected(), f\"\"\"{{{self.re_variable_value(target)}}} not checked.\"\"\""""]

    def _assert_not_checked(self, target, value):
        return [f"""assert not self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_selected(), f\"\"\"{{{self.re_variable_value(target)}}} had checked.\"\"\""""]

    def _assert_element_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""assert len(self.driver.find_elements(*self.re_by({self.re_variable_value(target)}))) > 0, f\"\"\"{{{self.re_variable_value(target)}}} not present.\"\"\"""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _assert_element_not_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""assert len(self.driver.find_elements(*self.re_by({self.re_variable_value(target)}))) == 0, f\"\"\"{{{self.re_variable_value(target)}}} always present.\"\"\"""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _assert_editable(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_enabled() is True, f\"\"\"{{{self.re_variable_value(target)}}} cannot editable.\"\"\""""]

    def _assert_not_editable(self, target, value):
        return [f"""assert self.driver.find_element(*self.re_by({self.re_variable_value(target)})).is_enabled() is False, f\"\"\"{{{self.re_variable_value(target)}}} can editable.\"\"\""""]

    def _assert_selected_label(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.all_selected_options.__len__() == 1:""",
            f"""{Config.space(1)}assert select.first_selected_option.text.strip() == {self.re_variable_value(value)}.strip(), f\"\"\"{{select.first_selected_option.text.strip()}} != {{{self.re_variable_value(value)}}}.strip()\"\"\"""",
            f"""else:""",
            f"""{Config.space(1)}raise WebDriverException("The assert selected label method only handles one selected option.")""",
        ]

    def _assert_selected_value(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.is_multiple:""",
            f"""{Config.space(1)}raise WebDriverException("The assert selected value method can not be used on multiple selections.")""",
            f"""else:""",
            f"""{Config.space(1)}assert select.first_selected_option.get_attribute(\"value\").strip() == {self.re_variable_value(value)}.strip(), f\"\"\"{{select.first_selected_option.get_attribute(\"value\").strip()}} != {{{self.re_variable_value(value)}}}.strip()\"\"\""""
        ]

    def _assert_not_selected_value(self, target, value):
        return [
            f"""select = Select(self.driver.find_element(*self.re_by({self.re_variable_value(target)})))""",
            f"""if select.is_multiple:""",
            f"""{Config.space(1)}raise WebDriverException("The assert not selected value method can not be used on multiple selections.")""",
            f"""else:""",
            f"""{Config.space(1)}assert select.first_selected_option.get_attribute(\"value\") != {self.re_variable_value(value)}, f\"\"\"{{select.first_selected_option.get_attribute(\"value\")}} == {{{self.re_variable_value(value)}}}\"\"\""""
        ]

    def _assert_alert(self, target, value):
        return [
            f"""assert self.popup_alert_confirm_text == {self.re_variable_value(target)}, f\"\"\"{{self.popup_alert_confirm_text}} != {{{self.re_variable_value(target)}}}\"\"\"""",
            f"""self.popup_alert_confirm_text = None""",
        ]

    def _assert_confirmation(self, target, value):
        return [
            f"""assert self.popup_alert_confirm_text == {self.re_variable_value(target)}, f\"\"\"{{self.popup_alert_confirm_text}} != {{{self.re_variable_value(target)}}}\"\"\"""",
            f"""self.popup_alert_confirm_text = None""",
        ]

    def _assert_prompt(self, target, value):
        return [
            f"""assert self.popup_prompt_text == {self.re_variable_value(target)}, f\"\"\"{{self.popup_prompt_text}} != {{{self.re_variable_value(target)}}}\"\"\"""",
            f"""self.popup_prompt_text = None""",
        ]
