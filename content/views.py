from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# importacion pra la vista basada en funciones 
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.http import HttpResponse
import json

from .models import Video
from .forms import VideoForm

from bases.views import SinPrivilegios

# vistas para Categorias
# TODO: completar los privilegios de los usuarios para cada vista


class VideoView(SinPrivilegios,\
    generic.ListView):
    # este permision_required es nesesario para ver el tema de permisos a nivel de vista
    permission_required = 'content.view_video'
    model = Video
    template_name = 'content/video_view.html'
    context_object_name = 'obj'
    


class VideoNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Video
    template_name = 'content/video_form.html'
    context_object_name = 'obj'
    form_class = VideoForm
    success_url = reverse_lazy('content:videos_list')
    login_url = 'bases:login'
    success_message = "Creado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)


class VideoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Video
    template_name = 'content/video_form.html'
    context_object_name = 'obj'
    form_class = VideoForm
    success_url = reverse_lazy('content:videos_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"


    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('content.delete_video', login_url='bases:sin_privilegios')
def video_delete(request, id):
    template_name = 'content/video_delete.html'
    contexto = {}
    cat = Video.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Video no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        cat.state = False
        cat.save()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Video  Inactivada')

    return render(request, template_name, contexto)
