from django.db import models

from bases.models import ClassModel
from sales.models import Contract, Order
from content.models import Video, Playlist
from component.models import Product
# Create your models here.
 

class Document(ClassModel):

    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # duration_pauta = models.IntegerField(null=False, blank=False)
    repeat_pauta_day = models.FloatField(null=False, blank=False)
    repeat_in_pauta = models.IntegerField(null=False, blank=False)
    # second_total_pauta = models.IntegerField(null=False, blank=False)
    second_total_day = models.IntegerField(null=False, blank=False)
    time_contract = models.IntegerField(null=False, blank=False)
    time_bonification = models.IntegerField(null=False, blank=False)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

class Report_day(ClassModel):
    date_now = models.DateField(null=False, blank=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
