from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
import datetime

from datetime import timedelta
import calendar

from openpyxl import Workbook
import openpyxl
import locale

# from django.utils import simplejson

# from .models import Client, Contract, Order


# from .forms import ClientForm, ContractForm

from sales.models import Contract, Order
from reportemision.models import Document, Report_day
from content.models import Video
from content.models import Playlist, Playlist_client_detail, Playlist_spot_detail, Playlist_document


