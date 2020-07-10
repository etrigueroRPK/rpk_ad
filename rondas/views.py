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

from django.db.models import Count
from django.contrib.auth.models import User






import math

from datetime import datetime

# vistas para Categorias
# TODO: completar los privilegios de los usuarios para cada vista


class RondasView(SinPrivilegios,
                generic.ListView):
    # este permision_required es nesesario para ver el tema de permisos a nivel de vista
    permission_required = 'rondas.view_inplace'
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


@login_required(login_url='/login/')
@permission_required('rondas.view_inplace', login_url='bases:sin_privilegios')
def inplace_view(request, id):
    template_name = 'rondas/inplace_view.html'
    contexto = {}
    cat = Inplace.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Registro no encontrado' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        # cat.state = False
        cat.update()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Registro  visto')

    return render(request, template_name, contexto)

@login_required(login_url='/login/')
@permission_required('rondas.delete_inplace', login_url='bases:sin_privilegios')
def inplace_delete(request, id):
    template_name = 'rondas/inplace_delete.html'
    contexto = {}
    cat = Inplace.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Registro no encontrado' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        # cat.state = False
        cat.delete()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Registro  eliminado')

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('rondas.view_inplace', login_url='bases:sin_privilegios')
def routes_view(request):
    template_name = 'rondas/routes_view.html'
    contexto = {}
    obj = Inplace.objects.values('user_created').annotate(dcount=Count('user_created'))
    users = User.objects.all()
    
   
       
    if not obj:
        return HttpResponse('Registro no encontrado' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'users':users}

    if request.method == 'POST':
        
        cdate = request.POST.get('created_date') 
        user_id = request.POST.get('user') 
        # print(cdate)
        # print(user_id)

        route = Inplace.objects.filter(datetime_insitu__startswith=cdate, user_created=user_id).all().order_by('datetime_insitu')
        table_origin = []
        table_destination = []
        table_route = []
        # print(route)
        for x in range(len(route) - 1):
            table_origin.append(route[x])
            
        for x in range(1, len(route) ):
            table_destination.append(route[x])
        
        for y in range(len(table_origin)):
            objeto = {}
            objeto['origin'] = table_origin[y].product
            objeto['origin_date'] = table_origin[y].datetime_insitu
            objeto['destination'] = table_destination[y].product
            objeto['destination_date'] = table_destination[y].datetime_insitu

            objeto['diferencia'] = table_destination[y].datetime_insitu - table_origin[y].datetime_insitu
            # print(table_destination[y].datetime_insitu - table_origin[y].datetime_insitu)
            table_route.append(objeto)

        user = User.objects.get(pk=user_id)
        cdate_date = datetime.strptime(cdate, "%Y-%m-%d")

        contexto = {'obj': obj, 'users':users, 'table_route':table_route, 'user':user, 'cdate':cdate_date}
        # return HttpResponse('Registro  visto')

    return render(request, template_name, contexto)