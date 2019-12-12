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
    img = models.ImageField(upload_to='categories', null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.name)

class Product(ClassModel):
    name = models.CharField(max_length=50, help_text='Name location', unique=True)
    place = models.CharField(max_length=100)
    img = models.ImageField(upload_to='categories', null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.category.name, self.name)
