from src.functions.def_regex import Regex


class CmdScript(Regex):
    def _run_script(self, target, value):
        return [f"""{self.re_script(target, "")}"""]

    def _execute_script(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = {self.re_script(target, "")}"""]

    def _execute_async_script(self, target, value):
        return [f"""self.vars[{self.re_variable_key(value)}] = {self.re_async_script(target, "")}"""]
