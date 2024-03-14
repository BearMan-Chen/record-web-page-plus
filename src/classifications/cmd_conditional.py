from src.functions.def_regex import Regex


class CmdConditional(Regex):
    def _if(self, target, value):
        return [f"""if {self.re_script(target)}:"""]

    def _else_if(self, target, value):
        return [f"""elif {self.re_script(target)}:"""]

    def _else(self, target, value):
        return [f"""else:"""]

    def _end(self, target, value):
        return []
