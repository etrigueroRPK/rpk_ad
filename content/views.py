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

from component.models import Product
from sales.models import Contract, Order

import math

# vistas para Categorias
# TODO: completar los privilegios de los usuarios para cada vista


class VideoView(SinPrivilegios,
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


# ==========================================================
# para manejar listas de reproduccion
# ==========================================================

def playlist_list(request):
    contexto = {}
    template_name = 'content/playlist_list.html'
    if request.method == 'GET':
        contexto = {}

    return render(request, template_name, contexto)


def playlist_generator(request):
    contexto = {}
    template_name = 'content/playlist_form.html'

    if request.method == 'GET':
        product = Product.objects.filter(state=1).all()
        contexto = {'obj': product}

    if request.method == 'POST':

        id_product = request.POST.get("id_product")

        order = Order.objects.filter(product_id=id_product, state=1).all()

        lista_order_json = []
        for item in order:
            # print(item.contract.id)
            videos = Video.objects.all().filter(contract_id=item.contract.id, state=True)
            for video in videos:

                # print(video)
                objeto_order = {}
                objeto_order["id"] = item.id
                objeto_order["pass"] = item.pass_contract
                objeto_order["porcentage"] = item.porcentage_contract
                objeto_order["contract"] = item.contract.client.name + " desde " + \
                    str(item.contract.start_date) + \
                    " al " + str(item.contract.end_date)
                objeto_order["description"] = item.description
                objeto_order["video_id"] = video.id
                objeto_order["video_name"] = video.name
                objeto_order["video_duration"] = video.duration_all()
                # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
                lista_order_json.append(objeto_order)

        # print(lista_order_json)

        contexto = {'obj': 'OK', 'order': lista_order_json}
        return HttpResponse(json.dumps(contexto), content_type=json)

        # return HttpResponse('ok')

    return render(request, template_name, contexto)


def playlist_order(request):
    contexto = {}
    template_name = ''

    if request.method == 'POST':

        product_id = request.POST.get('product')
        client_spot_list = request.POST.getlist('clientes_spots')

        product = Product.objects.filter(pk=product_id).get()
        time_operating = product.time_operating_valid()
        time_operating_second = convert_to_seconds(time_operating)
        lista_clientes_spot = []

        for item in client_spot_list:
            contract_id = item.split('-')[0]
            video_id = item.split('-')[1]
            
            
            order = Order.objects.filter(pk=contract_id).get()
            video = Video.objects.filter(pk=video_id).get()

        
            objeto = {}
            objeto["order_id"] = order.id
            objeto["client"] = order.contract.client.name
            objeto["pass"] = order.pass_contract
            objeto["porcentage"] = order.porcentage_contract
            objeto["video_id"] = video.id
            objeto["video_name"] = video.name
            objeto["duration"] = video.duration_all()
            objeto["time_operating"] = time_operating_second

            lista_clientes_spot.append(objeto)

        lista_nueva = []

        lista_nueva = complet_pass(lista_clientes_spot)

        # for lista in lista_clientes_spot:
        #     print(lista)
        
        
        
        # print(convert_to_seconds(time_operating))

        # print(time_operating)

        # print(product_id)
        # print(client_spot_list)
        contexto = {'obj': 'OK', 'order': lista_nueva}
        return HttpResponse(json.dumps(contexto), content_type=json)
    return HttpResponse('ok')


def complet_pass(listas):
    
    total_segundos = 0

    lista_nueva = []

    for lista in listas:
        
        order_id = lista['order_id']
        count = cout_spot(listas, order_id)
        lista["num_spot"] = count

    # a este punto se modifico las listas con pases divididos 
    # print(listas)

    for item in listas:
        pases = float(item['pass']) / float(item['num_spot'])
        porcentage = float(item['porcentage']) / float(item['num_spot'])

        duracion = convert_to_seconds(item['duration'])

        total_segundos = total_segundos + duracion

        item['pass'] = pases
        item['porcentage'] = porcentage
    
    suma_tem = 0
    bandera = True
    lista_nueva = listas

    for item in listas:

        suma_tem = time_all(lista_nueva)
        bandera = True
        while bandera:
            print(suma_tem)
            duracion_seg = count_spot_time(lista_nueva, item['video_id'])
            print(duracion_seg)
            porc = item['porcentage']
            print(porc)
            porc_aux = (duracion_seg * 100) / suma_tem
            print(porc_aux)
            if porc > porc_aux:
                lista_nueva.append(item)
            else:
                bandera = False    



    # for item in lista_nueva:
    #     print(item)
    # print(total_segundos)

    # print(listas)


    
    return lista_nueva

# devuelve el tiempo de aparacion de un spot
def count_spot_time(listas, video_id):
    suma = 0 
    for item in listas:
        if item['video_id'] == video_id:
            duration = convert_to_seconds(item['duration'])
            suma = suma + duration
    
    return suma 



# devuelve el tiempo total de la lista 
def time_all(listas):
    suma = 0

    for item in listas:
        duration = convert_to_seconds(item['duration'])
        suma = suma + duration
    
    return suma




# cuenta la aparicion de spots 
def cout_spot(list_clients, order_id):
    num = 0
    for item in list_clients:
        if item['order_id'] == order_id:
            num=num+1
    
        
    return num

# funcion que convienrte horas de opoeracion en segunsdos 
# TODO: ver la forma de optener este dato de manera general ya que esta en varias vistas 
def convert_to_seconds(horas):
    horas = str(horas)
    h = horas.split(':')[0]
    m = horas.split(':')[1]
    s = horas.split(':')[2]

    seconds = (int(h) * 60 * 60) + (int(m) * 60) + int(s)

    return seconds
