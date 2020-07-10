from django.urls import path
from .views import maintenance_list, maintenance_new, subproducts_get, electronic_get, maintenance_edit, maintenance_delete


urlpatterns = [
    # vistas para registro de mantenimineto
    path('maintenance/', maintenance_list, name='maintenance_list'),
    path('maintenance/new', maintenance_new, name='maintenance_new'),
    path('maintenance/edit/<int:id>', maintenance_edit, name='maintenance_edit'),
    path('maintenance/delete/<int:id>', maintenance_delete, name='maintenance_delete'),


    path('subproduct_get/<int:id>', subproducts_get, name='subproduct_get'),
    path('electronic_get/<int:id>', electronic_get, name='electronic_get'),


    # path('ronda/view/<int:id>', inplace_view, name='ronda_view'),
    # path('videos/edit/<int:pk>',
    #      VideoEdit.as_view(), name='video_edit'),
    # path('videos/disabled/<int:id>', video_disabled, name='video_disabled'),

]