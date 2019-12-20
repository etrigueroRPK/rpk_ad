from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.views import generic

from sales.models import Contract, Order
from component.models import Product

from django.db.models import Sum

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

    products = Product.objects.all()
    contracts_count = Contract.objects.count()
    general_porcentaje = Order.objects.values('product').annotate(total=Sum('porcentage_contract')).order_by('total')

    lista_por = []
    for item in general_porcentaje:
        objeto_order = {}
        objeto_order["product"] = str(item['product'])
        objeto_order["total"] = str(item['total'])
           
            # Se deberia asignar al dictionary todos los atributos que desee enviar en el json.
        lista_por.append(objeto_order)

    contexto = {'obj':contracts_count,'obj2':lista_por,'obj3':products}
    return render(request, template_name, contexto)

# class Home(LoginRequiredMixin  ,generic.ListView):
#     model = Contract
#     template_name = 'bases/home.html' 
#     context_object_name = 'obj'
#     queryset = Contract.objects.count()
#     login_url = 'bases:login'

class HomesinPrivilegios(generic.TemplateView):
    template_name="bases/error_400.html"