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



from bases.views import SinPrivilegios

from component.models import Product
from sales.models import Contract, Order, Respaldo
from content.models import Video, Playlist, Drive_urls


import math

import datetime






@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def products_list(request):
    template_name = 'display/products_list.html'
    contexto = {}
    products = Product.objects.filter(state=True).all()

    if not products:
        return HttpResponse('No se encontraron registros')

    if request.method == 'GET':
        contexto = {'obj': products}

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def products_client(request, id):
    template_name = 'display/products_clients.html'
    contexto = {}
    product = Product.objects.filter(pk=id).first()
    order = Order.objects.filter(state=True, product=id).all()

    product_id = product.id
    playlist = Playlist.objects.filter(product=product_id).last()
    

    if not order:
        return HttpResponse('No se encontraron registros')

    if request.method == 'GET':
        contexto = {'obj': order, 'product':product, 'playlist':playlist}

    

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def video_list(request, id):
    template_name = 'display/video_list.html'
    contexto = {}
    
    order = Order.objects.get(id=id)
    video = Video.objects.filter(contract=order.contract.id, state=True).all()

    if not video:
        contexto = {'obj':''}

    if request.method == 'GET':
        contexto = {'obj':video, 'order':order }

    

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def clients_list(request):
    template_name = 'display/clients_list.html'
    contexto = {}
    contract = Contract.objects.filter(state=True).all()
    list_contract = []
    for item in contract:
        objeto = {}
        urls = Respaldo.objects.filter(contract_id=item.id).order_by('-year')
        objeto['id'] = item.id
        objeto['client'] = item.client
        objeto['description'] = item.description
        objeto['auspice'] = item.auspice
        objeto['start_date'] = item.start_date
        objeto['end_date'] = item.end_date
        objeto['urls'] = urls
        list_contract.append(objeto)
    respaldo = Respaldo.objects.all()
    if not contract:
        contexto = {'obj':''}

    if request.method == 'GET':
        contexto = {'obj':list_contract, 'respaldo':respaldo}

    

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def client_order(request, id):
    template_name = 'display/client_order.html'
    contexto = {}
    contract = Contract.objects.get(pk=id)
    order = Order.objects.filter(state=True, contract=id).all()

    # product_id = product.id
    # playlist = Playlist.objects.filter(product=product_id).last()
    

    if not order:
        contexto = {'obj':'' }

    if request.method == 'GET':
        contexto = {'obj': order, 'contract':contract}

    

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
# @permission_required('display.view_display', login_url='bases:sin_privilegios')
def drive_list(request):
    template_name = 'display/drive_list.html'
    contexto = {}
    drive = Drive_urls.objects.filter(state=True).all()
    # list_contract = [] 
    # for item in contract:
    #     objeto = {}
    #     urls = Respaldo.objects.filter(contract_id=item.id).order_by('-year')
    #     objeto['id'] = item.id
    #     objeto['client'] = item.client
    #     objeto['description'] = item.description
    #     objeto['auspice'] = item.auspice
    #     objeto['start_date'] = item.start_date
    #     objeto['end_date'] = item.end_date
    #     objeto['urls'] = urls
    #     list_contract.append(objeto)
    # respaldo = Respaldo.objects.all()
    if not drive:
        contexto = {'obj':''}

    if request.method == 'GET':
        contexto = {'obj':drive}

    

    return render(request, template_name, contexto)