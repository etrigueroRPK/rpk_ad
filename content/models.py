from django.db import models

from bases.models import ClassModel
from sales.models import Contract, Order
from component.models import Product, City
# Create your models here.
 

class Video(ClassModel):
    name = models.CharField(max_length=100)
    duration = models.TimeField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(upload_to='videos', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        
        return '{}:{}'.format(self.name, self.duration)

    def duration_all(self):
        duration = str(self.duration)
        return duration

    def duration_seconds(self):
        t = self.duration
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        
        # print(type(seconds)) 
        return seconds


class Playlist(ClassModel):
    create_date = models.DateField(null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    proyection = models.BooleanField(default=False, null=False, blank=False)
    
    def __str__(self):
        return '{} del {} '.format(self.product, self.create_date)

class Playlist_spot_detail(ClassModel):
    repeat_count = models.IntegerField(null=False, blank=False)
    time_total = models.IntegerField(null=False, blank=False)
    porcentage = models.FloatField(null=False, blank=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Playlist_client_detail(ClassModel):
    time_total = models.IntegerField(null=False, blank=False)
    pauta_loop = models.FloatField(null=False, blank=False)
    second_total = models.IntegerField(null=False, blank=False)
    time_contract = models.IntegerField(null=False, blank=False)
    time_bonification = models.IntegerField(null=False, blank=False)

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Playlist_document(ClassModel):
    order_list = models.IntegerField(null=False, blank=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class Drive_urls(ClassModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    info = models.CharField(max_length=20, null=True, blank=True)
    url = models.CharField(max_length=500, null=False, blank=False)
    