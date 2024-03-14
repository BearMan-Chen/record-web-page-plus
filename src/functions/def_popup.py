from src.constants.enum_other import EnumDialogs


class Popup:
    popup_alert_confirm_text: str | None = None
    popup_alert_confirm_next: EnumDialogs | None = None
    popup_answer_text: str | None = None
    popup_prompt_text: str | None = None
    popup_prompt_next: EnumDialogs | None = None
    popup_ACCEPT = EnumDialogs.ACCEPT
    popup_ANSWER = EnumDialogs.ANSWER

    def popup_handle(self):
        try:
            alert = self.driver.switch_to.alert
            try:
                alert.send_keys("")
                self.popup_prompt_text = alert.text
                if self.popup_prompt_next == EnumDialogs.ANSWER:
                    alert.send_keys(self.popup_answer_text)
                    alert.accept()
                    self.popup_answer_text = ""
                else:
                    alert.dismiss()
                self.popup_prompt_next = None
            except:
                self.popup_alert_confirm_text = alert.text
                if self.popup_alert_confirm_next == EnumDialogs.ACCEPT:
                    alert.accept()
                else:
                    alert.dismiss()
                self.popup_alert_confirm_next = None
        except:
            pass

    def popup_prompt_answer(self, text: str):
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            self.popup_prompt_text = alert.text
            alert.accept()
        except:
            pass

    def popup_alert_confirm_accept(self):
        try:
            alert = self.driver.switch_to.alert
            self.popup_alert_confirm_text = alert.text
            alert.accept()
        except:
            pass

    def popup_alert_confirm_dismiss(self):
        try:
            alert = self.driver.switch_to.alert
            self.popup_alert_confirm_text = alert.text
            alert.dismiss()
        except:
            pass

    def popup_prompt_dismiss(self):
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys("")
            self.popup_prompt_text = alert.text
            alert.dismiss()
        except:
            pass
