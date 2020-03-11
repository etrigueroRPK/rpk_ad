from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

# from django.utils import simplejson

from .models import Client, Contract, Order

from component.models import Product
from .forms import ClientForm, ContractForm


# Create your views here.

# vistas para Categorias

class ClientView(LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = 'sales/client_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


class ClientNew(LoginRequiredMixin, generic.CreateView):
    model = Client
    template_name = 'sales/client_form.html'
    context_object_name = 'obj'
    form_class = ClientForm
    success_url = reverse_lazy('sales:client_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)


class ClientEdit(LoginRequiredMixin, generic.UpdateView):
    model = Client
    template_name = 'sales/client_form.html'
    context_object_name = 'obj'
    form_class = ClientForm
    success_url = reverse_lazy('sales:client_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


def client_delete(request, id):
    template_name = 'sales/client_delete.html'
    contexto = {}
    cat = Client.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('cliente no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        cat.state = False
        cat.save()
        contexto = {'obj': 'OK'}
        return HttpResponse('cliente Inactivo')

    return render(request, template_name, contexto)


# ====================================================================
# vistas necesarias para crear orden de trabajo
# ====================================================================

class ContractList(LoginRequiredMixin, generic.ListView):
    model = Contract
    template_name = 'sales/contract_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


def contract_list(request):
    # usado por AJAX, cambiar a nombre de productos e incluso cambiar esta solicitud a component
    if request.method == 'GET':
        product = Product.objects.filter(state=True).all().order_by("category")
        lista_order_json = []
        for item in product:
            objeto = {}
            objeto["id"] = item.id
            objeto["category"] = item.category.name
            objeto["name"] = item.name
            objeto["location"] = item.location.name
            objeto["time_operation"] = str(item.time_operating_valid())
            # print(item.time_operating_valid())
            # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
            lista_order_json.append(objeto)
        # print(lista_order_json)

        contexto = {'obj': 'OK', 'product': lista_order_json}
        return HttpResponse(json.dumps(contexto), content_type=json)


def contract_view(request, id):
    template_name = 'sales/contract_view.html'
    contexto = {}

    contract = Contract.objects.filter(pk=id, state=True).first()
    order = Order.objects.filter(contract_id=id).all()
    print('============================================================')

    # print(order)

    print('============================================================')
    if not contract:
        return HttpResponse('no se pudieron encontrar datos')

    if request.method == 'GET':
        contexto = {'contract': contract, 'order': order}

    if request.method == 'POST':
        contexto = {'obj': 'OK'}
        return HttpResponse('no tienes por que enviar datos a esta ruta')

    return render(request, template_name, contexto)


def contract_create(request):
    template_name = 'sales/contract_form.html'
    contexto = {}
    client = Client.objects.filter(state=True).all()

    if not client:
        return HttpResponse('no se pudieron encontrar datos')

    if request.method == 'GET':
        contexto = {'obj': client}

    if request.method == 'POST':
        
        contract = Contract

        client_id = int(request.POST.get("client"))
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        check = request.POST.getlist("check[]")
        pass_contract = request.POST.get("pass_contract")
        porcentage_contract = request.POST.get("porcentage_contract")
        auspice = request.POST.get("auspice")
        aux = False
        if auspice == 'on':
            aux = True
        else:
            aux = False

        if start_date == "":
            start_date = None
        if end_date == "":
            end_date = None
        print(auspice)
        print(aux)
        client_c = Client.objects.get(pk=client_id)

        contract = Contract(
            client=client_c,
            start_date=start_date,
            end_date=end_date,
            state=1,
            user_created=request.user,
            auspice = aux
        )
        contract.save()
        pases = 0
        porcentaje = 0
        for item in check:
            pases = 0
            porcentaje = 0
            product = Product.objects.get(pk=item)
            time_operating = str(product.time_operating_valid())
            print(time_operating)
            if pass_contract:
                pases = pass_contract
                porcentaje = calculo_pases_porcentaje(
                    time_operating, pass_contract, None, 30)
            if porcentage_contract:
                pases = calculo_pases_porcentaje(
                    time_operating, None, porcentage_contract, 30)
                porcentaje = porcentage_contract

            order = Order(
                contract=contract,
                product=product,
                pass_contract=pases,
                porcentage_contract=porcentaje,
                user_created=request.user,
                state=1
            )

            order.save()
        
        
        return HttpResponse({'ok':'ok'})

        # print(check)

        # TODO: ver la forma de enviar mensaje de contrato creado creado con ventana popup
        # return redirect("sales:contract_list")

    return render(request, template_name, contexto)


def contract_edit(request, id):
    template_name = 'sales/contract_edit.html'
    contexto = {}
    contract = Contract.objects.get(id=id)
    product = Product.objects.filter(state=True).all()
    order = Order.objects.filter(contract_id=id).all()

    if not contract:
        messages.error(request, 'No se encontraron datos')
        return redirect("sales:contract_list")

    if request.method == 'GET':
        contexto = {'contract': contract, 'product': product, 'order': order}

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        estado = request.POST.get('estado')

        print(estado)

        if start_date == '':
            start_date = '0001-01-01'

        if end_date == '':
            end_date = '0001-01-01'

        if estado == 'on':
            estado = True
        else:
            estado = False
        contract.start_date = start_date
        contract.end_date = end_date
        contract.state = estado
        contract.user_updated = request.user.id

        contract.save()

        contract = Contract
        # contexto = {'obj': 'OK'}
        messages.success(request, 'Se modifico correctamente ;)')

        return redirect("sales:contract_list")

    return render(request, template_name, contexto)


def contract_delete(request, id):
    # TODO: Inabilitar las ordenes que se asocian al contrato para que no lo muestre en los reportes.
    template_name = 'sales/contract_delete.html'
    contexto = {}
    cat = Contract.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('orden no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        cat.state = False
        cat.user_updated = request.user.id
        cat.save()

        orders = Order.objects.filter(contract_id=id)
        for order in orders:
            aux = Order.objects.filter(pk=order.id).first()
            aux.state = False
            aux.user_updated = request.user.id
            aux.save()

        contexto = {'obj': 'OK'}
        return HttpResponse('orden se desactivo')

    return render(request, template_name, contexto)


# ====================================================================
# vistas necesarias para crear orden de trabajo
# ====================================================================


def order_delete(request, id):
    template_name = 'sales/contract_edit.html'
    contexto = {}
    print(id)
    id_ctt = Order.objects.get(id=int(id))
    # product = Product.objects.filter(state=True).all()
    order = Order.objects.filter(contract_id=id_ctt.contract.id).all()
    Order.objects.get(id=int(id)).delete()

    if request.method == 'POST':
        lista_order_json = []
        for item in order:
            objeto_order = {}
            objeto_order["id"] = item.id
            objeto_order["category"] = item.product.category.name
            objeto_order["product"] = item.product.name
            objeto_order["location"] = item.product.location.name
            objeto_order["pass"] = item.pass_contract
            objeto_order["porcentage"] = item.porcentage_contract
            objeto_order["description"] = item.description
            objeto_order["estado"] = item.state
            # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
            lista_order_json.append(objeto_order)
        # print(lista_order_json)

        contexto = {'obj': 'OK', 'order': lista_order_json}
        return HttpResponse(json.dumps(contexto), content_type=json)

    # return render(request, template_name, contexto)


def order_new(request):
    template_name = 'sales/contract_edit.html'
    contexto = {}

    if request.method == 'POST':
        id_contract = request.POST.get('id_contract')
        id_product = request.POST.get('id_product')
        pases = request.POST.get('pases')
        porcentaje = request.POST.get('porcentaje')
        desc = request.POST.get('description')

        order = Order
        order = Order(
            contract_id=id_contract,
            product_id=id_product,
            pass_contract=pases,
            porcentage_contract=porcentaje,
            description=desc,
            state=True,
            user_created=request.user
        )
        order.save()

        order = Order.objects.filter(contract_id=id_contract).all()

        lista_order_json = []
        for item in order:
            objeto_order = {}
            objeto_order["id"] = item.id
            objeto_order["category"] = item.product.category.name
            objeto_order["product"] = item.product.name
            objeto_order["location"] = item.product.location.name
            objeto_order["pass"] = item.pass_contract
            objeto_order["porcentage"] = item.porcentage_contract
            objeto_order["description"] = item.description
            objeto_order["estado"] = item.state
            # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
            lista_order_json.append(objeto_order)
        # print(lista_order_json)

        contexto = {'obj': "OK", 'order': lista_order_json}
        return HttpResponse(json.dumps(contexto), content_type=json)

    # return render(request, template_name, contexto)


def order_update(request, id):
    # solo actualiza el estado de la orden
    contexto = {}
    print('esta llegando ')
    if request.method == 'POST':
        # id_order = request.POST.get('id')

        order = Order.objects.filter(pk=id).first()
        if order.state == True:
            order.state = False
        else:
            order.state = True
        order.user_updated = request.user.id
        order.save()

        contexto = {'obj': "OK"}
        return HttpResponse(json.dumps(contexto), content_type=json)

    # return render(request, template_name, contexto)


def calculo_pases_porcentaje(time_operating, pases=None, porcentaje=None, time_spot=30):
    # calcula los pases o el porcentaje que tiene segun se envie pases o porcentaje en un la locacion
    # de acuerdo al tiempo de operaciones que se envia
    hora = time_operating.split(':')[0]
    minutos = time_operating.split(':')[1]
    total_segundos = (int(hora) * 60 * 60) + (int(minutos) * 60)
    # print(total_segundos)
    if pases:
        tiempo_contratado = time_spot * int(pases)
        # print(tiempo_contratado)
        porcentaje = (tiempo_contratado * 100) / total_segundos
        # print(porcentaje)
        return porcentaje

    if porcentaje:
        tiempo_contratado = (int(porcentaje) * total_segundos) / 100
        # print(tiempo_contratado)
        pases = tiempo_contratado / time_spot
        # print(pases)
        return pases
