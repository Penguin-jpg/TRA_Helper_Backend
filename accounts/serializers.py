from rest_framework import serializers
from rest_framework.response import Response
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
            # "password",
            "email",
            "phone_number",
            "is_visually_impaired",
        ]

    def create(self, validated_data):
        identity_number = validated_data.pop("identity_number")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        return TRAUser.objects.create_user(
            identity_number=identity_number,
            email=email,
            password=password,
            **validated_data
        )


# 變更密碼用的serializer
class EditProfileSerializer(serializers.Serializer):
    identity_number = serializers.CharField(max_length=10, read_only=True)
    old_password = serializers.CharField(max_length=128, write_only=True)  # 舊密碼
    new_password = serializers.CharField(
        max_length=128, allow_blank=True, write_only=True
    )  # 新密碼
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=10, write_only=True)
    last_name = serializers.CharField(max_length=10, write_only=True)
    phone_number = serializers.CharField(max_length=10, write_only=True)
    is_visually_impaired = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email")
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.phone_number = validated_data.get("phone_number")
        instance.is_visually_impaired = validated_data.get("is_visually_impaired")
        instance.save()
        return instance
