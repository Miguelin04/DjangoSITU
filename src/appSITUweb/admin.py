from django.contrib import admin
from .models import Pasajero
from .models import Bus
from .models import Tarjeta
from .models import Viaje
from . models import SimularAccesoPago

class AdminPasajero(admin.ModelAdmin):
    list_display = ["__str__","nombre","apellido","cedula","email"]	
    class Meta(object):
	      model = Pasajero

class AdminTarjeta(admin.ModelAdmin):
    list_display = ["__str__","codigo","monto"]
    class Meta(object):
	      model = Tarjeta

class AdminBus(admin.ModelAdmin):
    list_display = ["__str__","placa","numero"]
    class Meta(object):
	      model = Bus

class AdminViaje(admin.ModelAdmin):
    list_display = ["__str__","bus", "costo","fecha_viaje","efectivo"]
    class Meta(object):
	      model = Viaje

class AdminSimularAccesoPago(admin.ModelAdmin):
    list_display = ["__str__","numero", "fecha_viaje"]
    class Meta(object):
	      model = SimularAccesoPago

admin.site.register(Pasajero,AdminPasajero)
admin.site.register(Tarjeta,AdminTarjeta)
admin.site.register(Bus,AdminBus)
admin.site.register(Viaje,AdminViaje)
admin.site.register(SimularAccesoPago,AdminSimularAccesoPago)
