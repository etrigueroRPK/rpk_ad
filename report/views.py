from django.shortcuts import render
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.utils import timezone
from sales.models import Contract, Order




@login_required(login_url='/login/')
def reporte(request):
    print('+++++++++++++++++++')
    template = get_template('report/saludo_mail.html')
    content = template.render()
    email = EmailMultiAlternatives(
        'hola desde djnago',
        'este es el mensaje',
        settings.EMAIL_HOST_USER,
        ['etriguero@rpk.com.bo','edmundotriguero@gmail.com']
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    # return render(request, 'report/report.html')



def report_mail_view(request):
    template_name = 'report/email_end_contract.html'
    contexto = {}
    date_now = timezone.now()
    date_now_Ymd = date_now.strftime("%Y-%m-%d")
    date_now_dmY = date_now.strftime("%d/%m/%Y")
    print(date_now)
    end_date = Contract.objects.filter(end_date=date_now_Ymd)

    if not end_date:
        return HttpResponse('cliente no existe' + str(id))

    if request.method == 'GET':
        end_date_list = []
        for item in end_date:
            objeto = {}
            order = Order.objects.filter(contract=item.id)
            # print(type(item))
            # print(order)
            objeto['client']= item.client
            objeto['start_date'] = item.start_date
            objeto['end_date'] = item.end_date
            objeto['orders'] = order
            # item['orden'] = order
            end_date_list.append(objeto)
        contexto = {'obj': end_date_list}

    # if request.method == 'POST':
    #     cat.state = False
    #     cat.save()
    #     contexto = {'obj': 'OK'}
    #     return HttpResponse('cliente Inactivo')

    return render(request, template_name, contexto)
