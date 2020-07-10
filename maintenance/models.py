from django.db import models

from bases.models import ClassModel

from component.models import Product
# Create your models here.
 

class Maintenance(ClassModel):
    
    created_date = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_product = models.IntegerField(blank=True, null=True)
    electronic = models.IntegerField(blank=True, null=True)
    collaboration = models.CharField(max_length=200, blank=True, null=True)
    work_done = models.TextField(max_length=1000, blank=True, null=True)
    conclusions = models.TextField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        
        return '{} {}'.format(self.product, self.created_date)