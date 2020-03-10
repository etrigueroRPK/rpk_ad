from django.db import models

from bases.models import ClassModel
from sales.models import Contract
from component.models import Product
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


class play_list(ClassModel):
    create_date = models.DateField()
    play_list = models.FileField(upload_to='play_list', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    def __str__(self):
        return '{} del {} '.format(self.product, self.create_date)
