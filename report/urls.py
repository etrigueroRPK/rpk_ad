from django.urls import path
from .views import reporte

urlpatterns = [
    # vistas para categorias
    
    path('report/send', reporte, name='send'),

    

]