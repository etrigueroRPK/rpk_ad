from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

# from django.utils import simplejson

# from .models import Client, Contract, Order


# from .forms import ClientForm, ContractForm

from component.models import Product




def report_contract(request):
    template_name = 'reportprint/report_contract.html'
    contexto = {}
    product = Product.objects.all()

    # if not cat:
    #     return HttpResponse('cliente no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': product}
        print('=============================================================')
        print(template_name)
    # if request.method == 'POST':
    #     cat.state = False
    #     cat.save()
    #     contexto = {'obj': 'OK'}
    #     return HttpResponse('cliente Inactivo')

    return render(request, 'reportprint/a.html',contexto)
