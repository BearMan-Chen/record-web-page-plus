from flask import Blueprint, send_from_directory, send_file
from os.path import join, exists, dirname
from shutil import rmtree

from src.constants.enum_other import EnumKey
from src.constants.enum_server import EnumFlask, EnumFlaskRoute, EnumServer
from src.constants.my_enum import EnumRouteAttribute
from src.functions.def_report import Report
from src.variable import Variable as Var

view_and_download = Blueprint(EnumFlask.VIEW_AND_DOWNLOAD.name_, __name__)


@view_and_download.get(EnumFlaskRoute.REPORT_HISTORY.route)
def view_and_download_report_history() -> list:
    return Report.report_history()


@view_and_download.get(EnumFlaskRoute.VIEW_ALLURE.route_args(EnumRouteAttribute.DATE_TIME))
def view_allure(date_time: str) -> send_from_directory:
    return send_from_directory(join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, date_time), Report.allure_report_html(date_time))


@view_and_download.delete(EnumFlaskRoute.DELETE_ALLURES.route_args(EnumRouteAttribute.DATE_TIME))
def delete_allures(date_time: str) -> tuple[str, int]:
    allure_folder_path = join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, date_time)
    if Var.run_test_info.get(EnumKey.STATUS.name_) == 2 and Var.allure_result_folders_and_info.get(EnumServer.ALLURE_OUTPUT.name_) == allure_folder_path:
        return rf"This {date_time} Folder is using.", 202
    else:
        if exists(allure_folder_path):
            rmtree(allure_folder_path)
        return "", 200


@view_and_download.get(EnumFlaskRoute.DOWNLOAD_ALLURE.route_args(EnumRouteAttribute.DATE_TIME))
def download_allure(date_time: str) -> send_from_directory:
    return send_from_directory(join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, date_time), Report.allure_report_html(date_time), as_attachment=True, download_name=Report.allure_report_html(date_time))


@view_and_download.get(EnumFlaskRoute.TEST_CASES_VIDEO.route_args(EnumRouteAttribute.DATE_TIME))
def test_cases_video(date_time: str) -> list:
    return Report.fetch_test_cases_video(date_time)


@view_and_download.get(EnumFlaskRoute.TEST_CASE_VIDEO.route_args(EnumRouteAttribute.DATE_TIME, EnumRouteAttribute.FILE_NAME))
def test_case_video(date_time: str, file_name: str) -> send_file:
    return send_file(Report.fetch_test_cast_video_file_abspath(date_time, file_name, EnumServer.VIDEO__FORMAT.value), mimetype='video/mp4', as_attachment=True)


@view_and_download.get(EnumFlaskRoute.TEST_CASE_SUBTITLE.route_args(EnumRouteAttribute.DATE_TIME, EnumRouteAttribute.FILE_NAME))
def test_case_subtitle(date_time: str, file_name: str) -> send_file:
    return send_file(Report.fetch_test_cast_video_file_abspath(date_time, file_name, EnumServer.SUBTITLE__FORMAT.value), mimetype='text/vtt', as_attachment=True)


@view_and_download.get(EnumFlaskRoute.TEST_CASE_MERGE_VIDEO_SUBTITLE.route_args(EnumRouteAttribute.DATE_TIME, EnumRouteAttribute.FILE_NAME))
def test_case_merge_video_subtitle(date_time: str, file_name: str) -> send_file:
    video_file_abspath = Report.fetch_test_cast_video_file_abspath(date_time, file_name, EnumServer.VIDEO__FORMAT.value)
    subtitle_file_abspath = Report.fetch_test_cast_video_file_abspath(date_time, file_name, EnumServer.SUBTITLE__FORMAT.value)
    output_video_file_abspath = Report.get_final_merge_video_subtitle_file_abspath(dirname(video_file_abspath), file_name, EnumServer.VIDEO__FORMAT.value)
    if exists(video_file_abspath) and exists(subtitle_file_abspath):
        if not exists(output_video_file_abspath):
            Report.insert_srt_to_video(video_file_abspath, subtitle_file_abspath, output_video_file_abspath)
        return send_file(output_video_file_abspath, mimetype='video/mp4', as_attachment=True)
    return "not found files", 202
