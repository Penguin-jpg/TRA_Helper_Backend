from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import TRAUserViewset, EditProfileView

router = DefaultRouter()
router.register(r"accounts", TRAUserViewset)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "accounts/<int:pk>/edit-profile/",
        EditProfileView.as_view(),
        name="edit-profile",
    ),
]
