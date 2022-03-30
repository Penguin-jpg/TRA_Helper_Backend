from gc import get_objects
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from .models import TRAUser
from .serializers import TRAUserSerializer, EditProfileSerializer


class TRAUserViewset(viewsets.ModelViewSet):
    queryset = TRAUser.objects.all()
    serializer_class = TRAUserSerializer
    # permission_classes = [] 待加入


class EditProfileView(APIView):
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]

    def get_object(self, pk):
        try:
            return TRAUser.objects.get(pk=pk)
        except TRAUser.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = TRAUserSerializer(instance, context={"request": request})
        return Response(serializer.data)

    # 變更資料(PUT)
    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = EditProfileSerializer(instance, data=request.data)

        if serializer.is_valid():
            # 舊密碼錯誤
            if not instance.check_password(
                serializer.validated_data.get("old_password")
            ):
                return Response({"detail": "密碼錯誤"}, status=status.HTTP_400_BAD_REQUEST)
            # 有要設定新密碼才做
            if serializer.validated_data.get("new_password") != "":
                instance.set_password(serializer.validated_data.get("new_password"))
            serializer.save()
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
