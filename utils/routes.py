# 存放所有路由
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import TRAUserViewset, EditProfileView
from tickets.views import TicketViewSet

router = DefaultRouter()
router.register(r"accounts", TRAUserViewset)
router.register(r"tickets", TicketViewSet)

ticket_list = TicketViewSet.as_view({"get": "list"})
ticket_create = TicketViewSet.as_view({"post": "create"})

urlpatterns = [
    path("", include(router.urls)),
    path("accounts/<int:pk>/edit/", EditProfileView.as_view(), name="edit-profile"),
    path("accounts/<int:pk>/tickets/", ticket_list, name="ticket-list"),
    path("accounts/<int:pk>/tickets/create/", ticket_create, name="ticket-create"),
]
