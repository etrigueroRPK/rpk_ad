from django.db import models

from bases.models import ClassModel
from sales.models import Contract, Order
from component.models import Product
# Create your models here.
 

# class report_client(ClassModel):

#     create_date = models.DateField(null=False, blank=False)
#     description = models.CharField(max_length=100, null=True, blank=True)
    
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    # def __str__(self):
        
    #     return '{}:{}'.format(self.name, self.duration)

    # def duration_all(self):
    #     duration = str(self.duration)
    #     return duration


# class Playlist(ClassModel):
#     create_date = models.DateField(null=False, blank=False)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return '{} del {} '.format(self.product, self.create_date)

# class Playlist_spot_detail(ClassModel):
#     repeat_count = models.IntegerField(null=False, blank=False)
#     time_total = models.IntegerField(null=False, blank=False)
#     porcentage = models.FloatField(null=False, blank=False)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

# class Playlist_client_detail(ClassModel):
#     time_total = models.IntegerField(null=False, blank=False)
#     pauta_loop = models.IntegerField(null=False, blank=False)
#     second_total = models.IntegerField(null=False, blank=False)
#     time_contract = models.IntegerField(null=False, blank=False)
#     time_bonification = models.IntegerField(null=False, blank=False)

#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)


# class Playlist_document(ClassModel):
#     order_list = models.IntegerField(null=False, blank=False)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)