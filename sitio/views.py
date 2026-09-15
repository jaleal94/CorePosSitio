"""Las vistas del sitio: la pagina publica y el panel de contactos."""

import csv

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from . import contenido
from .estructurados import datos_del_sitio
from .formularios import FormularioDeContacto
from .models import Contacto, EstadoContacto
from .planes import LO_QUE_TRAE, PLANES
from .servicios import PLAZO_DE_RESPUESTA, enlace_de_whatsapp, registrar_contacto, sin_atender

CLAVE_DE_GRACIAS = "contacto_recien_enviado"


def _ip(request):
    adelantado = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if adelantado:
        return adelantado.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or None


def _contexto_de_portada(formulario, request=None):
    return {
        "heroe": contenido.HEROE,
        "problemas": contenido.PROBLEMAS,
        "pasos": contenido.PASOS,
        "grupos": contenido.LO_QUE_HACE,
        "no_hace": contenido.LO_QUE_NO_HACE,
        "capturas": contenido.CAPTURAS,
        "planes": PLANES,
        "incluido": LO_QUE_TRAE,
        "preguntas": contenido.PREGUNTAS,
        "formulario": formulario,
        "estructurados": datos_del_sitio(request) if request else "",
    }


# Alto a proposito: en un local todos comparten la conexion, y un limite que
# estorbe a una persona de verdad es peor que el robot que evita.
@ratelimit(key="ip", rate="10/h", method="POST", block=True)
@require_http_methods(["GET", "POST"])
def portada(request):
    formulario = FormularioDeContacto(request.POST or None)

    if request.method == "POST":
        if formulario.lo_lleno_un_robot:
            # Se responde igual que a un envio bueno. Decirle que fue detectado
            # le enseña a la siguiente pasada.
            return redirect(reverse("sitio:gracias"))

        if formulario.is_valid():
            contacto, es_nuevo = registrar_contacto(
                datos=formulario.cleaned_data,
                origen=request.POST.get("origen", "")[:40],
                ip=_ip(request),
            )
            # Ya esta guardado. Lo que sigue es comodidad: si fallara, no se
            # perderia el contacto (principio III).
            request.session[CLAVE_DE_GRACIAS] = {
                "nombre": contacto.nombre.split(" ")[0],
                "es_nuevo": es_nuevo,
            }
            return redirect(reverse("sitio:gracias"))

        # Se vuelve a la pagina con el formulario marcado y sin perder nada de
        # lo que escribio.
        contexto = _contexto_de_portada(formulario, request)
        contexto["hay_errores"] = True
        return render(request, "sitio/portada.html", contexto)

    return render(request, "sitio/portada.html", _contexto_de_portada(formulario, request))


def gracias(request):
    datos = request.session.pop(CLAVE_DE_GRACIAS, None)
    return render(request, "sitio/gracias.html", {"datos": datos, "plazo": PLAZO_DE_RESPUESTA})


def privacidad(request):
    return render(request, "sitio/privacidad.html")


def robots(request):
    """Lo publico se indexa; el panel no.

    Se sirve desde una vista y no como archivo estatico para que la direccion
    del mapa salga de las rutas de verdad y no de un texto que envejece.
    """
    lineas = [
        "User-agent: *",
        "Allow: /$",
        "Allow: /privacidad/",
        "Disallow: /contactos/",
        "Disallow: /gracias/",
        "Disallow: /admin/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    texto = "\n".join(lineas)
    return HttpResponse(texto, content_type="text/plain; charset=utf-8")


def no_encontrado(request, exception=None):
    return render(request, "sitio/errores/404.html", status=404)


def fallo_del_servidor(request):
    return render(request, "sitio/errores/500.html", status=500)


# ------------------------------------------------------------------- el panel


@staff_member_required
def panel(request):
    """Los contactos, los que faltan por atender primero."""
    estado = request.GET.get("estado", "")
    contactos = Contacto.objects.all()
    if estado in EstadoContacto.values:
        contactos = contactos.filter(estado=estado)

    filas = [
        {"contacto": contacto, "whatsapp": enlace_de_whatsapp(contacto)}
        for contacto in contactos.select_related("atendido_por")[:200]
    ]

    return render(
        request,
        "sitio/panel/contactos.html",
        {
            "filas": filas,
            "estado": estado,
            "estados": EstadoContacto.choices,
            "pendientes": sin_atender().count(),
            "total": Contacto.objects.count(),
        },
    )


@staff_member_required
@require_http_methods(["POST"])
def actualizar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)

    estado = request.POST.get("estado")
    if estado in EstadoContacto.values:
        contacto.estado = estado
        if estado != EstadoContacto.NUEVO and contacto.atendido_en is None:
            contacto.atendido_en = timezone.now()
            contacto.atendido_por = request.user
    contacto.notas = request.POST.get("notas", contacto.notas)
    contacto.save()

    messages.success(request, f"{contacto.nombre}: actualizado.")
    return redirect(reverse("sitio:panel"))


@staff_member_required
def exportar(request):
    """La lista completa, para abrirla en Excel."""
    respuesta = HttpResponse(content_type="text/csv; charset=utf-8")
    respuesta["Content-Disposition"] = 'attachment; filename="contactos.csv"'
    # La marca de orden es lo que hace que Excel en español abra el archivo con
    # los acentos bien puestos.
    respuesta.write("﻿")

    escritor = csv.writer(respuesta)
    escritor.writerow(
        ["fecha", "nombre", "comercio", "telefono", "correo", "mensaje", "estado", "notas"]
    )
    for contacto in Contacto.objects.all().iterator():
        escritor.writerow(
            [
                contacto.creado_en.strftime("%d/%m/%Y %H:%M"),
                contacto.nombre,
                contacto.comercio,
                contacto.telefono_legible,
                contacto.correo,
                contacto.mensaje,
                contacto.get_estado_display(),
                contacto.notas,
            ]
        )
    return respuesta
