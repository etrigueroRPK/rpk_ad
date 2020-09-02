from django.db import models

from datetime import time

from bases.models import ClassModel
# Create your models here.


class Category(ClassModel):
    name = models.CharField(max_length=50, help_text='Name category', unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to='categories', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

class City(ClassModel):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    
    def __str__(self):
        return '{}'.format(self.name)

class Location(ClassModel):
    name = models.CharField(max_length=50, help_text='Name location', unique=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(upload_to='categories', null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


    def __str__(self):
        return '{} {}'.format(self.city.name, self.name)

class Product(ClassModel):
    name = models.CharField(max_length=50, help_text='Name location', unique=False)
    place = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(upload_to='product', null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_operating = models.TimeField(default='00:00') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return '{}   {}   {}'.format(self.category.name, self.location.name,  self.name)
    
    def time_operating_valid(self):
         
        hora = time(0,0,0)
        if self.time_operating == hora:
            return '24:00:00'

        return self.time_operating


    def time_operating_seconds(self):
        t = self.time_operating
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        if seconds == 0:
            seconds = 86400
        # print(type(seconds)) 
        

        return seconds

    # TODO: buscar la forma de continuar la tabla de inventarios 

class Subproduct(ClassModel):
    name = models.CharField(max_length=50, unique=False, null=True, blank=True)
    img = models.ImageField(upload_to='sub product', null=True, blank=True)
    place = models.CharField(max_length=50, null=True, blank=True)
    measure = models.CharField(max_length=50, unique=False)
    pixel_size = models.CharField(max_length=50, unique=False, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Electronic(ClassModel):
    name = models.CharField(max_length=50, unique=False, null=True, blank=True)
    serie = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=50, unique=False, blank=True, null=True)
    pixel_size = models.CharField(max_length=50, unique=False, blank=True, null=True)
    measure = models.CharField(max_length=50, unique=False, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    sub_product = models.ForeignKey(Subproduct, on_delete=models.CASCADE)

# no utilizado 
class Electronic_detaill(ClassModel):

    name = models.CharField(max_length=50, unique=False, blank=True, null=True)
    detaill = models.CharField(max_length=300, unique=False, blank=True, null=True)





