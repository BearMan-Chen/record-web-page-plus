from src.functions.def_regex import Regex


class CmdPopupWindow(Regex):
    def _answer_on_next_prompt(self, target, value):
        return [f"""self.popup_answer_text, self.popup_prompt_next = {self.re_variable_value(target)}, self.popup_ANSWER""", ]

    def _choose_cancel_on_next_prompt(self, target, value):
        return []

    def _choose_ok_on_next_confirmation(self, target, value):
        return [f"""self.popup_alert_confirm_next = self.popup_ACCEPT"""]

    def _choose_cancel_on_next_confirmation(self, target, value):
        return []

    def _webdriver_answer_on_visible_prompt(self, target, value):
        return [f"""self.popup_prompt_answer({self.re_variable_value(target)})"""]

    def _webdriver_choose_cancel_on_visible_prompt(self, target, value):
        return [f"""self.popup_prompt_dismiss()"""]

    def _webdriver_choose_ok_on_visible_confirmation(self, target, value):
        return [f"""self.popup_alert_confirm_accept()"""]

    def _webdriver_choose_cancel_on_visible_confirmation(self, target, value):
        return [f"""self.popup_alert_confirm_dismiss()"""]
