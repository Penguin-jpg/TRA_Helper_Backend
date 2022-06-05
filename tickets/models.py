from django.db import models
from accounts.models import TRAUser
from utils.choices import STATIONS, TRAINS

# 車票
class Ticket(models.Model):
    user = models.ForeignKey(
        TRAUser, on_delete=models.CASCADE, related_name="tickets", verbose_name="使用者"
    )
    date = models.DateTimeField(verbose_name="日期")
    start_station = models.IntegerField(choices=STATIONS, default=0, verbose_name="起點站")
    end_station = models.IntegerField(choices=STATIONS, default=0, verbose_name="終點站")
    train = models.IntegerField(choices=TRAINS, default=0, verbose_name="車種")
    seat = models.CharField(max_length=15, verbose_name="座位")
    QR_url = models.URLField(verbose_name="電子車票", default="www.google.com")
