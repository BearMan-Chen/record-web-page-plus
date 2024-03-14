import base64

from flask import session
from flask_socketio import SocketIO, join_room, leave_room

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer, EnumSocket
from src.functions.def_open import open_w
from src.functions.def_report import Report
from src.variable import Variable as Var

socketio = SocketIO()


def server_emit_test_screenshot(image_base64: base64) -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_TEST_SCREENSHOT.route, image_base64, room=EnumSocket.BEAR_ROOM.route)


def server_emit_speed_time(speed_time: float, include_self: bool = True) -> None:
    Var.run_test_info[EnumKey.SPEED_TIME.name_] = speed_time
    open_w(EnumServer.SPEED_TIME__FILE_PATH.value).write(str(speed_time))
    socketio.emit(EnumSocket.SERVER_EMIT_SPEED_TIME.route, speed_time, include_self=include_self)


def server_emit_test_result_change() -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_TEST_RESULT_CHANGE.route, Report.report_history())


def server_emit_run_test_info() -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_TEST_STATUS.route, Var.run_test_info)


@socketio.on(EnumSocket.CONNECT.name_)
def connect() -> None:
    print(EnumSocket.CONNECT.name_, session)


@socketio.on(EnumSocket.DISCONNECT.name_)
def disconnect() -> None:
    print(EnumSocket.DISCONNECT.name_, session)


@socketio.on(EnumSocket.JOIN_ROOM.route)
def join_bear_room() -> None:
    join_room(EnumSocket.BEAR_ROOM.route)


@socketio.on(EnumSocket.LEAVE_ROOM.route)
def leave_bear_room() -> None:
    leave_room(EnumSocket.BEAR_ROOM.route)


@socketio.on(EnumSocket.SERVER_ON_SPEED_TIME.route)
def on_update_speed_time(speed_time: int):
    server_emit_speed_time(speed_time, False)


@socketio.on(EnumSocket.SERVER_ON_VARIABLE_CHANGE.route)
def on_variable_change(data: dict) -> None:
    if Var.run_test_info[EnumKey.STATUS.name_] == 1 and EnumKey.MAIN_URL.name_ in data and EnumKey.VARIABLE.name_ in data:
        socketio.emit(EnumSocket.SERVER_EMIT_VARIABLE_CHANGE.route, data, include_self=False)
        update_run_test_info({EnumKey.TEST_VARIABLE.name_: data}, False)


def emit_reset() -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_RESET.route)


def upload_delete_change() -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_SIDE_FILES_CHANGE.route)


def test_plan_change(skip_sid) -> None:
    socketio.emit(EnumSocket.SERVER_EMIT_TEST_PLAN_CHANGE.route, skip_sid)


def update_run_test_info(datas: dict, emit: bool = True) -> None:
    for key, value in datas.items():
        if key in Var.run_test_info:
            Var.run_test_info[key] = value
    if emit:
        server_emit_run_test_info()
