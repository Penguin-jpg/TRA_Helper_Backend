from rest_framework import serializers
from .models import TRAUser


class TRAUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TRAUser
        fields = [
            "url",
            "id",
            "last_name",
            "first_name",
            "identity_number",
            "phone_number",
            "is_visually_impaired",
            "current_station",
        ]
