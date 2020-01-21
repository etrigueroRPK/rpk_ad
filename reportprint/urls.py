from django.urls import path
from .views import  report_contract

urlpatterns = [
    # vistas para ventas
    path('report_contract/',report_contract, name='report_contract'),
    
    
]