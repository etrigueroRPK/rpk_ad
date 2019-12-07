from django.db import models
from bases.models import ClassModel

# modelo para clientes

class Client(ClassModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    img = models.ImageField(upload_to='clients')

    def __str__(self):
        return '{}'.format(self.name)
