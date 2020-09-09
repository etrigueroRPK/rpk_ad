from django.urls import path
from .views import products_list, products_client, video_list, \
    clients_list, client_order, drive_list

urlpatterns = [
   
    path('display/products', products_list, name='products_list'),
    path('display/products_client/<int:id>', products_client, name='products_client'),

    path('display/video_list/<int:id>', video_list, name='video_list'),

    path('display/clients', clients_list, name='clients_list'),
    path('display/client_order/<int:id>', client_order, name='client_order'),

    path('display/drive', drive_list, name='drive_list'),




    # path('videos/edit/<int:pk>',
    #      VideoEdit.as_view(), name='video_edit'),
    # path('videos/disabled/<int:id>', video_disabled, name='video_disabled'),
    # path('videos/delete/<int:id>', video_delete, name='video_delete'),



    



]