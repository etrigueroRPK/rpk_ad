from django.db import models

from bases.models import ClassModel
# Create your models here.


class Category(ClassModel):
    name = models.CharField(max_length=50, help_text='Name category', unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to='categories', null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Location(ClassModel):
    name = models.CharField(max_length=50, help_text='Name location', unique=True)
    address = models.CharField(max_length=100)
    img = models.CharField(max_length=300, default='default.jpg')
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)


    def __str__(self):
        return '{}'.format(self.name)