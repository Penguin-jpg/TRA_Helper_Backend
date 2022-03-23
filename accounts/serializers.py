from rest_framework import serializers
from .models import Clerk


class ClerkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clerk
        fields = ["id", "url", "first_name", "last_name", "station"]
