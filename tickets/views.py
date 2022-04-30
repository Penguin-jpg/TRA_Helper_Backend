from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from accounts.models import TRAUser
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
        user_id = kwargs["pk"]
        user = TRAUser.objects.get(id=user_id)
        queryset = Ticket.objects.filter(user=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        self.get_object()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["start_station"] = STATIONS_LIST[data["start_station"]]
        data["end_station"] = STATIONS_LIST[data["end_station"]]
        data["train"] = TRAINS_LIST[data["train"]]
        return Response(data)
