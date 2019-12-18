from django.db import models

from bases.models import ClassModel
from sales.models import Contract
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

