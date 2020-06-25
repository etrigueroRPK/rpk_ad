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

from .models import Inplace
from .forms import InplaceForm


from bases.views import SinPrivilegios




import math

import datetime

# vistas para Categorias
# TODO: completar los privilegios de los usuarios para cada vista


class RondasView(SinPrivilegios,
                generic.ListView):
    # este permision_required es nesesario para ver el tema de permisos a nivel de vista
    permission_required = 'rondas.view_video'
    model = Inplace
    template_name = 'rondas/rondas_view.html'
    context_object_name = 'obj'


class RondaNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Inplace
    template_name = 'rondas/inplace_form.html'
    context_object_name = 'obj'
    form_class = InplaceForm
    success_url = reverse_lazy('rondas:rondas_list')
    login_url = 'bases:login'
    success_message = "Creado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)