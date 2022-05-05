from .external_data import STATIONS_DATA, TRAINS_DATA

STATIONS_LIST = [""] + [name for name in STATIONS_DATA.keys()]  # 補上空值
STATIONS = ((index, name) for index, name in enumerate(STATIONS_LIST))
INVERSE_STATIONS_MAP = {name: index for index, name in enumerate(STATIONS_LIST)}
TRAINS_LIST = [train_name for train_name in TRAINS_DATA]
TRAINS = ((index, train_name) for index, train_name in enumerate(TRAINS_DATA))
INVERSE_TRAINS_MAP = {name: index for index, name in enumerate(TRAINS_DATA)}
