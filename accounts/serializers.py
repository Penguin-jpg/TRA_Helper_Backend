from rest_framework import serializers
from rest_framework.reverse import reverse
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
            "password",
            "phone_number",
        ]

    def create(self, validated_data):
        identity_number = validated_data.pop("identity_number")
        password = validated_data.pop("password")
        return TRAUser.objects.create_user(
            identity_number=identity_number, password=password, **validated_data
        )


# 變更資料用的serializer
class EditProfileSerializer(serializers.Serializer):
    identity_number = serializers.ReadOnlyField()
    old_password = serializers.CharField(
        max_length=128, allow_blank=False, write_only=True
    )
    new_password = serializers.CharField(
        max_length=128, allow_blank=True, write_only=True
    )
    last_name = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=10)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.phone_number = validated_data.get("phone_number")
        instance.save()
        return instance


# 多參數的url
class ParameterisedHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Represents the instance, or a property on the instance, using hyperlinking.

    lookup_fields is a tuple of tuples of the form:
        ('model_field', 'url_parameter')
    """

    lookup_fields = (("pk", "pk"),)

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop("lookup_fields", self.lookup_fields)
        super(ParameterisedHyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            attr = obj
            for field in model_field.split("."):
                attr = getattr(attr, field)
            kwargs[url_param] = attr

        return reverse(view_name, kwargs=kwargs, request=request, format=format)
