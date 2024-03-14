from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from multiprocessing import freeze_support
from os import makedirs
from os.path import abspath
from os.path import exists
from psutil import disk_usage
from signal import signal, SIGINT
from sys import exit

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumServer, EnumFlask, EnumFlaskRoute
# from move_dict_to_templates import delete_and_copy_templates
from src.routers.edit_test_plan_api import edit_sides
from src.routers.run_web_test_api import run_tests, kill_task, update_progress
from src.routers.side_script_management_api import side_script_management
from src.routers.socket_api import server_emit_test_screenshot
from src.routers.view_and_download_api import view_and_download
from src.routers.socket_api import socketio, server_emit_speed_time, server_emit_test_result_change, update_run_test_info
from src.side_to_tests import main
from src.variable import Variable as Var

app = Flask(__name__, static_folder=EnumServer.STATIC__FOLDER_PATH.value)
app.register_blueprint(run_tests)
app.register_blueprint(edit_sides)
app.register_blueprint(side_script_management)
app.register_blueprint(view_and_download)
# 下載檔案，在客戶端可以取得檔名
CORS(app, expose_headers=["Content-Disposition"])
socketio.init_app(app, cors_allowed_origins="*")


# shutdown(sig, frame)
def shutdown(_, __):
    kill_task(Var.task_main)
    exit(0)


@app.get(EnumFlaskRoute.HOME.route)
def home():
    return render_template(EnumFlask.HOME_FILE.value)


@app.get(EnumFlaskRoute.ICON.route)
def icon():
    return send_from_directory(EnumServer.TEMPLATES__FOLDER_PATH.value, EnumFlask.ICON_FILE.value, mimetype='image/vnd.microsoft.icon')


@app.get(EnumFlaskRoute.DISK_USAGE.route)
def app_disk_usage():
    return str(disk_usage(abspath(".")).percent)


@app.post(EnumFlaskRoute.UPDATE_RUN_TEST_INFO.route)
def app_update_run_test_info():
    if request.remote_addr == EnumServer.HOSTNAME.value:
        update_run_test_info(request.json)
        return "OK"
    return "", 202


@app.post(EnumFlaskRoute.UPDATE_SPEED_TIME.route)
def app_update_speed_time():
    if request.remote_addr == EnumServer.HOSTNAME.value:
        server_emit_speed_time(request.json[EnumKey.SPEED_TIME.name_])
        return "OK"
    return "", 202


@app.get(EnumFlaskRoute.UPDATE_REPORT_HISTORY.route)
def app_update_report_history():
    if request.remote_addr == EnumServer.HOSTNAME.value:
        server_emit_test_result_change()
        return "OK"
    return "", 202


@app.post(EnumFlaskRoute.BASE64_SCREENSHOT.route)
def app_base64_screenshot():
    if request.remote_addr == EnumServer.HOSTNAME.value:
        server_emit_test_screenshot(request.json[EnumServer.BASE64.name_])
        return "OK"
    return "", 202


@app.get(EnumFlaskRoute.UPDATE_PROGRESS_FOR_TEST.route)
def app_update_progress_for_test():
    if request.remote_addr == EnumServer.HOSTNAME.value:
        update_progress(Var.allure_result_folders_and_info)
        return "OK"
    return "", 202


@app.get(EnumFlaskRoute.FETCH_CONTROL_PYTEST_RUNNING.route)
def app_fetch_control_pytest_running() -> (str, int):
    if request.remote_addr == EnumServer.HOSTNAME.value:
        return str(Var.control_pytest_running)
    return "", 202


if __name__ == '__main__':
    # delete_and_copy_templates()
    freeze_support()
    for folder_path in [EnumServer.UPLOAD_SIDE__FOLDER_PATH.value, EnumServer.BACKUP_VERSION__FOLDER_PATH.value, EnumServer.RUN_DATA__FOLDER_PATH.value]:
        if not exists(folder_path):
            makedirs(folder_path, exist_ok=True)
    signal(SIGINT, shutdown)
    main()
    # socketio.run(app, host=ConstAPI.Hostname, port=ConstAPI.Port, ssl_context="adhoc", debug=False, allow_unsafe_werkzeug=True)
    socketio.run(app, host=EnumServer.HOSTNAME.value, port=EnumServer.PORT.value, debug=False, allow_unsafe_werkzeug=True)
