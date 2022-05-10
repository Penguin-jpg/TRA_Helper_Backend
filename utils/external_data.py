from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
import re
import json

APP_ID = "64c272f958d0465b912299a04188cd2e"
APP_KEY = "ylPy-noRI1c7KPKHanG7tZh-ddU"
BASIC_STATIONS_INFO_URL = (
    "https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/Station?%24top=10000&%24format=JSON"
)
BASIC_TRAINS_INFO_URL = "https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/GeneralTrainInfo?%24top=10000&%24format=JSON"
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


def get_stations_data(url):
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


def get_trains_data(url):
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


# STATIONS_DATA = get_stations_data(BASIC_STATIONS_INFO_URL)
# TRAINS_DATA = get_trains_data(BASIC_TRAINS_INFO_URL)
STATIONS_DATA = get_stations_data_from_file(STATIONS_JSON_PATH)
TRAINS_DATA = get_trains_data_from_file(TRAINS_JSON_PATH)
