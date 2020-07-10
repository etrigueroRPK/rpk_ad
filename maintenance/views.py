from django.shortcuts import render, redirect

# Create your views here.
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

from component.models import Product, Subproduct, Electronic
from .models import Maintenance

import math

from datetime import datetime


@login_required(login_url='/login/')
@permission_required('maintenance.view_maintenance', login_url='bases:sin_privilegios')
def maintenance_list(request):
    template_name = 'maintenance/maintenance_list.html'
    contexto = {}
    obj = Maintenance.objects.filter(state=True).all()

    if not obj:
        contexto = {'obj': ''}

    if request.method == 'GET':
        contexto = {'obj': obj}

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('maintenance.view_maintenance', login_url='bases:sin_privilegios')
def maintenance_new(request):
    template_name = 'maintenance/maintenance_form.html'
    contexto = {}
    obj = Maintenance.objects.filter(state=True).all()
    products = Product.objects.filter(state=True).all()

    if not obj:
        contexto = {'obj': ''}

    if request.method == 'GET':
        contexto = {'obj': obj, 'products': products}

    if request.method == 'POST':
        # print(request.POST)
        created_date_str = request.POST.get('created_date')
        id_product = request.POST.get('product')
        subproduct = request.POST.get('subproduct')
        electronic = request.POST.get('electronic')
        collaboration = request.POST.get('collaboration')
        work_done = request.POST.get('work_done')
        conclusions = request.POST.get('conclusions')

        # datetime_str = '2016-10-03T19:00:00.999Z'

        created_date = datetime.strptime(created_date_str, "%d/%m/%Y %H:%M:%S")

        # created_date = created_date_str
        print(type(created_date))
        print(created_date)
        if subproduct == '':
            subproduct = 0
        if electronic == '':
            electronic = 0

        product = Product.objects.get(pk=id_product)

        maintenance = Maintenance
        maintenance = Maintenance(
            created_date=created_date,
            product=product,
            sub_product=subproduct,
            electronic=electronic,
            collaboration=collaboration,
            work_done=work_done,
            conclusions=conclusions,
            state=True,
            user_created=request.user

        )
        maintenance.save()

        return redirect("maintenance:maintenance_list")

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('maintenance.view_maintenance', login_url='bases:sin_privilegios')
def maintenance_edit(request, id):
    template_name = 'maintenance/maintenance_edit.html'
    contexto = {}
    obj = Maintenance.objects.get(pk=id)

    if not obj:
        contexto = {'obj': ''}

    if request.method == 'GET':
        product = obj.product
        # print(obj.sub_product)
        # print(obj.electronic)

        subproduct = Subproduct.objects.filter(id=obj.sub_product).first()
        electronic = Electronic.objects.filter(id=obj.electronic).first()
        contexto = {'obj': obj, 'product': product,
            'subproduct': subproduct, 'electronic': electronic}

    if request.method == 'POST':
        # print(request.POST)

        collaboration = request.POST.get('collaboration')
        work_done = request.POST.get('work_done')
        conclusions = request.POST.get('conclusions')

        obj.collaboration = collaboration
        obj.work_done = work_done
        obj.conclusions = conclusions
        obj.state = True
        obj.user_updated = request.user.id

        
        obj.save()

        return redirect("maintenance:maintenance_list")

    return render(request, template_name, contexto)


def subproducts_get(request, id):
    # usado por ajax
    contexto={}
    if request.method == 'GET':
        subproduct=Subproduct.objects.filter(product = id).all()



        subproduct_json=[]
        for item in subproduct:
            objeto_order={}
            objeto_order["id"]=item.id
            objeto_order["name"]=item.name
            objeto_order["place"]=item.place
            objeto_order["measure"]=item.measure
            subproduct_json.append(objeto_order)

        # TODO: ver la forma de enviar el nombre de la inagen

        contexto={'obj': 'OK', 'subproduct': subproduct_json}
        return HttpResponse(json.dumps(contexto), content_type = json)

def electronic_get(request, id):
    # usado por ajax
    contexto={}
    if request.method == 'GET':
        electronic=Electronic.objects.filter(sub_product = id).all()



        electronic_json=[]
        for item in electronic:
            objeto={}
            objeto["id"]=item.id
            objeto["name"]=item.name
            objeto["serie"]=item.serie
            objeto["measure"]=item.measure
            electronic_json.append(objeto)

        # TODO: ver la forma de enviar el nombre de la inagen

        contexto={'obj': 'OK', 'electronic': electronic_json}
        return HttpResponse(json.dumps(contexto), content_type = json)

def maintenance_delete(request, id):
    template_name = 'maintenance/maintenance_delete.html'
    contexto = {}
    obj = Maintenance.objects.get(pk=id)

    if not obj:
        return HttpResponse('no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        # cat.state = False
        obj.delete()
        # return redirect("maintenance:maintenance_list")
        contexto = {'obj': 'OK'}
        return HttpResponse('OK')

    return render(request, template_name, contexto)
