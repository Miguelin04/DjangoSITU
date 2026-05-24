"""ProyectoSITU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from appSITUweb.views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('pasajeros/', pasajeros, name='pasajeros'),
    path('pasajeros/create/', pasajeroCreate, name='pasajero_create'),
    path('pasajerosEdit/<id>', pasajerosEdit, name='pasajerosEdit'),
    path('pasajeros/delete/<int:id>/', pasajerosDelete, name='pasajeros_delete'),
    path('tarjetas/', tarjetas_list, name='tarjetas_list'),
    path('buses/', buses_list, name='buses_list'),
    path('viajes/', viajes_list, name='viajes_list'),
    path('tarjetas/create/', tarjetasCreate, name='tarjetas_create'),
    path('tarjetas/edit/<int:id>/', tarjetasEdit, name='tarjetas_edit'),
    path('tarjetas/delete/<int:id>/', tarjetasDelete, name='tarjetas_delete'),
    path('buses/create/', busesCreate, name='buses_create'),
    path('buses/edit/<int:id>/', busesEdit, name='buses_edit'),
    path('buses/delete/<int:id>/', busesDelete, name='buses_delete'),
    path('viajes/create/', viajesCreate, name='viajes_create'),
    path('viajes/edit/<int:id>/', viajesEdit, name='viajes_edit'),
    path('viajes/delete/<int:id>/', viajesDelete, name='viajes_delete'),
    path('api/pasajeros/', api_pasajeros, name='api_pasajeros'),
    path('api/pasajeros/<int:id>/', api_pasajero_detalle, name='api_pasajero_detalle'),
    path('api/tarjetas/', api_tarjetas, name='api_tarjetas'),
    path('api/tarjetas/<int:id>/', api_tarjeta_detalle, name='api_tarjeta_detalle'),
    path('api/buses/', api_buses, name='api_buses'),
    path('api/buses/<int:id>/', api_bus_detalle, name='api_bus_detalle'),
    path('api/viajes/', api_viajes, name='api_viajes'),
    path('api/viajes/<int:id>/', api_viaje_detalle, name='api_viaje_detalle'),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
