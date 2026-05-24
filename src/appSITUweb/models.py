from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError

class Pasajero(models.Model):
	cedula = models.CharField(max_length=10, blank=False)
	nombre = models.CharField(max_length=10, blank=False)
	imagen = models.ImageField(upload_to='img/%Y/%m/%d/')
	apellido = models.CharField(max_length=30)
	email = models.EmailField()
	def __str__(self):
		return self.cedula

class Tarjeta(models.Model):
	codigo = models.CharField(max_length=6, blank=False)
	monto = models.CharField(max_length=3, blank=False)
	idPasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
	def __str__(self):
		return f'Tarjeta: {self.codigo} | Pasajero: {str(self.idPasajero)} | Monto Tarjeta: {str(self.monto)}'
                                                                
class Bus(models.Model):
	placa = models.CharField(max_length=7, blank=False)
	cooperativa = models.CharField(max_length=10, blank=False)
	numero = models.DecimalField(max_digits=3, decimal_places=0)
	idTarjeta = models.ManyToManyField(Pasajero, through='Viaje')	
	def __str__(self):
		return self.placa

class Viaje(models.Model):
	pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
	bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
	costo = models.DecimalField(max_digits=4, decimal_places=2)
	cantidad = models.IntegerField()
	fecha_viaje = models.DateTimeField(auto_now_add=True)
	efectivo = models.BooleanField(default=True)	
	confortViaje = (
		('comodo', 'Comodo'),
		('incomodo', 'Incomodo'),
	)
	tipo = models.CharField(max_length=20, choices=confortViaje, default="")

	def save(self, *args, **kwargs):
		self.costo = Decimal("0.30")
		es_nuevo = self.pk is None

		# Solo descuenta al crear un viaje pagado con tarjeta.
		if es_nuevo and not self.efectivo:
			tarjeta = Tarjeta.objects.filter(idPasajero=self.pasajero).order_by("id").first()
			if not tarjeta:
				raise ValidationError("El pasajero no tiene tarjeta registrada.")

			try:
				saldo_actual = Decimal(str(tarjeta.monto).strip())
			except Exception as exc:
				raise ValidationError("El saldo de la tarjeta no tiene un formato numerico valido.") from exc

			cantidad_viajes = self.cantidad if self.cantidad and self.cantidad > 0 else 1
			descuento = self.costo * Decimal(cantidad_viajes)
			if saldo_actual < descuento:
				raise ValidationError("Saldo insuficiente en la tarjeta para registrar el viaje.")

			nuevo_saldo = saldo_actual - descuento
			tarjeta.monto = f"{nuevo_saldo:.2f}"
			tarjeta.save(update_fields=["monto"])

		super().save(*args, **kwargs)

	def __str__(self):
		return f'Pasajero: {self.pasajero.cedula} | Pasj.Nombre: {self.pasajero.nombre} | Precio: {str(self.costo)} | BusPlaca: {str(self.bus.placa)} | No.Bus: {str(self.bus.numero)}'

class SimularAccesoPago(models.Model):
	numero = models.CharField(max_length=7, blank=False)
	fecha_viaje = models.DateTimeField(auto_now_add=True)
	viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
	tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
	def __str__(self):
	  return f'Pasajero: {self.viaje.pasajero.nombre}'
