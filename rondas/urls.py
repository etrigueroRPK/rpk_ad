from django.urls import path
from .views import RondasView, RondaNew, inplace_view, inplace_delete
# from .views import VideoView, VideoNew, VideoEdit, VideoForm, video_delete, video_disabled, \
    # playlist_list, playlist_generator, playlist_order, playlist_new, playlist_view, playlist_delete

urlpatterns = [
    # vistas para registro de rondas
    path('rondas/', RondasView.as_view(), name='rondas_list'),
    path('ronda/new', RondaNew.as_view(), name='ronda_new'),
    path('ronda/view/<int:id>', inplace_view, name='ronda_view'),

    # path('videos/edit/<int:pk>',
    #      VideoEdit.as_view(), name='video_edit'),
    # path('videos/disabled/<int:id>', video_disabled, name='video_disabled'),
    path('ronda/delete/<int:id>', inplace_delete, name='ronda_delete'),

]