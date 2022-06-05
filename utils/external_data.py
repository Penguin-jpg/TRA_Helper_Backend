from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import re
import json
from requests import request


APP_ID = "64c272f958d0465b912299a04188cd2e"
APP_KEY = "ylPy-noRI1c7KPKHanG7tZh-ddU"
GENERAL_STATIONS_INFO_URL = (
    "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/Station?%24top=10000&%24format=JSON"
)
GENERAL_TRAINS_INFO_URL = "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/GeneralTrainInfo?%24top=10000&%24format=JSON"
GENERAL_TIME_TABLES_URL = "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/GeneralTimetable?%24top=10000&%24format=JSON"
STATIONS_JSON_PATH = "data/stations_json.json"
TRAINS_JSON_PATH = "data/trains_json.json"


class Auth:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        x_date = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(
            self.app_key.encode("utf-8"), ("x-date: " + x_date).encode("utf-8"), sha1
        )
        signature = base64.b64encode(hashed.digest()).decode()
        authorization = f'hmac username="{self.app_id}", algorithm="hmac-sha1", headers="x-date", signature="{signature}"'
        return {
            "Authorization": authorization,
            "x-date": x_date,
            "Accept - Encoding": "gzip",
        }


auth = Auth(APP_ID, APP_KEY)


def get_stations_data(url=GENERAL_STATIONS_INFO_URL):
    stations_json = request("get", url, headers=auth.get_auth_header()).json()
    station_names = [station["StationName"]["Zh_tw"] for station in stations_json]
    station_pos = [
        (
            station["StationPosition"]["PositionLat"],  # x座標(經度)
            station["StationPosition"]["PositionLon"],  # y座標(緯度)
        )
        for station in stations_json
    ]
    stations_data = {name: pos for name, pos in zip(station_names, station_pos)}
    return stations_data


def get_trains_data(url=GENERAL_TRAINS_INFO_URL):
    trains_json = request("get", url, headers=auth.get_auth_header()).json()
    train_nos = [train["TrainNo"] for train in trains_json]
    train_type_names = [
        re.sub(r"\([^()]*\)", "", train["TrainTypeName"]["Zh_tw"])  # 去除括號內(包含括號)的字串
        for train in trains_json
    ]

    trains_data = []
    for train_type_name, train_no in zip(train_type_names, train_nos):
        trains_data.append(f"{train_type_name} {str(train_no)}")

    return sorted(trains_data)


def get_selected_trains(
    url=GENERAL_TIME_TABLES_URL,
    start_station=None,
    end_station=None,
    start_time=None,
    end_time=None,
):
    time_tables_json = request("get", url, headers=auth.get_auth_header()).json()
    prefix_date = time_tables_json[0]["UpdateTime"]  # 取得年月日
    # 轉成datetime格式
    start_time = datetime.strptime(f"{prefix_date} {start_time}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{prefix_date} {end_time}", "%Y-%m-%d %H:%M")
    # 符合條件的資料
    selected_trains = []

    for time_table in time_tables_json:
        table = time_table["GeneralTimetable"]
        train_info = table["GeneralTrainInfo"]

        # 要找的起點站
        if train_info["StartingStationName"]["Zh_tw"] == start_station:
            start_stop_time = table["StopTimes"][0]
            arrival_start_time = datetime.strptime(
                f'{prefix_date} {start_stop_time["ArrivalTime"]}', "%Y-%m-%d %H:%M"
            )

            # 在要求的時間內才考慮
            if arrival_start_time >= start_time and arrival_start_time <= end_time:
                # 第一筆資料為起點站，所以不看
                stop_times = table["StopTimes"][1:]
                for stop_time in stop_times:
                    # print(stop_time)
                    # 要停靠的站
                    if stop_time["StationName"]["Zh_tw"] == end_station:
                        print("!")
                        selected_trains.append(
                            {
                                "train_no": train_info["TrainNo"],
                                "train_type": re.sub(
                                    r"\([^()]*\)",
                                    "",
                                    train_info["TrainTypeName"]["Zh_tw"],
                                ),
                                "arrival_time": f'{prefix_date} {stop_time["ArrivalTime"]}',  # 到站時間
                            }
                        )

    return selected_trains


def read_json(path):
    with open(path, encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data


def get_stations_data_from_file(path):
    stations_json = read_json(path)
    station_names = [station["StationName"]["Zh_tw"] for station in stations_json]
    station_pos = [
        (
            station["StationPosition"]["PositionLat"],  # x座標(經度)
            station["StationPosition"]["PositionLon"],  # y座標(緯度)
        )
        for station in stations_json
    ]
    stations_data = {name: pos for name, pos in zip(station_names, station_pos)}
    return stations_data


def get_trains_data_from_file(path):
    trains_json = read_json(path)
    train_nos = [train["TrainNo"] for train in trains_json]
    train_type_names = [
        re.sub(r"\([^()]*\)", "", train["TrainTypeName"]["Zh_tw"])  # 去除括號內(包含括號)的字串
        for train in trains_json
    ]

    trains_data = []
    for train_type_name, train_no in zip(train_type_names, train_nos):
        trains_data.append(f"{train_type_name} {str(train_no)}")

    return sorted(trains_data)


STATIONS_DATA = get_stations_data()
TRAINS_DATA = get_trains_data()
# STATIONS_DATA = get_stations_data_from_file(STATIONS_JSON_PATH)
# TRAINS_DATA = get_trains_data_from_file(TRAINS_JSON_PATH)
