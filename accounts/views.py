from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from .models import TRAUser
from .serializers import TRAUserSerializer, EditProfileSerializer


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class(
            instance=self.token, context={"request": self.request}
        )
        data = {"id": self.request.user.id}
        data.update(serializer.data)

        response = Response(
            data=data,
            status=status.HTTP_200_OK,
        )
        return response


class CustomLogoutView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        response = Response({"detail": "登出成功"}, status=status.HTTP_200_OK)
        return response


class TRAUserViewset(viewsets.ModelViewSet):
    queryset = TRAUser.objects.all()
    serializer_class = TRAUserSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class EditProfileView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = TRAUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditProfileSerializer

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # 更新資料(PUT)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
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
