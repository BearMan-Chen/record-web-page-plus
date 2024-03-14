from csv import reader
from datetime import datetime, timedelta, timezone
from glob import glob
from json import load
from os import makedirs, remove, rename
from os.path import join, split, getctime, sep, exists, basename
from subprocess import Popen, PIPE
from urllib.parse import unquote

from src.constants.enum_other import EnumElTreeProps, EnumKey
from src.constants.enum_server import EnumServer
from src.functions.def_open import open_r, open_w
from src.functions.def_regex import Regex

chars = f"{sep}\f\n\r\t\v "


class Report:
    @staticmethod
    def run_popen(popen_list: list) -> bytes:
        if isinstance(popen_list, list):
            popen = Popen(popen_list, shell=EnumServer.IS_WINDOWS.value, stdin=PIPE, stdout=PIPE)
            outs, errs = popen.communicate()
            if errs:
                print("ERROR", errs)
            return outs

    @staticmethod
    def datetime_tz8_str() -> str:
        return datetime.strftime(datetime.now(tz=timezone(timedelta(hours=8))), EnumServer.DATETIME__FORMAT.value)

    @staticmethod
    def abspath_log_path(file_name: str) -> str:
        makedirs(EnumServer.LOG__FOLDER_PATH.value, exist_ok=True)
        return join(EnumServer.LOG__FOLDER_PATH.value, f"{file_name}.{EnumServer.LOG__FORMAT.value}")

    @staticmethod
    def allure_report_html(date_time: str) -> str:
        return f"allure_report_{date_time}.html"

    @staticmethod
    def create_allure_result_folders_and_info(folder_name: str, total: int) -> dict:
        allure_result_folder_path: str = join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, folder_name)
        allure_result_folders: dict = {
            EnumServer.ALLURE_OUTPUT.name_: allure_result_folder_path,
            EnumServer.ALLURE_FOR_OPEN.name_: join(allure_result_folder_path, EnumServer.ALLURE_FOR_OPEN.name_),
            EnumServer.ALLURE_FOR_SERVE.name_: join(allure_result_folder_path, EnumServer.ALLURE_FOR_SERVE.name_),
            EnumServer.ALLURE_LOG.name_: join(allure_result_folder_path, f"{folder_name}.{EnumServer.LOG__FORMAT.value}"),
            EnumServer.ALLURE_SINGLE_HTML.name_: join(allure_result_folder_path, Report.allure_report_html(folder_name)),
            EnumServer.ALLURE_TEST_VIDEOS.name_: join(allure_result_folder_path, EnumServer.ALLURE_TEST_VIDEOS.name_),
            EnumServer.ALLURE_TOTAL__FILE.name_: total
        }
        for key, value in allure_result_folders.items():
            if key in [
                EnumServer.ALLURE_OUTPUT.name_,
                EnumServer.ALLURE_FOR_OPEN.name_,
                EnumServer.ALLURE_FOR_SERVE.name_,
                EnumServer.ALLURE_TEST_VIDEOS.name_
            ]:
                makedirs(value, exist_ok=True)
        open_w(join(allure_result_folder_path, EnumServer.ALLURE_TOTAL__FILE.value)).write(str(total))
        return allure_result_folders

    @staticmethod
    def fetch_test_cast_video_root_path(date_time: str) -> str:
        return join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, date_time, EnumServer.ALLURE_TEST_VIDEOS.name_).__str__()

    @staticmethod
    def fetch_test_cast_video_file_abspath(date_time: str, file_name: str, file_type: str) -> str:
        return glob(join(Report.fetch_test_cast_video_root_path(date_time), "**", f"{unquote(file_name)}.{file_type}"), recursive=True)[0]

    @staticmethod
    def get_all_test_case_folder(root_folder: str, sort_by_ctime: bool = True) -> list:
        folders = glob(join(root_folder, "*", "*", ""))
        return sorted(folders, key=lambda folder: getctime(folder) if EnumServer.IS_WINDOWS.value else Regex.fetch_birth_datetime(Report.run_popen(["stat", folder]))) if sort_by_ctime else folders

    @staticmethod
    def get_rel_path(root_folder: str, sub_folder: str) -> str:
        return sub_folder[len(root_folder) if sub_folder[:len(root_folder)] == root_folder else 0:].strip(chars)

    @staticmethod
    def get_final_video_file_path(root_folder: str, sub_folder: str, only_file_name: bool = False) -> str:
        rel_path: str = Report.get_rel_path(root_folder, sub_folder)
        file_name = f"""{rel_path.replace(sep, EnumServer.VIDEO_SUBTITLE_SEP__FORMAT.value)}.{EnumServer.VIDEO__FORMAT.value}"""
        return file_name if only_file_name else join(root_folder, rel_path, file_name)

    @staticmethod
    def get_final_subtitle_file_path(root_folder: str, sub_folder: str, only_file_name: bool = False) -> str:
        rel_path: str = Report.get_rel_path(root_folder, sub_folder)
        file_name = f"""{rel_path.replace(sep, EnumServer.VIDEO_SUBTITLE_SEP__FORMAT.value)}.{EnumServer.SUBTITLE__FORMAT.value}"""
        return file_name if only_file_name else join(root_folder, rel_path, file_name)

    @staticmethod
    def get_final_merge_video_subtitle_file_abspath(video_folder_abspath: str, file_name: str, file_type: str) -> str:
        return join(video_folder_abspath, f"{file_name}(with subtitle).{file_type}")

    @staticmethod
    def fetch_test_cases_video(date_time: str) -> list:
        def dict_to_list(input_data: dict) -> list:
            output_list: list = []
            if isinstance(input_data, dict):
                for input_key, input_value in input_data.items():
                    output_list.append({
                        EnumElTreeProps.LABEL.name_: input_key,
                        EnumElTreeProps.CHILDREN.name_: dict_to_list(input_value),
                        EnumElTreeProps.PATH.name_: "",
                    })
            elif isinstance(input_data, str):
                filename = Report.get_final_video_file_path(test_cast_video_root_path, input_data, True)
                output_list.append({
                    EnumElTreeProps.LABEL.name_: filename,
                    EnumElTreeProps.CHILDREN.name_: [],
                    EnumElTreeProps.PATH.name_: input_data,
                })
            return output_list

        result = {}
        test_cast_video_root_path = Report.fetch_test_cast_video_root_path(date_time)
        test_video_folder_path_len = len(test_cast_video_root_path)
        for test_case_folder_path in Report.get_all_test_case_folder(test_cast_video_root_path):
            if Regex.check_video_file_finish(Report.get_final_video_file_path(test_cast_video_root_path, test_case_folder_path)):
                temp = result
                test_case_sub_folders: str = test_case_folder_path[test_video_folder_path_len:].strip(chars)
                *test_case_split_sub_folders, last_test_case_sub_folder = test_case_sub_folders.split(sep)
                for test_case_split_folder in test_case_split_sub_folders:
                    temp = temp.setdefault(test_case_split_folder, {})
                temp[last_test_case_sub_folder] = test_case_sub_folders.replace(sep, EnumServer.VIDEO_SUBTITLE_SEP__FORMAT.value)
        return dict_to_list(result)

    @staticmethod
    def insert_srt_to_video(video_path: str, subtitle_path: str, output_path: str) -> None:
        Report.run_popen([
            r"ffmpeg.exe" if EnumServer.IS_WINDOWS.value else "ffmpeg",
            "-y",
            "-i",
            rf"{video_path}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            # rf"subtitles=\'{Regex.re_handel_text_for_windows_cmd(subtitle_path)}\':force_style='FontName=SourceHanSansCN-Bold,PrimaryColour=&HBBFFFFFF,OutlineColour=&HBB000000,BorderStyle=2'",
            rf"subtitles=\'{Regex.re_handel_text_for_windows_cmd(subtitle_path)}\'",
            rf"{output_path}"
        ])

    @staticmethod
    def save_video_size(test_cast_video_root_path: str) -> None:
        for test_case_folder_path in Report.get_all_test_case_folder(test_cast_video_root_path):
            video_file_path = Report.get_final_video_file_path(test_cast_video_root_path, test_case_folder_path)
            if exists(video_file_path):
                video_file_name = split(video_file_path)[-1]
                Report.run_popen([r"ffmpeg.exe" if EnumServer.IS_WINDOWS.value else "ffmpeg", "-y", "-i", video_file_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", video_file_name])
                remove(video_file_path)
                rename(video_file_name, video_file_path)

    @staticmethod
    def seconds_to_hmsf(seconds: float) -> str:
        if seconds < 0:
            seconds = 0
        return f"{int(seconds // 3600):02}:{int(seconds % 3600 // 60):02}:{int(seconds % 60):02}.{int(seconds % 1 * 1000):03}"

    @staticmethod
    def csv_to_vtt(subtitle_file_path: str, video_file_path: str) -> None:
        if exists(subtitle_file_path):
            csv_reader = list(reader(open_r(subtitle_file_path)))
            subtitle_vtt = ["WEBVTT"]
            if csv_reader and csv_reader[0] and csv_reader[0][0] != subtitle_vtt[0]:
                csv_reader = [[float(_)] + __ for _, *__ in csv_reader]
                *rows, last_row = csv_reader
                start_timestamp = getctime(video_file_path) if EnumServer.IS_WINDOWS.value else Regex.fetch_birth_datetime(Report.run_popen(["stat", video_file_path]))
                for idx, row in enumerate(rows):
                    subtitle_vtt.append(f"{idx}\n{Report.seconds_to_hmsf(row[0] - start_timestamp)} --> {Report.seconds_to_hmsf(csv_reader[idx + 1][0] - start_timestamp)}\n{row[1]}")
                subtitle_vtt.append(f"{len(csv_reader) - 1}\n{Report.seconds_to_hmsf(last_row[0] - start_timestamp)} --> 99:59:59.999\n{last_row[1]}")
                open_w(subtitle_file_path).write("\n\n".join(subtitle_vtt))

    @staticmethod
    def fetch_progress(allure_for_serve_results_json_file_path: list, allure_total_file_path: str) -> dict:
        finish_progres, total_progres, pass_count = 0, 0, 0
        total_progres = int(open_r(allure_total_file_path).read().strip())
        for allure_for_serve_result_json_file_path in allure_for_serve_results_json_file_path:
            temp_status = load(open_r(allure_for_serve_result_json_file_path))[EnumKey.STATUS.name_].upper()
            if temp_status == "PASSED":
                pass_count += 1
            if temp_status != "SKIPPED":
                finish_progres += 1
        return {
            EnumKey.FINISH_COUNT.name_: finish_progres,
            EnumKey.TOTAL_COUNT.name_: total_progres,
            EnumKey.FINISH_RATE.name_: finish_progres / total_progres * 100 if total_progres else 0,
            EnumKey.PASS_RATE.name_: pass_count / finish_progres * 100 if finish_progres else 0
        }

    @staticmethod
    def report_history() -> list:
        return [
            {
                EnumKey.ID.name_: idx + 1,
                EnumKey.NAME.name_: basename(row),
                EnumKey.PROGRESS.name_: Report.fetch_progress(
                    glob(join(row, EnumServer.ALLURE_FOR_SERVE.name_, "*-result.json")),
                    join(row, EnumServer.ALLURE_TOTAL__FILE.value)
                )
            } for idx, row in enumerate(sorted(glob(join(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value, "*")), reverse=True))
        ] if exists(EnumServer.ALLURE_RESULTS__FOLDER_PATH.value) else []
