from django.db import models

from bases.models import ClassModel

from component.models import Product
# Create your models here.
 

class Inplace(ClassModel):
    
    datetime_insitu = models.DateTimeField()
    img = models.ImageField(upload_to='rondas')
    description = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100, null=False, blank=False)
    longitude = models.CharField(max_length=100, null=False, blank=False)

    

    def __str__(self):
        
        return '{}'.format(self.datetime_insitu)

    
