from django.core.management.base import BaseCommand
from django.utils import timezone

from django.template import loader
from django.conf import settings

from django.core.mail import send_mail

from sales.models import Contract, Order



class Command(BaseCommand):
    help = 'envia mails de contrato finalizado '

    def handle(self, *args, **kwargs):
        self.check_end_date()
        self.stdout.write("!!!!! ")


    def check_end_date(self):

        date_now = timezone.now()
        date_now_Ymd = date_now.strftime("%Y-%m-%d")
        date_now_dmY = date_now.strftime("%d/%m/%Y")
        print(date_now)
        end_date = Contract.objects.filter(end_date=date_now_Ymd)
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
        # contexto = {'obj': end_date_list}

        if end_date:
            try:

                # TODO: validar solo si hay contratos finalizados
                html_message = loader.render_to_string(
                    '../../report/templates/report/email_end_contract.html',
                    {
                        'obj': end_date_list
                    }
                )
                send_mail(
                    'RECORDATORIO FINAL DE CONTRATO: '+ date_now_dmY,
                    'Sistema - ADpubli RPK. Srl.',
                    settings.EMAIL_HOST_USER,
                    ['etriguero@rpk.com.bo', 'kvargas@rpk.com.bo'],
                    fail_silently=True,
                    html_message=html_message
                )
                print(end_date)
            except Exception as e:
                print('Error:')
                print(e)

