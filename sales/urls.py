from django.urls import path
from .views import  ClientView, ClientNew, ClientEdit, client_delete

urlpatterns = [
    # vistas para ventas
    path('client/',ClientView.as_view(), name='client_list'),
    path('client/new',ClientNew.as_view(), name='client_new'),
    path('client/edit/<int:pk>',ClientEdit.as_view(), name='client_edit'),
    path('client/delete/<int:id>',client_delete, name='client_delete'),



]