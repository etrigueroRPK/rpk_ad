from django.urls import path
from .views import  report_contract, report_playlist, report_playlist_xls

urlpatterns = [
    # vistas para ventas
    path('report_contract/<int:id>',report_contract, name='report_contract'),

    path('report_platlist/<int:id>',report_playlist, name='report_playlist'),

    path('report_playlist_xls/<int:id>',report_playlist_xls, name='report_playlist_xls'),

    
    
]