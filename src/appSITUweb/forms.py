from django import forms
from .models import Bus, Pasajero, Tarjeta, Viaje


class BaseSituForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs.update({"class": "form-control"})


class PasajeroFormulario(BaseSituForm):

	class Meta:
		model = Pasajero
		fields=["cedula","nombre","apellido", "email","imagen"] 
		#fields = '__all__'


class TarjetaFormulario(BaseSituForm):
	class Meta:
		model = Tarjeta
		fields = ["codigo", "monto", "idPasajero"]


class BusFormulario(BaseSituForm):
	class Meta:
		model = Bus
		fields = ["placa", "cooperativa", "numero"]


class ViajeFormulario(BaseSituForm):
	efectivo = forms.ChoiceField(
		choices=(
			("efectivo", "Efectivo"),
			("tarjeta", "Tarjeta"),
		),
		label="Metodo de pago",
	)

	class Meta:
		model = Viaje
		fields = ["pasajero", "bus", "cantidad", "efectivo", "tipo"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance and self.instance.pk:
			self.initial["efectivo"] = "efectivo" if self.instance.efectivo else "tarjeta"
		else:
			self.initial.setdefault("efectivo", "efectivo")

	def clean_cantidad(self):
		cantidad = self.cleaned_data.get("cantidad")
		if cantidad is None or cantidad < 1:
			raise forms.ValidationError("La cantidad de viajes debe ser al menos 1.")
		return cantidad

	def clean_efectivo(self):
		return self.cleaned_data.get("efectivo") == "efectivo"