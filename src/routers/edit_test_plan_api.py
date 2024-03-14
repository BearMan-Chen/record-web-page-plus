import json

from flask import Blueprint, request
from os.path import exists

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer, EnumFlask, EnumFlaskRoute
from src.routers.socket_api import test_plan_change
from src.functions.def_open import open_r, open_w

edit_sides = Blueprint(EnumFlask.EDIT_SIDES.name_, __name__)


@edit_sides.get(EnumFlaskRoute.ALL_SCRIPT.route)
def all_script() -> list | dict:
    return json.load(open_r(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value)) if exists(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value) else []


@edit_sides.post(EnumFlaskRoute.REWRITE_ALL_SCRIPT.route)
def rewrite_all_script():
    if exists(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value):
        json.dump(request.json[EnumServer.ALL_SCRIPT_JSON__FILE_PATH.name_], open_w(EnumServer.ALL_SCRIPT_JSON__FILE_PATH.value))
        test_plan_change(request.json[EnumKey.SID.name_])
        return "OK"
    return "Not found file", 412
