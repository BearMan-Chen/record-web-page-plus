from src.functions.def_regex import Regex


class CmdBrowser(Regex):
    def _open(self, target, value):
        return [f"""self.open({self.re_variable_value(target)}.strip())"""]

    @staticmethod
    def _close(target, value):
        return [f"""self.driver.get("data:,") if len(self.driver.window_handles) == 1 else self.driver.close()"""]

    def _set_window_size(self, target, value):
        return [
            f"""wh = {self.re_variable_value(target)}.split(\"x\")""",
            f"""self.driver.set_window_size(wh[0], wh[1])"""
        ]

    def _store_window_handle(self, target, value):
        return [f"""self.vars[{self.re_variable_key(target)}] = self.driver.current_window_handle"""]

    def _select_window(self, target, value):
        return [f"""self.driver.switch_to.window(self.re_window({self.re_variable_value(target)}))"""]

    @staticmethod
    def _window_handles(target, value):
        return [f"""self.window_handles = self.driver.window_handles"""]

    def _opens_window(self, target, value):
        return [f"""self.vars[{self.re_variable_key(target)}] = self.wait_for_window({value})"""]
