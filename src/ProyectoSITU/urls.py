"""ProyectoSITU URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # <-- Importación nativa para la redirección
from appSITUweb.views import *

urlpatterns = [
    # CORREGIDO: Redirección limpia hacia la lista de pasajeros
    path('', RedirectView.as_view(url='/pasajeros/', permanent=False), name='home'),
    
    path('admin/', admin.site.urls),  # Asegurado admin.site.urls estándar
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
    
    # API endpoints
    path('api/pasajeros/', api_pasajeros, name='api_pasajeros'),
    path('api/pasajeros/<int:id>/', api_pasajero_detalle, name='api_pasajero_detalle'),
    path('api/tarjetas/', api_tarjetas, name='api_tarjetas'),
    path('api/tarjetas/<int:id>/', api_tarjeta_detalle, name='api_tarjeta_detalle'),
    path('api/buses/', api_buses, name='api_buses'),
    path('api/buses/<int:id>/', api_bus_detalle, name='api_bus_detalle'),
    path('api/viajes/', api_viajes, name='api_viajes'),
    path('api/viajes/<int:id>/', api_viaje_detalle, name='api_viaje_detalle'),
]

# Servir archivos de media de manera dinámica
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
