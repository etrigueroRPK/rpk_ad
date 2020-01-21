
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [

    path('',include(('bases.urls','bases'), namespace='bases')),
    # rutas de modulo componentes
    path('component/',include(('component.urls','component'), namespace='component')),

    # rutas del modulo ventas
    path('sales/',include(('sales.urls','sales'), namespace='sales')),
    # rutas para ocontenidos y videos pautas
    path('content/',include(('content.urls','content'), namespace='content')),
    # ruta para los reportes y envio de mails
    path('report/',include(('report.urls','report'), namespace='report')),
    # rutas para los reportes que se pueden imprimir
    path('reportprint/',include(('reportprint.urls','reportprint'), namespace='reportprint')),



    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
