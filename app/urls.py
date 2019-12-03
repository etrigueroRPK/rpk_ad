
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('',include(('bases.urls','bases'), namespace='bases')),
    path('component/',include(('component.urls','component'), namespace='component')),

    path('admin/', admin.site.urls),
]
