from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from .models import TRAUser
from .serializers import TRAUserSerializer


class TRAUserViewset(viewsets.ModelViewSet):
    queryset = TRAUser.objects.all()
    serializer_class = TRAUserSerializer
    # permission_classes = [] 待加入
