from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from .models import Ticket
from .serializers import TicketSerializer
from utils.choices import STATIONS_LIST, TRAINS_LIST


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
    lookup_url_kwargs = "ticket_pk"

    def create(self, request, *args, **kwargs):
        request.data["user"] = kwargs["pk"]  # 取得要找的使用者
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.get_object()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["start_station"] = STATIONS_LIST[data["start_station"]]
        data["end_station"] = STATIONS_LIST[data["end_station"]]
        data["train"] = TRAINS_LIST[data["train"]]
        return Response(data)
