from django.urls import path
from .views import products_view, list_client, list_video

urlpatterns = [
    # vistas para categorias
    path('products_view/', products_view, name='products_view'),
    # path('categories/new', CategoryNew.as_view(), name='categories_new'),
    # path('categories/edit/<int:pk>',
    #      CategoryEdit.as_view(), name='categories_edit'),
    # ajax
    path('list_client/<int:id>', list_client, name='list_client'),
    path('list_video/<int:id>', list_video, name='list_video'),

]
