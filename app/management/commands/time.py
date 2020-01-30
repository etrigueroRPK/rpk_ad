from django.core.management.base import BaseCommand
from django.utils import timezone

from django.template import loader


from django.core.mail import send_mail

from sales.models import Contract
from report.views import reporte


class Command(BaseCommand):
    help = 'envia mails de prueba '

    def handle(self, *args, **kwargs):
        self.check_end_date()
        self.stdout.write("!!!!! ")


    def check_end_date(self):

        date_now = timezone.now()
        date_now_Ymd = date_now.strftime("%Y-%m-%d")
        date_now_dmY = date_now.strftime("%d/%m/%Y")
        print(date_now)
        end_date = Contract.objects.filter(end_date=date_now_Ymd)

        if end_date:

            # TODO: validar solo si hay contratos finalizados
            html_message = loader.render_to_string(
                '../../report/templates/report/report.html',
                {
                    'obj': end_date
                }
            )
            send_mail(
                'RECORDATORIO FINAL DE CONTRATO: '+ date_now_dmY,
                'Sistema - ADpubli RPK. Srl.',
                'edmundotriguero@gmail.com',
                ['etriguero@rpk.com.bo', 'kevin.vargas.pastor@gmail.com'],
                fail_silently=True,
                html_message=html_message
            )
            print(end_date)
