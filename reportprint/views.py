from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
import datetime

# from django.utils import simplejson

# from .models import Client, Contract, Order


# from .forms import ClientForm, ContractForm

from sales.models import Contract, Order




def report_contract(request,id):
    template_name = 'reportprint/report_contract.html'
    contexto = {}
    contract = Contract.objects.filter(pk=id).first()
    
    today = datetime.datetime.now()
    order = Order.objects.filter(contract=id)
    if not contract:
        return HttpResponse('el registro con id: ' + str(id) + ' no existe!!!')

    if request.method == 'GET':

        contexto = {'today': today, 'contract':contract, 'order':order }
        
    

    return render(request, template_name,contexto)
