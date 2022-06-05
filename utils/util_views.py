from rest_framework import views
from rest_framework.response import Response
from .external_data import STATIONS_DATA, get_selected_trains
from .choices import STATIONS_LIST, INVERSE_STATIONS_MAP


class StationNameToPosView(views.APIView):
    def get_object(self):
        name = self.kwargs.get("name")
        try:
            return STATIONS_DATA[name]
        except KeyError:
            return "查無此車站"

    def get(self, request, name, format=None):
        station_pos = self.get_object()
        if station_pos != "查無此車站":
            return Response({"x": station_pos[0], "y": station_pos[1]})
        else:
            return Response({"detail": "查無此車站"})


class SelectTrainView(views.APIView):
    def get(self, request, format=None):
        try:
            start_station = request.data["start_station"]
            end_station = request.data["end_station"]
            start_time = request.data["start_time"]
            end_time = request.data["end_time"]
        except KeyError:
            return Response({"detail": "json資料錯誤"})

        if not start_station in STATIONS_LIST and not end_station in STATIONS_LIST:
            return Response({"detail": "車站資料錯誤"})

        selected_trains = get_selected_trains(
            start_station=start_station,
            end_station=end_station,
            start_time=start_time,
            end_time=end_time,
        )

        return Response(selected_trains)
