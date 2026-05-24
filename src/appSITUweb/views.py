import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import BusFormulario, PasajeroFormulario, TarjetaFormulario, ViajeFormulario
from .models import Bus, Pasajero, Tarjeta, Viaje
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

def home_view(request):
    return render(request,"index.html",{})

def pasajeros(request):
    data = PasajeroFormulario()
    pasajeros_list = Pasajero.objects.prefetch_related("tarjeta_set").all().order_by("id")
    total_pasajeros = pasajeros_list.count()

    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")

    return render(
        request,
        "pasajeros_list.html",
        {
            "pasajeros": pasajeros_list,
            "total_pasajeros": total_pasajeros,
            "form": data,
        },
    )


def tarjetas_list(request):
    tarjetas = Tarjeta.objects.select_related("idPasajero").all().order_by("id")
    tarjetas_total_monto = tarjetas.aggregate(total=Sum("monto")).get("total") or Decimal("0.00")
    pasajeros_con_tarjeta = tarjetas.values("idPasajero").distinct().count()

    return render(
        request,
        "tarjetas_list.html",
        {
            "tarjetas": tarjetas,
            "tarjetas_activas": tarjetas.count(),
            "tarjetas_total_monto": tarjetas_total_monto,
            "pasajeros_con_tarjeta": pasajeros_con_tarjeta,
        },
    )


def buses_list(request):
    buses = Bus.objects.prefetch_related("idTarjeta").all().order_by("id")
    hoy = timezone.localdate()
    buses_activos_hoy = Bus.objects.filter(viaje__fecha_viaje__date=hoy).distinct().count()
    buses_cooperativas = buses.values("cooperativa").distinct().count()

    return render(
        request,
        "buses_list.html",
        {
            "buses": buses,
            "buses_totales": buses.count(),
            "buses_activos_hoy": buses_activos_hoy,
            "buses_cooperativas": buses_cooperativas,
        },
    )


def viajes_list(request):
    viajes = Viaje.objects.select_related("pasajero", "bus").all().order_by("-fecha_viaje")
    hoy = timezone.localdate()
    viajes_hoy = viajes.filter(fecha_viaje__date=hoy)

    total_expr = ExpressionWrapper(
        F("costo") * F("cantidad"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    recaudacion_hoy = viajes_hoy.aggregate(total=Sum(total_expr)).get("total") or Decimal("0.00")
    buses_activos_hoy = Bus.objects.filter(viaje__fecha_viaje__date=hoy).distinct().count()
    tarjetas_activas = Tarjeta.objects.count()

    return render(
        request,
        "viajes_list.html",
        {
            "viajes": viajes,
            "recaudacion_hoy": recaudacion_hoy,
            "viajes_hoy": viajes_hoy.count(),
            "buses_activos_hoy": buses_activos_hoy,
            "tarjetas_activas": tarjetas_activas,
        },
    )


def pasajeroCreate(request):
    if request.method == "POST":
        formulario = PasajeroFormulario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
    return redirect(to="pasajeros")

def pasajerosEdit(request, id):
    pasajeros = get_object_or_404(Pasajero, id = id)
    data = {
        'form' : PasajeroFormulario(instance=pasajeros)
    }
    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, instance=pasajeros, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")

    return render(request,'pasajerosEdit.html',data)


@require_POST
def pasajerosDelete(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)
    pasajero.delete()
    return redirect(to="pasajeros")


def tarjetasCreate(request):
    if request.method == "POST":
        formulario = TarjetaFormulario(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="tarjetas_list")
    else:
        formulario = TarjetaFormulario()

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Crear tarjeta",
            "form": formulario,
            "texto_boton": "Guardar tarjeta",
        },
    )


def tarjetasEdit(request, id):
    tarjeta = get_object_or_404(Tarjeta, id=id)
    if request.method == "POST":
        formulario = TarjetaFormulario(data=request.POST, instance=tarjeta)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="tarjetas_list")
    else:
        formulario = TarjetaFormulario(instance=tarjeta)

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Editar tarjeta",
            "form": formulario,
            "texto_boton": "Guardar cambios",
        },
    )


@require_POST
def tarjetasDelete(request, id):
    tarjeta = get_object_or_404(Tarjeta, id=id)
    tarjeta.delete()
    return redirect(to="tarjetas_list")


def busesCreate(request):
    if request.method == "POST":
        formulario = BusFormulario(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="buses_list")
    else:
        formulario = BusFormulario()

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Crear bus",
            "form": formulario,
            "texto_boton": "Guardar bus",
        },
    )


def busesEdit(request, id):
    bus = get_object_or_404(Bus, id=id)
    if request.method == "POST":
        formulario = BusFormulario(data=request.POST, instance=bus)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="buses_list")
    else:
        formulario = BusFormulario(instance=bus)

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Editar bus",
            "form": formulario,
            "texto_boton": "Guardar cambios",
        },
    )


@require_POST
def busesDelete(request, id):
    bus = get_object_or_404(Bus, id=id)
    bus.delete()
    return redirect(to="buses_list")


def viajesCreate(request):
    if request.method == "POST":
        formulario = ViajeFormulario(data=request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect(to="viajes_list")
            except ValidationError as exc:
                formulario.add_error(None, exc)
    else:
        formulario = ViajeFormulario()

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Crear viaje",
            "form": formulario,
            "texto_boton": "Guardar viaje",
        },
    )


def viajesEdit(request, id):
    viaje = get_object_or_404(Viaje, id=id)
    if request.method == "POST":
        formulario = ViajeFormulario(data=request.POST, instance=viaje)
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect(to="viajes_list")
            except ValidationError as exc:
                formulario.add_error(None, exc)
    else:
        formulario = ViajeFormulario(instance=viaje)

    return render(
        request,
        "entity_form.html",
        {
            "titulo": "Editar viaje",
            "form": formulario,
            "texto_boton": "Guardar cambios",
        },
    )


@require_POST
def viajesDelete(request, id):
    viaje = get_object_or_404(Viaje, id=id)
    viaje.delete()
    return redirect(to="viajes_list")


def _pasajero_to_dict(pasajero):
    return {
        "id": pasajero.id,
        "cedula": pasajero.cedula,
        "nombre": pasajero.nombre,
        "apellido": pasajero.apellido,
        "email": pasajero.email,
        "imagen": pasajero.imagen.url if pasajero.imagen else "",
    }


def _json_body(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8") or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    return {}


def _validation_error_response(exc):
    if hasattr(exc, "message_dict"):
        return JsonResponse({"error": exc.message_dict}, status=400)
    return JsonResponse({"error": exc.messages}, status=400)


def api_pasajeros(request):
    if request.method == "GET":
        data = [_pasajero_to_dict(p) for p in Pasajero.objects.all().order_by("id")]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        if body != {}:
            pasajero = Pasajero(
                cedula=body.get("cedula", ""),
                nombre=body.get("nombre", ""),
                apellido=body.get("apellido", ""),
                email=body.get("email", ""),
                imagen=body.get("imagen", ""),
            )
            try:
                pasajero.full_clean()
                pasajero.save()
            except ValidationError as exc:
                return _validation_error_response(exc)
            return JsonResponse(_pasajero_to_dict(pasajero), status=201)

        formulario = PasajeroFormulario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            pasajero = formulario.save()
            return JsonResponse(_pasajero_to_dict(pasajero), status=201)

        return JsonResponse({"error": formulario.errors}, status=400)

    return HttpResponseNotAllowed(["GET", "POST"])


def api_pasajero_detalle(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)

    if request.method == "GET":
        return JsonResponse(_pasajero_to_dict(pasajero))

    if request.method in ["PUT", "PATCH"]:
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        pasajero.cedula = body.get("cedula", pasajero.cedula)
        pasajero.nombre = body.get("nombre", pasajero.nombre)
        pasajero.apellido = body.get("apellido", pasajero.apellido)
        pasajero.email = body.get("email", pasajero.email)
        if "imagen" in body:
            pasajero.imagen = body.get("imagen")

        try:
            pasajero.full_clean()
            pasajero.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_pasajero_to_dict(pasajero))

    if request.method == "DELETE":
        pasajero.delete()
        return JsonResponse({"ok": True, "message": "Pasajero eliminado."})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


def _tarjeta_to_dict(tarjeta):
    return {
        "id": tarjeta.id,
        "codigo": tarjeta.codigo,
        "monto": tarjeta.monto,
        "id_pasajero": tarjeta.idPasajero_id,
    }


def _bus_to_dict(bus):
    return {
        "id": bus.id,
        "placa": bus.placa,
        "cooperativa": bus.cooperativa,
        "numero": str(bus.numero),
        "pasajeros": list(bus.idTarjeta.values_list("id", flat=True)),
    }


def _viaje_to_dict(viaje):
    return {
        "id": viaje.id,
        "pasajero_id": viaje.pasajero_id,
        "bus_id": viaje.bus_id,
        "costo": str(viaje.costo),
        "cantidad": viaje.cantidad,
        "fecha_viaje": viaje.fecha_viaje.isoformat() if viaje.fecha_viaje else None,
        "efectivo": viaje.efectivo,
        "tipo": viaje.tipo,
    }


def api_tarjetas(request):
    if request.method == "GET":
        data = [_tarjeta_to_dict(t) for t in Tarjeta.objects.all().order_by("id")]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        pasajero = get_object_or_404(Pasajero, id=body.get("id_pasajero"))
        tarjeta = Tarjeta(
            codigo=body.get("codigo", ""),
            monto=body.get("monto", ""),
            idPasajero=pasajero,
        )
        try:
            tarjeta.full_clean()
            tarjeta.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_tarjeta_to_dict(tarjeta), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


def api_tarjeta_detalle(request, id):
    tarjeta = get_object_or_404(Tarjeta, id=id)

    if request.method == "GET":
        return JsonResponse(_tarjeta_to_dict(tarjeta))

    if request.method in ["PUT", "PATCH"]:
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        if "id_pasajero" in body:
            tarjeta.idPasajero = get_object_or_404(Pasajero, id=body.get("id_pasajero"))
        tarjeta.codigo = body.get("codigo", tarjeta.codigo)
        tarjeta.monto = body.get("monto", tarjeta.monto)

        try:
            tarjeta.full_clean()
            tarjeta.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_tarjeta_to_dict(tarjeta))

    if request.method == "DELETE":
        tarjeta.delete()
        return JsonResponse({"ok": True, "message": "Tarjeta eliminada."})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


def api_buses(request):
    if request.method == "GET":
        data = [_bus_to_dict(b) for b in Bus.objects.all().order_by("id")]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        bus = Bus(
            placa=body.get("placa", ""),
            cooperativa=body.get("cooperativa", ""),
            numero=body.get("numero", 0),
        )
        try:
            bus.full_clean()
            bus.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_bus_to_dict(bus), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


def api_bus_detalle(request, id):
    bus = get_object_or_404(Bus, id=id)

    if request.method == "GET":
        return JsonResponse(_bus_to_dict(bus))

    if request.method in ["PUT", "PATCH"]:
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        bus.placa = body.get("placa", bus.placa)
        bus.cooperativa = body.get("cooperativa", bus.cooperativa)
        bus.numero = body.get("numero", bus.numero)

        try:
            bus.full_clean()
            bus.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_bus_to_dict(bus))

    if request.method == "DELETE":
        bus.delete()
        return JsonResponse({"ok": True, "message": "Bus eliminado."})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


def api_viajes(request):
    if request.method == "GET":
        data = [_viaje_to_dict(v) for v in Viaje.objects.all().order_by("id")]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        pasajero = get_object_or_404(Pasajero, id=body.get("pasajero_id"))
        bus = get_object_or_404(Bus, id=body.get("bus_id"))
        viaje = Viaje(
            pasajero=pasajero,
            bus=bus,
            costo="0.30",
            cantidad=body.get("cantidad", 0),
            efectivo=body.get("efectivo", True),
            tipo=body.get("tipo", ""),
        )
        try:
            viaje.full_clean()
            viaje.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_viaje_to_dict(viaje), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


def api_viaje_detalle(request, id):
    viaje = get_object_or_404(Viaje, id=id)

    if request.method == "GET":
        return JsonResponse(_viaje_to_dict(viaje))

    if request.method in ["PUT", "PATCH"]:
        body = _json_body(request)
        if body is None:
            return JsonResponse({"error": "JSON invalido."}, status=400)

        if "pasajero_id" in body:
            viaje.pasajero = get_object_or_404(Pasajero, id=body.get("pasajero_id"))
        if "bus_id" in body:
            viaje.bus = get_object_or_404(Bus, id=body.get("bus_id"))

        viaje.costo = "0.30"
        viaje.cantidad = body.get("cantidad", viaje.cantidad)
        viaje.efectivo = body.get("efectivo", viaje.efectivo)
        viaje.tipo = body.get("tipo", viaje.tipo)

        try:
            viaje.full_clean()
            viaje.save()
        except ValidationError as exc:
            return _validation_error_response(exc)

        return JsonResponse(_viaje_to_dict(viaje))

    if request.method == "DELETE":
        viaje.delete()
        return JsonResponse({"ok": True, "message": "Viaje eliminado."})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])