from src.functions.def_regex import Regex


class CmdStore(Regex):
    def _store(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = {self.re_variable_value(target)}"""]

    def _store_title(self, target, value):
        return [
            f"""target = {self.re_variable_value(target)}""",
            f"""self.vars[{self.re_variable_key(value)}] = target if target else self.driver.title"""
        ]

    def _store_json(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = json.loads({self.re_variable_value(target)})"""]

    def _store_text(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = self.driver.find_element(*self.re_by({self.re_variable_value(target)})).text"""]

    def _store_value(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = self.driver.find_element(*self.re_by({self.re_variable_value(target)})).get_attribute(\"value\")"""]

    def _store_attribute(self, target, value):
        return [
            f"""target_split = {self.re_variable_value(target)}.rsplit(\"@\", 1)""",
            f"""self.vars[{self.re_variable_key(value)}] = self.driver.find_element(*self.re_by(target_split[0])).get_attribute(target_split[1])"""
        ]

    def _store_xpath_count(self, target, value):
        return [
            f"""self.driver.implicitly_wait(0)""",
            f"""self.vars[{self.re_variable_key(value)}] = len(self.driver.find_elements(*self.re_by({self.re_variable_value(target)})))""",
            f"""self.driver.implicitly_wait(30)"""
        ]
