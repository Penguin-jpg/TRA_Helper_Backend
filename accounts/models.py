from django.db import models
from django.contrib.auth.models import AbstractUser, Group

STATIONS = ()
SEX = ((0, "女"), (1, "男"))

# 站務人員
class Clerk(AbstractUser):
    station = models.IntegerField(choices=STATIONS, default=0, verbose_name="車站")
