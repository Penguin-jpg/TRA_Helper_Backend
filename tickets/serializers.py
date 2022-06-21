from rest_framework import serializers
from accounts.models import TRAUser
from .models import Ticket
from utils.choices import (
    STATIONS_LIST,
    TRAINS_LIST,
    INVERSE_STATIONS_MAP,
    INVERSE_TRAINS_MAP,
)


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=TRAUser.objects.all())
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
    start_station = serializers.ChoiceField(choices=STATIONS_LIST, default=0)
    end_station = serializers.ChoiceField(choices=STATIONS_LIST, default=0)
    start_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
    end_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
    train = serializers.ChoiceField(choices=TRAINS_LIST, default=0)
    seat = serializers.CharField(max_length=15)
    QR_url = serializers.URLField()  # 電子車票的url

    class Meta:
        model = Ticket
        fields = [
            "url",
            "id",
            "user",
            "date",
            "start_station",
            "end_station",
            "start_time",
            "end_time",
            "train",
            "seat",
            "QR_url",
        ]

    def create(self, validated_data):
        return Ticket.objects.create(
            user=validated_data.get("user"),
            date=validated_data.get("date"),
            start_station=INVERSE_STATIONS_MAP[validated_data.get("start_station")],
            end_station=INVERSE_STATIONS_MAP[validated_data.get("end_station")],
            start_time=validated_data.get("start_time"),
            end_time=validated_data.get("end_time"),
            train=INVERSE_TRAINS_MAP[validated_data.get("train")],
            seat=validated_data.get("seat"),
            QR_url=validated_data.get("QR_url"),
        )
