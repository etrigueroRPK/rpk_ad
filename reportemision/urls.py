from django.urls import path
from .views import  report_client, report_client_all

urlpatterns = [
    # vistas para ventas
    path('report_client/',report_client, name='report_client'),

    path('report_client/<int:id>',report_client_all, name='report_client_all'),

    # path('report_playlist_xls/<int:id>',report_playlist_xls, name='report_playlist_xls'),

    
    
]