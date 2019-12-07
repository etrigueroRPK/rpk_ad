from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

from .models import Client
from .forms import ClientForm

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


def client_delete(request,id):
    template_name='sales/client_delete.html'
    contexto={}
    cat = Client.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('cliente no existe' + str(id))
    
    if request.method=='GET':
        contexto={'obj':cat}

    if request.method=='POST':
        cat.state=False
        cat.save()
        contexto={'obj':'OK'}
        return HttpResponse('cliente Inactivo')

    return render(request,template_name,contexto)
