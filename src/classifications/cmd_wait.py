from src.functions.def_regex import Regex


class CmdWait(Regex):
    def _wait_for_text(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, 30).until(expected_conditions.text_to_be_present_in_element(self.re_by({self.re_variable_value(target)}), {self.re_variable_value(value)}))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until(expected_conditions.presence_of_element_located(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_not_present(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until_not(expected_conditions.presence_of_element_located(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_visible(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until(expected_conditions.visibility_of_element_located(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_not_visible(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until_not(expected_conditions.visibility_of_element_located(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_editable(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until(expected_conditions.element_to_be_clickable(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]

    def _wait_for_element_not_editable(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""WebDriverWait(self.driver, float({self.re_variable_value(value)}) / 1000).until_not(expected_conditions.element_to_be_clickable(self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)""",
        ]
