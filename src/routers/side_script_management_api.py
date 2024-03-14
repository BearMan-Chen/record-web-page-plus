from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, send_from_directory
from glob import glob
from json import load, dump
from os import rename
from os.path import basename, join, exists
from re import search
from shutil import rmtree

from src.constants.enum_other import EnumScriptJson
from src.constants.enum_server import EnumServer, EnumFlask, EnumFlaskRoute
from src.constants.my_enum import EnumRouteAttribute
from src.routers.socket_api import upload_delete_change
from src.side_to_tests import SideToTests
from src.functions.def_open import open_r, open_w

side_script_management = Blueprint(EnumFlask.SIDE_SCRIPT_MANAGEMENT.name_, __name__)


def backup_version(file_name: str) -> str:
    file_path = join(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value, file_name)
    if exists(file_path):
        rename(file_path, join(EnumServer.BACKUP_VERSION__FOLDER_PATH.value, f"{file_name}.v{datetime.now(tz=timezone(timedelta(hours=0))).timestamp()}"))
    return file_path


def __delete_all_script_and_folder__(fileid: str) -> None:
    if exists(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value):
        all_script_json = load(open_r(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value))
        dump([script_json for script_json in all_script_json if fileid != script_json[EnumScriptJson.FILE_ID.name_]], open_w(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value))

    test_folder = join(EnumServer.TESTS__FOLDER_PATH.value, f"""test_{fileid}""")
    if exists(test_folder):
        rmtree(test_folder)


@side_script_management.post(EnumFlaskRoute.UPLOAD_SIDE_FILES.route)
def upload_side_files() -> dict:
    for file in request.files.values():
        if search(r"\.side$", file.filename.strip()):
            file_path = backup_version(file.filename.strip())
            file.save(file_path)
            SideToTests().main([file_path])
            upload_delete_change()
    return current_all_side()


@side_script_management.get(EnumFlaskRoute.DOWNLOAD_SIDE_FILE.route_args(EnumRouteAttribute.FILE_NAME))
def download_side_file(file_name: str) -> send_from_directory:
    return send_from_directory(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value, file_name, as_attachment=True, download_name=file_name)


@side_script_management.delete(EnumFlaskRoute.DELETE_SIDE_FILES.route_args(EnumRouteAttribute.FILE_NAME))
def delete_side_files(file_name: str) -> dict:
    if isinstance(file_name, str):
        backup_version(file_name.strip())
        __delete_all_script_and_folder__(SideToTests.sha1(SideToTests.filename(file_name)))
        upload_delete_change()
    return current_all_side()


@side_script_management.get(EnumFlaskRoute.CURRENT_ALL_SIDE.route)
def current_all_side() -> dict:
    return {basename(file): True for file in glob(join(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value, "*.side"))} if exists(EnumServer.UPLOAD_SIDE__FOLDER_PATH.value) else {}
