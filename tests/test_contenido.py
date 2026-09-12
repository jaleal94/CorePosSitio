"""Que la pagina diga lo que tiene que decir, y como.

La tentacion constante de quien escribe esto es describir el sistema por dentro:
modulos, kardex, multi-tenant. Son palabras que no significan nada para quien
lee la pagina, y la prueba de abajo es la unica forma de que no se cuelen a la
tercera revision.
"""

import re

import pytest
from django.urls import reverse

from sitio import contenido

pytestmark = pytest.mark.django_db

# Las palabras con las que se describe el sistema por dentro. Si una aparece en
# la pagina, es que se escribio pensando en el programa y no en quien lo usa.
VETADAS = (
    "kardex",
    "multi-tenant",
    "multitenant",
    "tenant",
    "saas",
    "backend",
    "frontend",
    "api",
    "stack",
    "deploy",
    "dashboard",
    "onboarding",
    "modulo",
    "modulos",
)


@pytest.fixture
def cuerpo(client):
    return client.get(reverse("sitio:portada")).content.decode()


def palabras_de(texto):
    return set(re.findall(r"[a-zA-Záéíóúñü-]+", texto.lower()))


# ------------------------------------------------------------- como se habla


@pytest.mark.parametrize("vetada", VETADAS)
def test_ninguna_palabra_de_programador_llega_a_la_pagina(vetada, cuerpo):
    # Se mira solo lo que se ve: las clases de estilo y los nombres de archivo
    # no son texto para nadie.
    visible = re.sub(r"<[^>]+>", " ", cuerpo)

    assert vetada not in palabras_de(visible), (
        f"La palabra '{vetada}' aparece en la pagina. Es como se describe el "
        "sistema por dentro, y no significa nada para quien lo lee. Digalo en "
        "lenguaje de comercio."
    )


@pytest.mark.parametrize(
    "fuente",
    [
        *[p.queja for p in contenido.PROBLEMAS],
        *[p.respuesta for p in contenido.PROBLEMAS],
        *[g.resuelve for g in contenido.LO_QUE_HACE],
        *[f for g in contenido.LO_QUE_HACE for f in g.funciones],
        *[p.respuesta for p in contenido.PREGUNTAS],
    ],
)
def test_el_contenido_declarado_tampoco_las_usa(fuente):
    """Se comprueba en el origen, no solo en el HTML: asi el mensaje del fallo
    señala la frase exacta que hay que reescribir."""
    encontradas = palabras_de(fuente) & set(VETADAS)

    assert not encontradas, f"'{fuente[:60]}...' usa {sorted(encontradas)}"


# ------------------------------------------------------ que este todo lo que va


@pytest.mark.parametrize(
    "ancla",
    ["problema", "como-funciona", "lo-que-hace", "verlo", "precios", "preguntas", "contacto"],
)
def test_cada_seccion_esta_en_la_pagina(ancla, cuerpo):
    assert f'id="{ancla}"' in cuerpo


def test_el_heroe_dice_que_es_y_para_quien(cuerpo):
    assert contenido.HEROE["titulo"] in cuerpo
    assert "bodegas" in cuerpo.lower()


def test_los_cinco_problemas_estan(cuerpo):
    for problema in contenido.PROBLEMAS:
        assert problema.queja in cuerpo


def test_se_dice_lo_que_el_producto_no_hace(cuerpo):
    """Callarlo cuesta tres llamadas y un cliente molesto (principio I)."""
    assert "Lo que no hace" in cuerpo
    for limite in contenido.LO_QUE_NO_HACE:
        assert limite in cuerpo


def test_hay_al_menos_seis_preguntas(cuerpo):
    assert len(contenido.PREGUNTAS) >= 6
    for pregunta in contenido.PREGUNTAS:
        assert pregunta.pregunta in cuerpo


def test_las_preguntas_incomodas_estan_respondidas():
    """Las que frenan una compra: si no estan aqui, llegan por WhatsApp igual."""
    todas = " ".join(p.pregunta.lower() for p in contenido.PREGUNTAS)

    for tema in ["luz", "internet", "datos", "ir"]:
        assert tema in todas, f"falta la pregunta sobre '{tema}'"


def test_el_boton_de_contacto_se_ve_sin_bajar(cuerpo):
    """En 360 px, la cabecera fija es lo unico visible al abrir."""
    cabecera = cuerpo.split("</header>")[0]

    assert 'href="#contacto"' in cabecera


# --------------------------------------------------------------- sin terceros


def test_nada_se_carga_desde_otro_servidor(cuerpo):
    """Principio IV y X: ni tipografias, ni bibliotecas, ni rastreadores.

    Lo que se mide es lo que el navegador **descarga al abrir la pagina**: la
    hoja de estilos, los guiones, las imagenes, los marcos. Un enlace a otro
    sitio no cuenta: es un destino al que la persona decide ir, y sin ellos no
    habria como escribirnos ni como entrar al sistema.
    """
    guiones = re.findall(r"<script[^>]+src=\"(https?://[^\"]+)\"", cuerpo)
    imagenes = re.findall(r"<img[^>]+src=\"(https?://[^\"]+)\"", cuerpo)
    marcos = re.findall(r"<iframe[^>]+src=\"(https?://[^\"]+)\"", cuerpo)
    hojas = re.findall(r"<link[^>]+href=\"(https?://[^\"]+)\"", cuerpo)
    recursos = guiones + imagenes + marcos + hojas

    assert recursos == [], f"la pagina descarga cosas de afuera: {recursos}"


def test_no_hay_guiones_en_linea(cuerpo):
    """La politica de contenido los bloquea: uno aqui deja de funcionar mudo."""
    assert "<script>" not in cuerpo
    assert not re.search(r"\bon(click|load|submit|change)=", cuerpo)


@pytest.mark.parametrize("ruta", ["/", "/gracias/", "/privacidad/"])
def test_ningun_comentario_de_plantilla_llega_al_navegador(client, ruta):
    """`{# #}` en Django es de una sola linea, y no avisa cuando no lo es.

    Un comentario de varias lineas escrito asi no se elimina: se sirve como
    texto y aparece en la pagina, arriba del todo, a la vista de cualquiera.
    Django no da ni un aviso. Esta prueba es la unica forma de enterarse.
    """
    cuerpo = client.get(ruta).content.decode()

    fugas = re.findall(r"\{#.{0,60}", cuerpo, re.S)
    assert not fugas, (
        f"Hay comentarios de plantilla visibles en {ruta}: {fugas[:2]}. "
        "Un comentario de varias lineas va en {% comment %}, no en {# #}."
    )
