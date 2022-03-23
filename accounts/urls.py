from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import TRAUserViewset

router = DefaultRouter()
router.register(r"accounts", TRAUserViewset)

urlpatterns = [path("", include(router.urls))]
