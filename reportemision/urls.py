from django.urls import path
from .views import  report_client, report_client_all, order_report_list, order_report_print

urlpatterns = [
    # vistas para ventas
    path('report_client/',report_client, name='report_client'),

    path('report_client/<int:id>',report_client_all, name='report_client_all'),

    path('order_report/<int:id>', order_report_list, name='order_report_list'),


    path('order_report_print/<int:id>', order_report_print, name='order_report_print'),

    # path('report_playlist_xls/<int:id>',report_playlist_xls, name='report_playlist_xls'),

    
    
]