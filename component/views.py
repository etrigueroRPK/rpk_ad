from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.http import HttpResponse
import json

from .models import Category, Location, Product
from .forms import CategoryForm, LocationForm, ProductForm

# Create your views here.

# vistas para Categorias


class CategoryView(LoginRequiredMixin, PermissionRequiredMixin,\
    generic.ListView):
    permission_required = 'component.view_category'
    model = Category
    template_name = 'component/category_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


class CategoryNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Category
    template_name = 'component/category_form.html'
    context_object_name = 'obj'
    form_class = CategoryForm
    success_url = reverse_lazy('component:categories_list')
    login_url = 'bases:login'
    success_message = "Creado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)


class CategoryEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'component/category_form.html'
    context_object_name = 'obj'
    form_class = CategoryForm
    success_url = reverse_lazy('component:categories_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"


    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


def category_delete(request, id):
    template_name = 'component/category_delete.html'
    contexto = {}
    cat = Category.objects.filter(pk=id).first()

    if not cat:
        return HttpResponse('Categoria no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': cat}

    if request.method == 'POST':
        cat.state = False
        cat.save()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Categoria  Inactivada')

    return render(request, template_name, contexto)

# =======================================
# Visatas para Locaciones

# vista para listar las locaiones


class LocationView(LoginRequiredMixin, generic.ListView):
    model = Location
    template_name = 'component/location_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

# vista par acrear nuevas locaiones


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

# vista para editar locaiones


class LocationEdit(LoginRequiredMixin, generic.UpdateView):
    model = Location
    template_name = 'component/location_form.html'
    context_object_name = 'obj'
    form_class = LocationForm
    success_url = reverse_lazy('component:locations_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


def location_delete(request, id):
    template_name = 'component/location_delete.html'
    contexto = {}
    loc = Location.objects.filter(pk=id).first()

    if not loc:
        return HttpResponse('Locacion no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': loc}
       

    if request.method == 'POST':
        loc.state = False
        loc.save()
        contexto = {'obj': 'OK'}
        return HttpResponse('Location Inactivo')
    
    return render(request, template_name, contexto)

# ==================================
# vistas para productos
# ==================================

class ProductView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'component/product_view.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

# vista par acrear nuevas productos


class ProductNew(LoginRequiredMixin, generic.CreateView):
    model = Product
    template_name = 'component/product_form.html'
    context_object_name = 'obj'
    form_class = ProductForm
    success_url = reverse_lazy('component:product_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

# vista para editar productos


class ProductEdit(LoginRequiredMixin, generic.UpdateView):
    model = Product
    template_name = 'component/product_form.html'
    context_object_name = 'obj'
    form_class = ProductForm
    success_url = reverse_lazy('component:product_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


def product_delete(request, id):
    template_name = 'component/product_delete.html'
    contexto = {}
    loc = Product.objects.filter(pk=id).first()

    if not loc:
        return HttpResponse('Product no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': loc}
       

    if request.method == 'POST':
        loc.state = False
        loc.save()
        contexto = {'obj': 'OK'}
        return HttpResponse('Location Inactivo')
    
    return render(request, template_name, contexto)

