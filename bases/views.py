from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.views import generic

from sales.models import Contract, Order
from component.models import Product
from maintenance.models import Maintenance

from django.db.models import Sum, Count

# Create your views here.

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'bases:login'
    raise_exception = False
    redirect_field_name = 'redirecto_to'

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


@login_required(login_url='/login/')
def home(request):
    template_name = 'bases/home.html'
    contexto= {}

    products = Product.objects.filter(state=True).all()
    contracts_money = Contract.objects.filter(state=True, auspice=False).count()
    contract_auspice = Contract.objects.filter(state=True, auspice=True).count()
    general_porcentaje = Order.objects.values('product').annotate(total=Sum('porcentage_contract')).order_by('total').filter(state=True)
    count_maintenance = Maintenance.objects.values('product').annotate(total=Count('product_id')).order_by('total')
    # print("======+++======")
    # print(count_maintenance)
    # print(general_porcentaje)
    list_count_maintenance = []
    aux = 0
    for item2 in products:
        
        if aux < 3:
            for item in count_maintenance:
                if item['product'] == item2.id:
                    objeto = {}
                    objeto['product'] = item2
                    objeto['total'] = item['total']
                    list_count_maintenance.append(objeto)
                    aux = aux + 1

    lista_por = []
    for item in general_porcentaje:
        objeto_order = {}
        objeto_order["product"] = str(item['product'])
        objeto_order["total"] = str(item['total'])
           
            # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
        lista_por.append(objeto_order)

    contexto = {'contract_money':contracts_money,'contract_auspice':contract_auspice,'obj2':lista_por,'obj3':products,'count_maintenance':list_count_maintenance}
    return render(request, template_name, contexto)

# class Home(LoginRequiredMixin  ,generic.ListView):
#     model = Contract
#     template_name = 'bases/home.html' 
#     context_object_name = 'obj'
#     queryset = Contract.objects.count()
#     login_url = 'bases:login'

class HomesinPrivilegios(generic.TemplateView):
    template_name="bases/error_400.html"