from src.functions.def_regex import Regex
from src.config import Config


class CmdLoop(Regex):
    def _while(self, target, value):
        return [f"""while {self.re_script(target)}:"""]

    def _times(self, target, value):
        return [
            f"""times = {self.re_variable_value(target)}.strip()""",
            f"""for _ in range(int(float(times) if times else 0)):"""
        ]

    def _for_each(self, target, value):
        return [
            f"""for_each = {self.re_variable_value(target, True)}""",
            f"""for self.vars[{self.re_variable_key(value)}] in for_each if isinstance(for_each, str) or isinstance(for_each, list) else []:"""
        ]

    def _do(self, target, value):
        return [f"""while True:"""]

    def _repeat_if(self, target, value):
        return [
            f"""if not {self.re_script(target)}:""",
            f"""{Config.space(1)}break"""
        ]
