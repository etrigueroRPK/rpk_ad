from django.urls import path
from .views import VideoView, VideoNew, VideoEdit, VideoForm, video_delete

urlpatterns = [
    # vistas para categorias
    path('videos/', VideoView.as_view(), name='videos_list'),
    path('videos/new', VideoNew.as_view(), name='video_new'),
    path('videos/edit/<int:pk>',
         VideoEdit.as_view(), name='video_edit'),
    path('videos/delete/<int:id>', video_delete, name='video_delete'),

    



]