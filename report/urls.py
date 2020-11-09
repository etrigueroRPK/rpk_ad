from django.urls import path
from .views import reporte, report_mail_view, report_mail_video

urlpatterns = [
    # vistas para categorias
    
    path('send', reporte, name='send'),
    path('report_mail_view', report_mail_view, name='report_mail_view'),
    path('report_mail_video', report_mail_video, name='report_mail_video'),


    

]