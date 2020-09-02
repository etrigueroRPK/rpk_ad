from django.urls import path
from .views import  ContractList, ClientView, ClientNew, ClientEdit, client_delete, \
    ContractList,contract_view,  contract_create, contract_edit, contract_delete, contract_list, contract_disabled, \
    order_delete, order_new, order_update, \
    url_admin, url_new, url_id, url_delete

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

    path('contract/disabled/<int:id>',contract_disabled, name='contract_disabled'),

    path('contract/list/',contract_list, name='contract_list_ajax'),



    path('order/new',order_new, name='order_new'),
    path('order/delete/<int:id>',order_delete, name='order_delete'),
    path('order/update/<int:id>',order_update, name='order_update'),

    # urls para crear url ubicaciones de google drive en la cuenta de repositorio 

    path('url_admin/<int:id>',url_admin, name='url_admin'),
    # ajax
    path('url_new/<int:id>',url_new, name='url_new'),
    path('url_id/view/<int:id>',url_id, name='url_id'),
    path('url_delete/<int:id>',url_delete, name='url_delete'),


    
]