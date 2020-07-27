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

# from django.utils import simplejson

# from .models import Client, Contract, Order


# from .forms import ClientForm, ContractForm

from sales.models import Contract, Order
from .models import Document
from content.models import Video
from content.models import Playlist, Playlist_client_detail, Playlist_spot_detail, Playlist_document


def report_client(request):
    template_name = 'reportemision/contract_list.html'
    contexto = {}
    contract = Contract.objects.filter(state=True).all()

    # today = datetime.datetime.now()
    # order = Order.objects.filter(contract=id)
    if not contract:
        return HttpResponse('el registro con id: ' + str(id) + ' no existe!!!')

    if request.method == 'GET':

        contexto = {'obj': contract}

    return render(request, template_name, contexto)

def order_report_list(request, id):
    # id => contract_id
    template_name = 'reportemision/order_report_list.html'
    contexto = {}
    
    document = Document.objects.filter(contract=id).all()
    
    contexto = {'obj':document}
    return render(request, template_name, contexto)


def order_report_print(request, id):
    template_name = 'reportemision/order_report_print.html'
    contexto = {}

    document = Document.objects.get(pk=id)
   
    playlist_spot = Playlist_spot_detail.objects.filter(order_id=document.order.id, playlist_id=document.playlist_id).all()
    videos = []
    time_in_pauta_total = 0 
    repeat_in_pauta = 0
    videos_id = []
    for item in playlist_spot:
        objeto = {}
        video = Video.objects.get(pk=item.video_id)
        videos_id.append(video.id)
        objeto['name_video'] = video.name
        objeto['duration'] = video.duration_all
        objeto['duration_seconds'] = video.duration_seconds
        objeto['repeat_in_pauta'] = item.repeat_count
        objeto['time_in_pauta'] = item.time_total
        time_in_pauta_total = time_in_pauta_total + int(item.time_total) 
        repeat_in_pauta = repeat_in_pauta + int(item.repeat_count)
        videos.append(objeto)

    playlist = Playlist_document.objects.filter(playlist_id=document.playlist_id).all().order_by('order_list')
    playlist_client = []
    for item in playlist:
        objeto = {}
        objeto['orden_list'] = item.order_list
        if (not item.video.id in videos_id):
            objeto['name_video'] = 'Otro cliente'
            objeto['color'] = 0
        else:
            objeto['name_video'] = item.video.name
            objeto['color'] = 1
        objeto['duration'] = item.video.duration_all()
        playlist_client.append(objeto)

    for item in playlist_client:
        print(item)

    contexto = {'obj':document, 'videos':videos, 'time':time_in_pauta_total,'time2':repeat_in_pauta, 'playlist':playlist_client}

    return render(request,template_name,contexto)

def report_client_all(request, id):
    template_name = 'reportemision/contract_list.html'
    contexto = {}

    contract = Contract.objects.get(pk=id)
    order = Order.objects.filter(contract=id)

    report = []
    # print(contract)
    for i in order:
        order_id = i.id
        # print(i.id)
        playlist_client_detail = Playlist_client_detail.objects.filter(order=order_id).order_by('playlist__create_date')
        if playlist_client_detail:

            for j in playlist_client_detail:
                # print(j.order.id)
                playlist_spot_detail = Playlist_spot_detail.objects.filter(playlist=j.playlist.id, order=order_id)
                for k in playlist_spot_detail:
                    # print(k.video.name)
                    # se extrae informacion por videos de todos los contratos 
                    item = {}
                    item["id"] = str(order_id) + str(k.video.id) + str(j.playlist.product.id)
                    item["contract_id"] = contract.id
                    item["order_id"] = order_id
                    item["video_id"] = k.video.id
                    item["client"] = contract.client.name
                    item["start_date"] = contract.start_date
                    item["end_date"] = contract.end_date
                    item["playlist_id"] = j.playlist.id
                    item["location"] = j.playlist.product
                    item["create_date"] = j.playlist.create_date
                    item["video_name"] = k.video.name
                    item["video_duration"] = k.video.duration_all()
                    item["repeticiones"] = k.repeat_count
                    item["pauta_loop"] = j.pauta_loop
                    item["second_total"] = j.second_total
                    item["time_contract"] = j.time_contract
                    item["time_bonification"] = j.time_bonification

                    # print(j.playlist.create_date)
                    report.append(item)

        else:
            # encaso de no existir informacion de los videos se toma todo en vacio
            item = {}
            item["id"] = str(order_id) + str(0) + str(i.product.id) 
            item["contract_id"] = contract.id
            item["order_id"] = order_id
            item["video_id"] = 0
            item["client"] = contract.client.name
            item["start_date"] = contract.start_date
            item["end_date"] = contract.end_date
            item["playlist_id"] = 0

            item["location"] = i.product
            item["create_date"] = datetime.datetime.strptime('0001-01-01', "%Y-%m-%d").date()
            item["video_name"] = 'sin registro de playlist'
            item["video_duration"] = 0
            item["repeticiones"] = 0
            item["pauta_loop"] = 0
            item["second_total"] = 0
            item["time_contract"] = 0
            item["time_bonification"] = 0
            report.append(item)

        report_2 = report_resume(report)

    if request.method == 'GET':

        # for m in report:
            # print(m)


        template_name = 'reportemision/contract_date.html'
        contexto = {'report': report, 'contract': contract, 'order': order, 'report2':report_2}





        return render(request, template_name, contexto)

    if request.method == 'POST':

        bandera = request.POST.get('bandera')

        start_date_n = request.POST.get('start_date')
        end_date_n = request.POST.get('end_date')

        start_date_n = datetime.datetime.strptime(
            start_date_n, "%Y-%m-%d").date()
        end_date_n = datetime.datetime.strptime(end_date_n, "%Y-%m-%d").date()

        if bandera == '1':
            aux_order = []
            print(bandera)
            for item in report_2:
                
                if (not item['order_id'] in aux_order):
                    aux_order.append(item['order_id'])
                    order_id = Order.objects.get(pk=item['order_id'])
                    contract_id = Contract.objects.get(pk=item['contract_id'])
                    playlist_id = Playlist.objects.get(pk=item['playlist_id'])
                    document = Document(
                        start_date=start_date_n,
                        end_date=end_date_n,
                        contract=contract_id,
                        order=order_id,
                        repeat_pauta_day=item['pauta_loop'],
                        repeat_in_pauta=item['repeticiones'],

                        second_total_day=item['second_total'],
                        time_contract=item['time_contract'],
                        time_bonification=item['time_bonification'],
                        playlist=playlist_id,
                        user_created=request.user

                    )
                    document.save()
                    contract = Contract.objects.filter(state=True).all()
                    template_name = 'reportemision/contract_list.html'

                    contexto = {'obj': contract}
        else:
            # diferencia = end_date_n - start_date_n
            # diferencia = diferencia.days + 1
            # print(diferencia)

            report_date = []
            aux = []
            aux_report = []
            for item in report:
                aux_report = report
                if not(item["id"] in aux):
                    
                    aux.append(item["id"])
                    report_id = item["id"]
                    fechas = rellenar_fechas(aux_report, report_id, start_date_n, end_date_n)
                    report_date.append(fechas)
                    # print(report_date)
            
                

            template_name = 'reportemision/contract_complet.html'
            contexto = {'obj': report_date}
            # print(report_date)

        return render(request, template_name, contexto)


    return render(request, template_name, contexto)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
def report_resume(report):
    nueva_report = []
    aux_lista = []
    
    for item in report:
        if (not item["order_id"] in aux_lista):
            aux_lista.append(item["order_id"])
            max_bonification = hallar_bonificacion_max(report, item["order_id"])
            aux = extaer_playlist_id(report, max_bonification["playlist_id"])
            nueva_report = nueva_report + aux

    
    # for item in nueva_report:
        
    #     print(item)
    return(nueva_report)

def extaer_playlist_id(report, playlist_id):
    aux = []
    for item in report:
        if item["playlist_id"] == playlist_id:
            aux.append(item)

    return(aux)
        

def hallar_bonificacion_max(report, order_id):
    aux_max = 0
    for item2 in report:
        if item2["order_id"] == order_id:
            aux_max = item2
            pass

    for item in report:
        if item["order_id"] == order_id:
            if  item["time_bonification"] >= aux_max["time_bonification"]:
                aux_max = item
    
    
    return(aux_max)
# ==================================================================

def rellenar_fechas(lista, id, start_date_n, end_date_n):
    
    aux_lista = []
    
    dias = end_date_n - start_date_n
    dias = dias.days
    
    for item in lista:
        if item["id"] == id:
            aux_lista.append(item)

    
    
    
    oficial = aux_lista[0]

    inicio = start_date_n
    dia = start_date_n
    lol = aux_lista[0]
    final = aux_lista[len(aux_lista)-1]["create_date"]
    lista_final = []
    # print(str(aux_lista[0]["create_date"]))
    if str(aux_lista[0]["create_date"]) == '0001-01-01':
        # print('no tiene registro de video ni de pauta')
        pass
    else:

        for k in aux_lista:
            aux = 0
            diferencia =  k["create_date"] - inicio 
            inicio = k["create_date"]
            # print(diferencia.days)

            if diferencia.days == 0:
                aux = 0
            if diferencia.days > 1:
                
                aux = diferencia.days 
            if diferencia.days == 1:
                aux = 1

            # print(aux)

            for num in range(aux):
                # obj[str(dia)] = lol
                # lol["dia"] = dia
                a = {}
                a["dia"] = dia
                a["create_date"] = lol["create_date"]
                a["video_duration"] = lol["video_duration"]
                a["repeticiones"] = lol["repeticiones"]
                a["pauta_loop"] = lol["pauta_loop"]
                a["second_total"] = lol["second_total"]
                a["time_contract"] = lol["time_contract"]
                a["time_bonification"] = lol["time_bonification"]
                dia = dia + timedelta(days=1)
                lista_final.append(a)

            if dia == final:
                # obj[str(dia)] = k
                # k["dia"] = dia
                a = {}
                a["dia"] = dia
                a["create_date"] = k["create_date"]
                a["video_duration"] = k["video_duration"]
                a["repeticiones"] = k["repeticiones"]
                a["pauta_loop"] = k["pauta_loop"]
                a["second_total"] = k["second_total"]
                a["time_contract"] = k["time_contract"]
                a["time_bonification"] = k["time_bonification"]
                lista_final.append(a)

                
            lol = k

        if not(final == end_date_n):
            diferencia = end_date_n - final
            diferencia = diferencia.days + 1
            
            
            for num in range(diferencia):
                # obj[str(dia)] = aux_lista[len(aux_lista) - 1]
                lolo = aux_lista[len(aux_lista) - 1]
                # lolo["dia"] = dia
                a = {}
                a["dia"] = dia
                a["create_date"] = lolo["create_date"]
                a["video_duration"] = lol["video_duration"]
                a["repeticiones"] = lolo["repeticiones"]
                a["pauta_loop"] = lolo["pauta_loop"]
                a["second_total"] = lolo["second_total"]
                a["time_contract"] = lolo["time_contract"]
                a["time_bonification"] = lolo["time_bonification"]
                dia = dia + timedelta(days=1)
                lista_final.append(a)

    # print("================================================")
    # for w in obj:
    #     # print(type(w))
    #     print(str(obj[w]["create_date"]) + ' -> ' +str(w))
    #     # print(w) 
    # print("================================================")
    # lista_final.append(obj)
    oficial["fechas"] = lista_final
    # print("oficia-despues")
    # print(oficial)
    # print(lista_final)
    # print(oficial)
    # print("====dia====")
    # dia =  datetime.datetime.strptime('2020-02-29', "%Y-%m-%d").date()
    # print(dia + timedelta(days=1))
    # print("====dia=====")
    return oficial
