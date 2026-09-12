"""El contacto: que se guarde siempre, que no se duplique, que no lo llene un robot.

Es la unica conversion que importa y la unica superficie del sitio abierta a
internet. Un contacto perdido es un cliente perdido, y lo peor es que no hay
forma de enterarse de que se perdio (principio III).
"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from sitio.models import Contacto, EstadoContacto, solo_digitos
from sitio.servicios import PLAZO_DE_RESPUESTA, enlace_de_whatsapp, registrar_contacto

pytestmark = pytest.mark.django_db

BUENO = {
    "nombre": "Maria Perez",
    "comercio": "Bodega La Esquina",
    "telefono": "0414 123.45.67",
    "correo": "maria@ejemplo.test",
    "mensaje": "Tengo dos cajas y quiero saber si me sirve",
}


def enviar(client, **cambios):
    datos = {**BUENO, **cambios}
    return client.post(reverse("sitio:portada"), datos, follow=True)


# ------------------------------------------------------------ que se guarde


def test_un_envio_valido_guarda_el_contacto(client):
    respuesta = enviar(client)

    assert respuesta.status_code == 200
    contacto = Contacto.objects.get()
    assert contacto.nombre == "Maria Perez"
    assert contacto.comercio == "Bodega La Esquina"
    assert contacto.mensaje == "Tengo dos cajas y quiero saber si me sirve"
    assert contacto.esta_sin_atender


def test_el_telefono_se_guarda_normalizado(client):
    """`0414-123.45.67` y `04141234567` son el mismo telefono (D-01)."""
    enviar(client)

    assert Contacto.objects.get().telefono == "04141234567"


def test_queda_registrado_de_donde_llego(client):
    """Saber que seccion convence es la unica forma de mejorar la pagina."""
    client.post(reverse("sitio:portada"), {**BUENO, "origen": "seccion-precios"}, follow=True)

    contacto = Contacto.objects.get()
    assert contacto.origen == "seccion-precios"
    assert contacto.origen_ip


def test_despues_de_enviar_se_ve_la_pagina_de_gracias(client):
    respuesta = enviar(client)

    cuerpo = respuesta.content.decode()
    assert "Maria" in cuerpo
    assert PLAZO_DE_RESPUESTA in cuerpo


def test_el_correo_y_el_mensaje_son_opcionales(client):
    enviar(client, correo="", mensaje="")

    contacto = Contacto.objects.get()
    assert contacto.correo == ""
    assert contacto.mensaje == ""


# ---------------------------------------------------------- que no se duplique


def test_un_reenvio_no_crea_un_segundo_contacto(client):
    """Quien no ve respuesta en una hora lo manda otra vez. Es lo normal."""
    enviar(client)
    enviar(client, mensaje="Sigo interesada")

    assert Contacto.objects.count() == 1


def test_el_reenvio_suma_lo_nuevo_que_conto(client):
    enviar(client)
    enviar(client, mensaje="Se me olvido decir que tengo dos locales")

    contacto = Contacto.objects.get()
    assert "dos cajas" in contacto.mensaje
    assert "dos locales" in contacto.mensaje


def test_el_reenvio_no_pisa_el_trabajo_del_operador(client):
    """Su estado y sus notas son nuestras, no suyas."""
    enviar(client)
    contacto = Contacto.objects.get()
    contacto.estado = EstadoContacto.ATENDIDO
    contacto.notas = "Ya la llame, quedamos para el martes"
    contacto.save()

    enviar(client, mensaje="Otra cosa")

    contacto.refresh_from_db()
    assert contacto.estado == EstadoContacto.ATENDIDO
    assert contacto.notas == "Ya la llame, quedamos para el martes"


def test_el_servicio_dice_si_era_nuevo():
    _, primero = registrar_contacto(datos=BUENO)
    _, segundo = registrar_contacto(datos=BUENO)

    assert primero is True
    assert segundo is False


# ----------------------------------------------------------------- los robots


def test_un_envio_con_la_trampa_llena_no_guarda_nada(client):
    respuesta = enviar(client, sitio_web="http://spam.test")

    assert not Contacto.objects.exists()
    # Y se le responde igual que a una persona: decirle que fue detectado le
    # enseña a la siguiente pasada.
    assert respuesta.status_code == 200
    assert "Listo" in respuesta.content.decode()


def test_la_trampa_no_le_pide_nada_a_una_persona(client):
    """Escondida, fuera del tabulador y anunciada a los lectores de pantalla."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    trampa = cuerpo.split('name="sitio_web"')[0].split("<div")[-1]

    assert "sr-only" in trampa
    assert 'aria-hidden="true"' in trampa
    assert 'tabindex="-1"' in cuerpo


# ------------------------------------------------------------- lo que falla


def test_un_campo_que_falta_se_explica_sin_perder_lo_escrito(client):
    respuesta = client.post(reverse("sitio:portada"), {**BUENO, "telefono": ""})

    cuerpo = respuesta.content.decode()
    assert respuesta.status_code == 200
    assert not Contacto.objects.exists()
    assert "Bodega La Esquina" in cuerpo, "lo que ya habia escrito no se puede perder"
    assert "Falta algo" in cuerpo


def test_un_telefono_corto_se_explica_en_lenguaje_comun(client):
    respuesta = client.post(reverse("sitio:portada"), {**BUENO, "telefono": "12345"})

    assert "telefono completo" in respuesta.content.decode()
    assert not Contacto.objects.exists()


# ------------------------------------------------------------------ whatsapp


def test_el_enlace_de_whatsapp_la_llama_por_su_nombre():
    contacto, _ = registrar_contacto(datos=BUENO)

    enlace = enlace_de_whatsapp(contacto)

    assert enlace.startswith("https://wa.me/04141234567?text=")
    assert "Maria" in enlace
    assert "Bodega" in enlace


# -------------------------------------------------------------------- el panel


@pytest.fixture
def personal(client):
    usuario = User.objects.create_user("operador", password="clave-de-prueba", is_staff=True)
    client.force_login(usuario)
    return usuario


def test_sin_sesion_no_se_ve_el_panel(client):
    for nombre in ["panel", "exportar"]:
        respuesta = client.get(reverse(f"sitio:{nombre}"))
        assert respuesta.status_code == 302, f"{nombre} se ve sin sesion"


def test_el_panel_muestra_los_contactos_con_su_enlace(client, personal):
    registrar_contacto(datos=BUENO)

    cuerpo = client.get(reverse("sitio:panel")).content.decode()

    assert "Maria Perez" in cuerpo
    assert "Bodega La Esquina" in cuerpo
    assert "0414-1234567" in cuerpo
    assert "wa.me/04141234567" in cuerpo


def test_el_panel_cuenta_los_que_faltan_por_atender(client, personal):
    registrar_contacto(datos=BUENO)
    registrar_contacto(datos={**BUENO, "telefono": "04149999999"})

    respuesta = client.get(reverse("sitio:panel"))

    assert respuesta.context["pendientes"] == 2


def test_marcar_atendido_deja_constancia_de_quien_y_cuando(client, personal):
    contacto, _ = registrar_contacto(datos=BUENO)

    client.post(
        reverse("sitio:actualizar_contacto", args=[contacto.pk]),
        {"estado": EstadoContacto.ATENDIDO, "notas": "Quedamos para el martes"},
    )

    contacto.refresh_from_db()
    assert contacto.estado == EstadoContacto.ATENDIDO
    assert contacto.atendido_por == personal
    assert contacto.atendido_en is not None
    assert contacto.notas == "Quedamos para el martes"


def test_la_exportacion_trae_los_contactos(client, personal):
    registrar_contacto(datos=BUENO)

    respuesta = client.get(reverse("sitio:exportar"))
    cuerpo = respuesta.content.decode("utf-8-sig")

    assert respuesta["Content-Type"].startswith("text/csv")
    assert "Maria Perez" in cuerpo
    assert "0414-1234567" in cuerpo


# ------------------------------------------------------------------ el comando


def test_el_comando_lista_los_pendientes():
    from io import StringIO

    from django.core.management import call_command

    registrar_contacto(datos=BUENO)
    salida = StringIO()

    call_command("contactos_pendientes", stdout=salida)

    texto = salida.getvalue()
    assert "1 contacto sin atender" in texto
    assert "Maria Perez" in texto


def test_el_comando_lo_dice_cuando_no_hay_nada_pendiente():
    from io import StringIO

    from django.core.management import call_command

    salida = StringIO()
    call_command("contactos_pendientes", stdout=salida)

    assert "No hay contactos sin atender" in salida.getvalue()


# ------------------------------------------------------------------ utilidades


@pytest.mark.parametrize(
    ("escrito", "esperado"),
    [
        ("0414-123.45.67", "04141234567"),
        ("0414 123 4567", "04141234567"),
        ("+58 414 1234567", "584141234567"),
        ("", ""),
    ],
)
def test_el_telefono_se_normaliza(escrito, esperado):
    assert solo_digitos(escrito) == esperado


# --------------------------------------------------------------- el limite


def test_el_limite_de_tasa_dice_que_espere_y_no_que_no_tiene_permiso(client, settings):
    """Decir "no tiene permiso" cuando si lo tiene es mentir (principio I)."""
    for numero in range(11):
        respuesta = client.post(
            reverse("sitio:portada"), {**BUENO, "telefono": f"0414123{numero:04d}"}
        )

    assert respuesta.status_code == 429
    cuerpo = respuesta.content.decode()
    assert "Espere un momento" in cuerpo
    assert "permiso" in cuerpo, "tiene que aclarar que no es falta de permiso"
    assert "WhatsApp" in cuerpo, "y ofrecer la salida"


def test_los_primeros_envios_pasan_sin_estorbo(client):
    """Un limite que estorbe a una persona de verdad es peor que el robot."""
    for numero in range(5):
        respuesta = client.post(
            reverse("sitio:portada"), {**BUENO, "telefono": f"0414555{numero:04d}"}
        )
        assert respuesta.status_code == 302, f"el envio {numero + 1} se bloqueo"

    assert Contacto.objects.count() == 5
