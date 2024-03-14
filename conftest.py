import pytest
import sys
from pytest import Config
from logging import getLogger
from re import search

from src.constants.enum_server import EnumPytest
from src.functions.def_open import open_w
from src.functions.def_report import Report

log = getLogger(__name__)


def pytest_configure(config):
    """ Create a log file if log_file is not mentioned in *.ini file"""
    option = dict()
    for arg in config.invocation_params.args:
        re_search = search(r"^(--[a-z_]+)=([\w\d\-_:./\\]+)$", arg)
        if re_search:
            groups = re_search.groups()
            option[groups[0]] = groups[1]
    log_file_path = option[EnumPytest.LOG_FILE_ABSPATH.value] if EnumPytest.LOG_FILE_ABSPATH.value in option else Report.abspath_log_path(Report.datetime_tz8_str())
    config.option.log_file = log_file_path
    sys.stdout = open_w(log_file_path)


def pytest_unconfigure():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


def pytest_addoption(parser):
    parser.addoption(EnumPytest.LOG_FILE_ABSPATH.value, action="store", help="Specify the log file path")
    parser.addoption(EnumPytest.TEST_VIDEO_FOLDER_ABSPATH.value, action="store", help="test video folder path")


@pytest.fixture(scope="session")
def test_video_folder_abspath(pytestconfig: Config) -> str:
    return pytestconfig.getoption(EnumPytest.TEST_VIDEO_FOLDER_ABSPATH.value)
