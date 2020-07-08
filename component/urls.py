from django.urls import path
from .views import CategoryView, CategoryNew, CategoryEdit, category_delete, \
    LocationView, LocationNew, LocationEdit, location_delete, \
    ProductView, ProductNew, ProductEdit, product_delete, \
    sub_product_view, sub_product_new, sub_product_view_id, sub_product_delete, \
    CityView, CityNew, CityEdit, city_delete, \
    electronic_view, electronic_new, electronic_view_id, electronic_delete

urlpatterns = [
    # vistas para categorias
    path('categories/', CategoryView.as_view(), name='categories_list'),
    path('categories/new', CategoryNew.as_view(), name='categories_new'),
    path('categories/edit/<int:pk>',
         CategoryEdit.as_view(), name='categories_edit'),
    path('categories/delete/<int:id>', category_delete, name='categories_delete'),

    # vistas para locaciones
    path('locations/', LocationView.as_view(), name='locations_list'),
    path('locations/new', LocationNew.as_view(), name='locations_new'),
    path('locations/edit/<int:pk>', LocationEdit.as_view(), name='locations_edit'),
    path('locations/delete/<int:id>', location_delete, name='locations_delete'),

    # vistas para Productos
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/new', ProductNew.as_view(), name='product_new'),
    path('products/edit/<int:pk>', ProductEdit.as_view(), name='product_edit'),
    path('products/delete/<int:id>', product_delete, name='product_delete'),


    # vistas para sub_productos

    path('sub_product/view/<int:id>', sub_product_view, name='sub_product'),
    path('sub_product_id/view/<int:id>',
         sub_product_view_id, name='sub_product_id'),
    path('sub_product/new/<int:id>', sub_product_new, name='sub_product_new'),
    path('sub_product/delete/<int:id>',
         sub_product_delete, name='sub_product_delete'),

    # vistas para ciudad
    path('city/', CityView.as_view(), name='city_list'),
    path('city/new', CityNew.as_view(), name='city_new'),
    path('city/edit/<int:pk>',
         CityEdit.as_view(), name='city_edit'),
    path('city/delete/<int:id>', city_delete, name='city_delete'),



    # vistas para asignar electronicos a subproductos
    path('electronic/view/<int:id>', electronic_view, name='electronic'),
    path('electronic/new/<int:id>', electronic_new, name='electronic_new'),
    path('electronic_id/view/<int:id>', electronic_view_id, name='electronic_id'), 
    path('electronic/delete/<int:id>', electronic_delete, name='electronic_delete'),


]
