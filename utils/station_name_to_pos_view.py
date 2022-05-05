from rest_framework import views
from rest_framework.response import Response
from .external_data import STATIONS_DATA


class StationNameToPosView(views.APIView):
    def get_object(self, name):
        try:
            return STATIONS_DATA[name]
        except KeyError:
            return "查無此車站"

    def get(self, request, name, format=None):
        station_pos = self.get_object(name)
        if station_pos != "查無此車站":
            return Response({"x": station_pos[0], "y": station_pos[1]})
        else:
            return Response({"detail": "查無此車站"})
