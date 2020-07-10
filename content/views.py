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

from .models import Video, Playlist, Playlist_client_detail, Playlist_spot_detail, Playlist_document
from .forms import VideoForm

from bases.views import SinPrivilegios

from component.models import Product
from sales.models import Contract, Order

import math

import datetime

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
@permission_required('content.disabled_video', login_url='bases:sin_privilegios')
def video_disabled(request, id):
    template_name = 'content/video_disabled.html'
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
        # cat.state = False
        cat.delete()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Video  borrado')

    return render(request, template_name, contexto)


# ==========================================================
# para manejar listas de reproduccion
# ==========================================================

@login_required(login_url='/login/')
@permission_required('content.delete_playlist', login_url='bases:sin_privilegios')
def playlist_delete(request, id):
    template_name = 'content/playlist_delete.html'
    contexto = {}
    cat = Playlist.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Playlist no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        # cat.state = False
        cat.delete()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Playlist  borrado')

    return render(request, template_name, contexto)



def playlist_list(request):
    contexto = {}
    template_name = 'content/playlist_list.html'
    if request.method == 'GET':
        playlist = Playlist.objects.all()
        contexto = {'obj': playlist}

    return render(request, template_name, contexto)


def playlist_view(request, id):
    contexto = {}
    template_name = 'content/playlist_list.html'
    if request.method == 'GET':
        playlist = Playlist.objects.filter(id=id).first()
        pl = list(map(list, playlist.clients_g))
        # pls = json.loads(pl)
        print(pl)
        print(type(pl))

    return render(request, template_name, contexto)


def playlist_generator(request):
    contexto = {}
    template_name = 'content/playlist_form.html'

    if request.method == 'GET':
        product = Product.objects.filter(state=1).all()
        today = datetime.datetime.now()
        contexto = {'obj': product, 'today': today}

    if request.method == 'POST':

        id_product = request.POST.get("id_product")

        order = Order.objects.filter(product_id=id_product, state=1).all().order_by('-contract__auspice')
        # print(order)
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

    if request.method == 'POST':

        product_id = request.POST.get('product')
        client_spot_list = request.POST.getlist('clientes_spots')

        product = Product.objects.filter(pk=product_id).get()
        time_operating = product.time_operating_valid()
        time_operating_second = convert_to_seconds(time_operating)
        lista_clientes_spot = []
        # se vuelve a generar la lista de clientes y spots con los que selecciono el cliente
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
        lista_info_spots = []
        lista_info_cliente = []
        lista_ordenada = []

        lista_nueva = complet_pass(lista_clientes_spot)
        lista_ordenada = ordenar_lista(lista_nueva)
        lista_info_spots = extraxt_data_spots(lista_nueva)
        lista_info_cliente = extract_data_client(lista_nueva)

        contexto = {'obj': 'OK', 'order': lista_ordenada,
                    'info_spot': lista_info_spots, 'info_client': lista_info_cliente}
        return HttpResponse(json.dumps(contexto), content_type=json)
    return HttpResponse('ok')



def playlist_order_2(request):
    contexto = {}

    if request.method == 'POST':

        product_id = request.POST.get('product')
        client_spot_list = request.POST.getlist('clientes_spots')

        product = Product.objects.filter(pk=product_id).get()
        time_operating = product.time_operating_valid()
        print('Time operation')
        print(time_operating)
        time_operating_second = convert_to_seconds(time_operating)
        lista_clientes_spot = []
        # se vuelve a generar la lista de clientes y spots con los que selecciono el cliente
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
        lista_info_spots = []
        lista_info_cliente = []
        lista_ordenada = []

        lista_nueva = complet_pass_2(lista_clientes_spot)
        lista_ordenada = ordenar_lista(lista_nueva)
        lista_info_spots = extraxt_data_spots(lista_nueva)
        lista_info_cliente = extract_data_client(lista_nueva)

        contexto = {'obj': 'OK', 'order': lista_ordenada,
                    'info_spot': lista_info_spots, 'info_client': lista_info_cliente}
        return HttpResponse(json.dumps(contexto), content_type=json)
    return HttpResponse('ok')


def playlist_new(request):

    if request.method == 'POST':
        product_id = request.POST.get('product')
        create_date = request.POST.get('create_date')
        clientes_g = request.POST.getlist('clientes_g')
        spots_g = request.POST.getlist('spots_g')
        playlist_g = request.POST.getlist('playlist_g')
        print(clientes_g)

        print(spots_g)
        print(playlist_g)

        product = Product.objects.get(pk=product_id)

        playlist = Playlist(
            create_date=create_date,
            product=product,
            state=True,
            user_created=request.user
        )
        playlist.save()

        for item in clientes_g:
            time_total = item.split('|')[0]
            pauta_loop = item.split('|')[1]
            second_total = item.split('|')[2]
            time_contract = item.split('|')[3]
            time_bonification = item.split('|')[4]
            order_id = item.split('|')[5]
            order = Order.objects.get(pk=order_id)
            # print(item.split('|'))

            playlist_client_detail = Playlist_client_detail(
                time_total=time_total,
                pauta_loop=pauta_loop,
                second_total=second_total,
                time_contract=time_contract,
                time_bonification=time_bonification,
                order=order,
                user_created=request.user,
                playlist=playlist
            )
            playlist_client_detail.save()

        for item in spots_g:
            repeat_count = item.split('|')[0]
            time_total = item.split('|')[1]
            porcentage = item.split('|')[2]
            video_id = item.split('|')[3]
            order_id = item.split('|')[4]
            video = Video.objects.get(pk=video_id)
            order = Order.objects.get(pk=order_id)
            playlist_spot_detail = Playlist_spot_detail(
                repeat_count=repeat_count,
                time_total=time_total,
                porcentage=porcentage,
                video=video,
                order=order,
                playlist=playlist,
                user_created=request.user
            )
            playlist_spot_detail.save()

        for item in playlist_g:
            order_list = item.split('|')[0]
            video_id = item.split('|')[1]
            video = Video.objects.get(pk=video_id)
            playlist_document = Playlist_document(
                order_list=order_list,
                video=video,
                playlist=playlist,
                user_created=request.user
            )
            playlist_document.save()

        return HttpResponse('ok')

    return HttpResponse('ok')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# =============================================================================================
# funciones que ayudan al ordenamineto de las listas finales
# TODO: MEJORAR y/o llevar estos metodos a otro archivo de manera que sea accesible para otras vista.
###############################################################################################



def ordenar_lista(listas):
    aux_listas = listas
    lista_contada = []
    aux_agregado = []
    nueva_lista_ordenada = []
    for item in listas:
        if(not item['order_id'] in aux_agregado):
            aux_agregado.append(item['order_id'])
            aux_count = contar_apariciones_order_id(
                aux_listas, item['order_id'])
            if aux_count >= 1:
                new_item = {}
                new_item['order_id'] = item['order_id']
                new_item['client'] = item['client']
                new_item['apariciones'] = aux_count
                lista_contada.append(new_item)

    lista_contada.sort(key=lambda item: item['apariciones'], reverse=True)

    # retorna la lista como esta debido a que ya esta ordenada
    if lista_contada[0]['apariciones'] == 1:
        return listas

    # inicializa la nueva lista con los valores mas altos
    for item4 in listas:
        if lista_contada[0]['order_id'] == item4['order_id']:
            nueva_lista_ordenada.append(item4)

    for x in range(1, len(lista_contada)):

        lista_aux = []
        for item in listas:
            if lista_contada[x]['order_id'] == item['order_id']:

                lista_aux.append(item)
                # print(lista_aux)

        nueva_lista_ordenada = intercalar_listas(
            nueva_lista_ordenada, lista_aux)

    return nueva_lista_ordenada

# intercala los spot realizar mas opciones intercalamiento


def intercalar_listas(lista1, lista2):
    r = round(len(lista1) / len(lista2))
    aux = []
    posicion = 0
    for item in lista2:
        aux = lista1
        aux.insert(posicion, item)
        posicion = posicion + r + 1
    # print('============================================================')
    # for item in aux:
    #     print(item)
    # print('============================================================')
    return aux


def contar_apariciones_order_id(listas, order_id):
    sum = 0
    for item in listas:
        if item['order_id'] == order_id:
            sum = sum + 1

    return sum


def extract_data_client(listas):
    lista_nueva = []
    aux_agregado = []
    aux = listas
    time_total = 0
    for item in listas:
        time_total = time_total + convert_to_seconds(item['duration'])

    # print(time_total)
    for item in listas:
        if(not item['order_id'] in aux_agregado):
            aux_agregado.append(item['order_id'])
            tiempo_total = count_time_client(aux, item['order_id'])
            if tiempo_total > 1:
                order_id = item['order_id']
                order = Order.objects.filter(pk=order_id).get()
                # print(order.pass_contract)
                loop_pauta = int(item['time_operating']) / time_total
                print(loop_pauta)
                time_contract = int(order.pass_contract) * 30
                new_item = {}
                new_item['order_id'] = item['order_id']
                new_item['client'] = item['client']
                new_item['time_total_pauta'] = tiempo_total
                new_item['loop_pauta'] = round(loop_pauta, 2)
                new_item['time_total_all'] = round((tiempo_total * loop_pauta))
                new_item['time_contract'] = time_contract
                new_item['time_bonification'] = round((tiempo_total * loop_pauta) - time_contract)
                lista_nueva.append(new_item)

    # for  item2 in lista_nueva:
    #     print(item2)

    return lista_nueva

# contar el tiempo total de los spot por cliente


def count_time_client(listas, client):
    suma = 0

    for item in listas:
        if item['order_id'] == client:
            suma = suma + int(convert_to_seconds(item['duration']))

    return suma

# extrae los totales de los spots y devuelve


def extraxt_data_spots(listas):

    lista_nueva = []
    items_founs = []

    # cuenta la cantidad de apariciones en la lista
    for item in listas:
        if(not item in items_founs):
            items_founs.append(item)
            count = listas.count(item)
            if count >= 1:
                new_item = {}
                new_item['order_id'] = item['order_id']
                new_item['client'] = item['client']
                new_item['count_repeat'] = count
                new_item['video_id'] = item['video_id']
                new_item['video_name'] = item['video_name']
                new_item['duration'] = convert_to_seconds(item['duration'])
                new_item['time_total'] = int(
                    convert_to_seconds(item['duration'])) * count
                new_item['pass'] = item['pass']
                new_item['porcentage'] = item['porcentage']
                new_item['time_operating'] = item['time_operating']
                lista_nueva.append(new_item)

        # objeto['client'] = aux

    return lista_nueva

# # cuenta aparicion de clientes
# def count_client(listas, client):
#     count = 0
#     for item in listas:
#         if item['client'] == client:
#             count = count + 1

#     return count
# completa los pases segun el porcentaje de contrato general 
def complet_pass_2(listas):


    lista_nueva = []

    for lista in listas:

        order_id = lista['order_id']
        count = cout_spot(listas, order_id)
        lista["num_spot"] = count

    suma_tem = 0
    bandera = True
    lista_nueva = listas

    # completa los spots de acuerdo a los porcentages que figuran en su espacio de contratado

    for item in listas:

        suma_tem = time_all(lista_nueva)
        bandera = True
        while bandera:
            # print(suma_tem)
            duracion_seg = count_client_time(lista_nueva, item['order_id'])
            # print(duracion_seg)
            porc = item['porcentage']
            # print(item["video_name"])
            # print(porc)
            porc_aux = (duracion_seg * 100) / suma_tem
            # print(porc_aux)
            if porc >= porc_aux:
                lista_nueva.append(item)
            else:
                bandera = False

   

    # for item in lista_nueva:
    #     print(item)

    return lista_nueva

# completa los pases dividiendo el porcentaje contratado a cada spot 
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

    # completa los spots de acuerdo a los porcentages que figuran en su espacio de contratado

    for item in listas:

        suma_tem = time_all(lista_nueva)
        bandera = True
        while bandera:
            # print(suma_tem)
            duracion_seg = count_spot_time(lista_nueva, item['video_id'])
            # print(duracion_seg)
            porc = item['porcentage']
            # print(item["video_name"])
            # print(porc)
            porc_aux = (duracion_seg * 100) / suma_tem
            # print(porc_aux)
            if porc >= porc_aux:
                lista_nueva.append(item)
            else:
                bandera = False

    lista_nueva2 = lista_nueva
    for item in lista_nueva:

        suma_tem = time_all(lista_nueva)
        bandera = True
        while bandera:
            # print(suma_tem)
            duracion_seg = count_spot_time(lista_nueva2, item['video_id'])
            # print(duracion_seg)
            porc = item['porcentage']
            # print(item["video_name"])
            # print(porc)
            porc_aux = (duracion_seg * 100) / suma_tem
            # print(porc_aux)
            if porc >= porc_aux:
                lista_nueva2.append(item)
            else:
                bandera = False

    # for item in lista_nueva2:
        # print(item)
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

# devuelve el tiempo de aparacion de una order de id 
def count_client_time(listas, order_id):
    suma = 0
    for item in listas:
        if item['order_id'] == order_id:
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
            num = num+1

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
