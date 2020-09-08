from django.db import models
from bases.models import ClassModel

from component.models import Product

from datetime import datetime

# modelo para clientes

class Client(ClassModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    img = models.ImageField(upload_to='clients', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)
# ordenes de pautaa
class Contract(ClassModel):
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    auspice = models.BooleanField(default=False)

    def __str__(self):
        
        return '{}, {} desde el {} al {}'.format(self.client.name, self.description, self.start_date   ,self.end_date)

    
        

# orden por cada producto

class Order(ClassModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass_contract = models.IntegerField(default=0)
    porcentage_contract = models.FloatField(default=0)
    description = models.CharField(max_length=150, null=True, blank=True)
    

    def __str__(self):
        return '{}'.format(self.description)

# url de respaldo 
class Respaldo(ClassModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    month_year = models.CharField(max_length=50, null=False, blank=False)
    year = models.ImageField(null=False, blank=False)
    url = models.CharField(max_length=500, null=False, blank=False)
    description = models.CharField(max_length=150, null=True, blank=True)


    