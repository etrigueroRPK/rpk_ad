from django.urls import path
from .views import CategoryView, CategoryNew, CategoryEdit, LocationView, LocationNew, category_delete

urlpatterns = [
    # vistas para categorias
    path('categories/',CategoryView.as_view(), name='categories_list'),
    path('categories/new',CategoryNew.as_view(), name='categories_new'),
    path('categories/edit/<int:pk>',CategoryEdit.as_view(), name='categories_edit'),
    path('categories/delete/<int:id>',category_delete, name='categories_delete'),

    # vistas para locaciones
    path('locations/',LocationView.as_view(), name='locations_list'),
    path('locations/new',LocationNew.as_view(), name='locations_new'),

]