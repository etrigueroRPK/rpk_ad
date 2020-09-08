from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
import datetime

from datetime import timedelta
import calendar

from openpyxl import Workbook
import openpyxl
import locale

# from django.utils import simplejson

# from .models import Client, Contract, Order


# from .forms import ClientForm, ContractForm

from sales.models import Contract, Order
from reportemision.models import Document, Report_day
from content.models import Video
from content.models import Playlist, Playlist_client_detail, Playlist_spot_detail, Playlist_document
from component.models import Product

def products_view(request):
    template_name = ''
    contexto = {}
    products = Product.objects.all()

    if request.method == 'GET':
        template_name = 'allviewcontract/product_view.html'
        contexto = {'obj':products}

    return render(request, template_name, contexto)

def list_client(request, id):
    
    if request.method == 'POST':
        order = Order.objects.filter(product_id=id).all()
        
        order_list = []
        for item in order:
            objeto = {}
            objeto['id'] = item.id
            objeto['client'] = item.contract.client.name + ' ' + item.contract.description
            objeto['start_date'] = str(item.contract.start_date)
            objeto['end_date'] = str(item.contract.end_date)
            objeto['contract_id'] = item.contract.id
            order_list.append(objeto)

        contexto = {'obj':'OK', 'order':order_list}
        return HttpResponse(json.dumps(contexto), content_type=json)
    
    return redirect('allviewcontract:products_view')

def list_video(request, id):
    
    if request.method == 'POST':
        order = Video.objects.filter(contract_id=id).all()
        
        order_list = []
        for item in order:
            objeto = {}
            objeto['id'] = str(item.id)
            objeto['name'] = item.name
            objeto['start_date'] = str(item.start_date)
            objeto['end_date'] = str(item.end_date)
            
            order_list.append(objeto)

        contexto = {'obj':'OK', 'order':order_list}
        return HttpResponse(json.dumps(contexto), content_type=json)
    
    return redirect('allviewcontract:products_view')