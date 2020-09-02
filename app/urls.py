
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [

    path('', include(('bases.urls', 'bases'), namespace='bases')),
    # rutas de modulo componentes
    path('component/', include(('component.urls', 'component'), namespace='component')),

    # rutas del modulo ventas
    path('sales/', include(('sales.urls', 'sales'), namespace='sales')),
    # rutas para ocontenidos y videos pautas
    path('content/', include(('content.urls', 'content'), namespace='content')),
    # ruta para los reportes y envio de mails
    path('report/', include(('report.urls', 'report'), namespace='report')),
    # rutas para los reportes que se pueden imprimir
    path('reportprint/', include(('reportprint.urls',
                                  'reportprint'), namespace='reportprint')),

    # rutas para los reportes de emision de cliente y mensual general
    path('reportemision/', include(('reportemision.urls',
                                    'reportemision'), namespace='reportemision')),

    # rutas para rondas de personal en las locaciones
    path('rondas/', include(('rondas.urls', 'rondas'), namespace='rondas')),

    # rutas para mostrar vistas de reportes rapidos como clinetes por locaion spots por clientes
    path('display/', include(('display.urls', 'display'), namespace='display')),

    # rutas para mostrar vistas de reportes rapidos como clinetes por locaion spots por clientes
    path('maintenance/', include(('maintenance.urls', 'maintenance'), namespace='maintenance')),

    # rutas para mostrar todos los contratos y sus locaciones con sus respectivos spots 
    # path('allviewcontract/', include(('allviewcontract.urls', 'allviewcontract'), namespace='allviewcontract')),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
