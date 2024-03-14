from src.functions.def_regex import Regex


class CmdTestTools(Regex):
    def _echo(self, target, value):
        return [f"""log.info({self.re_variable_value(target)})"""]

    def _pause(self, target, value):
        return [f"""time.sleep(float({self.re_variable_value(target)}) / 1000)"""]

    def _set_speed(self, target, value):
        return [f"""self.set_speed({self.re_variable_value(target)})"""]

    def _debugger(self, target, value):
        return [f"""pass  # debugger"""]

    def _run(self, target, value):
        return [f"""self.run_commands({self.re_variable_value(target)}, r\"{self.command_path}\", {self.re_variable_value(value)})"""]
