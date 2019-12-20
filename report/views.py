from django.shortcuts import render

from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required



@login_required(login_url='/login/')
def reporte(request):
    print('+++++++++++++++++++')
    send_mail(
        'hola desde djnago',
        'este es el mensaje',
        'edmundotriguero@gmail.com',
        ['etriguero@rpk.com.bo'],
        fail_silently = False
    )
    return render(request, 'report/report.html')