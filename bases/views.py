from django.shortcuts import render


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
# Create your views here.

class Home(LoginRequiredMixin  ,generic.TemplateView):
    template_name = 'bases/home.html' 
    login_url = 'bases:login'

class HomesinPrivilegios(generic.TemplateView):
    teplate_name="bases/error_400.html"