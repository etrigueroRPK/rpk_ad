from django.urls import path
from .views import VideoView, VideoNew, VideoEdit, VideoForm, video_delete, \
    playlist_list, playlist_generator, playlist_order, playlist_new, playlist_view

urlpatterns = [
    # vistas para categorias
    path('videos/', VideoView.as_view(), name='videos_list'),
    path('videos/new', VideoNew.as_view(), name='video_new'),
    path('videos/edit/<int:pk>',
         VideoEdit.as_view(), name='video_edit'),
    path('videos/delete/<int:id>', video_delete, name='video_delete'),


    # rutas para videos
    path('playlist/', playlist_list, name='playlist_list'),
    path('playlist/generator', playlist_generator, name='playlist_generator'),
    path('playlist/contract_list/', playlist_generator, name='playlist_contract_list'),

    path('playlist/generator/order/', playlist_order, name='playlist_order'),
    path('playlist/new', playlist_new, name='playlist_new'),
    path('playlist/view/<int:id>', playlist_view, name='playlist_view'),

    



]