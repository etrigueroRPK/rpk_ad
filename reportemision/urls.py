from django.urls import path
from .views import  report_client, report_client_all, order_report_list, order_report_print, \
    report_client_generate, report_generate_save, report_client_view, \
    report_client_xls, report_client_day_view, report_day_delete

urlpatterns = [
    # vistas para reportes
    path('report_client/',report_client, name='report_client'),

    path('report_client/<int:id>',report_client_all, name='report_client_all'),

    path('order_report/<int:id>', order_report_list, name='order_report_list'),


    path('order_report_print/<int:id>', order_report_print, name='order_report_print'),

    # path('report_playlist_xls/<int:id>',report_playlist_xls, name='report_playlist_xls'),
    # ruta
    path('report_client_generate/<int:id>',report_client_generate, name='report_client_generate'),
    path('report_client_view/<int:id>',report_client_view, name='report_client_view'),
    
    path('report_client_day/view/<int:order_id>/<int:video_id>/<int:playlist_id>', report_client_day_view, name='report_client_day_view'),
    
    
    # ajax
    path('report_day/delete/<int:id>', report_day_delete, name='report_day_delete'),


    path('report_client_xls/<int:id>/<slug:month>/<int:order_id>',report_client_xls, name='report_client_xls'),
    path('report_generate_save/',report_generate_save, name='report_generate_save'),
]