from django.urls import path
from .views import reporte, report_mail_view

urlpatterns = [
    # vistas para categorias
    
    path('send', reporte, name='send'),
    path('report_mail_view', report_mail_view, name='report_mail_view'),

    

]