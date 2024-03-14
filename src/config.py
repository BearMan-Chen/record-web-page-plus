from selenium.webdriver.common.by import By


class Config:
    add_space = 4

    @staticmethod
    def space(times: int) -> str:
        return " " * Config.add_space * times

    default_test_main_import: list = [
        f"""import allure""",
        f"""import logging""",
        f""""""
    ]

    default_test_command_import: list = [
        f"""import time""",
        f"""import json""",
        f"""import logging""",
        f"""from src.decorator import disable_assertions""",
        f"""from pytest_check import check""",
        f"""from selenium.webdriver.remote.webdriver import WebDriverException""",
        f"""from selenium.webdriver.common.keys import Keys""",
        f"""from selenium.webdriver.support.wait import WebDriverWait""",
        f"""from selenium.webdriver.support import expected_conditions""",
        f"""from selenium.webdriver.support.ui import Select""",
        f"""from selenium.webdriver.common.action_chains import ActionChains""",
        f""""""
    ]

    default_test_self_import: list = [
        f"""from src.default_pytest import DefaultPytest""",
        f""""""
    ]

    default_test_log_import: list = [
        f"""log = logging.getLogger(__name__)""",
        f""""""
    ]

    by: dict = {
        "id": By.ID,
        "css": By.CSS_SELECTOR,
        "name": By.NAME,
        "xpath": By.XPATH,
        "tagName": By.TAG_NAME,
        "className": By.CLASS_NAME,
        "linkText": By.LINK_TEXT,
        "partialLinkText": By.PARTIAL_LINK_TEXT
    }
