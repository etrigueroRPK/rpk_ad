from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

from .models import Category, Location
from .forms import CategoryForm, LocationForm

# Create your views here.

# vistas para Categorias 

class CategoryView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'component/category_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


class CategoryNew(LoginRequiredMixin, generic.CreateView):
    model = Category
    template_name = 'component/category_form.html'
    context_object_name = 'obj'
    form_class = CategoryForm
    success_url = reverse_lazy('component:categories_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        
        return super().form_valid(form)

class CategoryEdit(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'component/category_form.html'
    context_object_name = 'obj'
    form_class = CategoryForm
    success_url = reverse_lazy('component:categories_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id
        
        return super().form_valid(form)


def category_delete(request,id):
    template_name='component/category_delete.html'
    contexto={}
    cat = Category.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Categoria no existe' + str(id))
    
    if request.method=='GET':
        contexto={'obj':cat}

    if request.method=='POST':
        cat.state=False
        cat.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivo')

    return render(request,template_name,contexto)

# =======================================
# Visatas para Locaciones

class LocationView(LoginRequiredMixin, generic.ListView):
    model = Location
    template_name = 'component/location_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class LocationNew(LoginRequiredMixin, generic.CreateView):
    model = Location
    template_name = 'component/location_form.html'
    context_object_name = 'obj'
    form_class = LocationForm
    success_url = reverse_lazy('component:locations_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user
        
        return super().form_valid(form)