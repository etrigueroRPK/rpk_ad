from django.db import models
from bases.models import ClassModel

from component.models import Product

# modelo para clientes

class Client(ClassModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    img = models.ImageField(upload_to='clients')

    def __str__(self):
        return '{}'.format(self.name)

class Contract(ClassModel):
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}:{}'.format(self.client.name,self.start_date,self.end_date)

class Order(ClassModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass_contract = models.IntegerField(default=0)
    porcentage_contract = models.FloatField(default=0)
    description = models.CharField(max_length=150, null=True, blank=True)
    

    def __str__(self):
        return '{}'.format(self.description)