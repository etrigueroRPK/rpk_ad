from django.urls import path
from .views import  ContractList, ClientView, ClientNew, ClientEdit, client_delete, \
    ContractList,contract_view,  contract_create, contract_edit, contract_delete, \
    order_delete, order_new

urlpatterns = [
    # vistas para ventas
    path('client/',ClientView.as_view(), name='client_list'),
    path('client/new',ClientNew.as_view(), name='client_new'),
    path('client/edit/<int:pk>',ClientEdit.as_view(), name='client_edit'),
    path('client/delete/<int:id>',client_delete, name='client_delete'),

    path('contract/',ContractList.as_view(), name='contract_list'),
    path('contract/view/<int:id>',contract_view, name='contract_view'),
    path('contract/new/',contract_create, name='contract_new'),
    path('contract/edit/<int:id>',contract_edit, name='contract_edit'),
    path('contract/delete/<int:id>',contract_delete, name='contract_delete'),


    path('order/new',order_new, name='order_new'),
    path('order/delete/<int:id>',order_delete, name='order_delete'),
    
]