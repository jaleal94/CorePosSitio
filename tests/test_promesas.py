"""Que el sitio no prometa nada que dejo de ser cierto.

Core Pos tenia un plan gratuito. Ya no: cuesta 19,99 $ al mes y entrar cuesta
60 $ una sola vez. El sitio prometia "gratis" y "sin tarjeta" en seis sitios
distintos, y **ninguno estaba en la seccion de precios**: el titular, la
descripcion para buscadores, la seccion de contacto, el boton de pedir la
tienda, la pagina de gracias, y una que no esta escrita en ninguna plantilla
porque son pixeles dentro de la imagen que se ve al compartir por WhatsApp.

El principio I de este proyecto es que aqui no se dice nada que no sea cierto.
Una promesa de gratis en una pagina de venta no es un texto viejo: es lo que
alguien lee justo antes de que le pasen una factura de 60 $.

Por eso esta prueba no busca en los archivos: **pide cada pagina publica al
servidor y mira lo que sale**, que es lo que la gente lee. Buscar en las
plantillas encontraria cinco de las seis y dejaria pasar la que se arma en
`contenido.py`.
"""

import ast
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.django_db

RAIZ = Path(settings.RAIZ)

# Las paginas que cualquiera puede abrir. El panel de contactos no entra: es
# nuestro, no es una promesa a nadie.
PAGINAS = ("sitio:portada", "sitio:gracias", "sitio:privacidad")

PROMESAS = (
    re.compile(r"\bgratis\b", re.I),
    re.compile(r"\bgratuit[oa]s?\b", re.I),
    re.compile(r"sin tarjeta", re.I),
    re.compile(r"sin compromiso", re.I),
    re.compile(r"\bprueb[ae]lo\b", re.I),
    re.compile(r"sin tiempo limite", re.I),
    re.compile(r"plan de entrada", re.I),
    re.compile(r"cambi[ae] de plan", re.I),
)


def texto_de(html):
    """Lo que se lee, sin etiquetas. Las clases estan llenas de palabras sueltas."""
    cuerpo = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", html)
    cuerpo = re.sub(r"<[^>]+>", " ", cuerpo)
    return re.sub(r"\s+", " ", cuerpo)


@pytest.mark.parametrize("nombre", PAGINAS)
def test_ninguna_pagina_promete_que_es_gratis(client, nombre):
    cuerpo = client.get(reverse(nombre)).content.decode()
    leible = texto_de(cuerpo)
    encontradas = [p.pattern for p in PROMESAS if p.search(leible)]
    assert not encontradas, (
        f"{nombre} sigue prometiendo: {encontradas}. Ya no hay plan gratuito ni prueba sin pagar."
    )


@pytest.mark.parametrize("nombre", PAGINAS)
def test_tampoco_lo_promete_en_lo_que_no_se_ve(client, nombre):
    """La descripcion para buscadores y las etiquetas de compartir.

    No se leen en la pagina: se leen en el resultado de Google y en la tarjeta
    que arma WhatsApp. Es donde mas gente ve el mensaje y donde menos se mira al
    cambiarlo.
    """
    cuerpo = client.get(reverse(nombre)).content.decode()
    metas = re.findall(r'<meta[^>]+content="([^"]*)"', cuerpo)
    metas.append(re.search(r"<title>(.*?)</title>", cuerpo, re.S).group(1))
    for contenido in metas:
        encontradas = [p.pattern for p in PROMESAS if p.search(contenido)]
        assert not encontradas, f"{nombre} promete {encontradas} en: {contenido[:90]}"


def frases_del_guion(ruta):
    """Todos los textos escritos en un archivo de Python.

    Se analiza el arbol y no el texto. Una expresion regular sobre el codigo
    depende de donde caigan los saltos de linea, y eso lo decide el formateador:
    la primera version de esta prueba encontraba una de las dos frases que la
    imagen dibuja, y pasaba en verde sin mirar la otra. Una prueba que no
    comprueba lo que dice que comprueba es peor que no tenerla.

    Los comentarios no estan en el arbol, asi que el que explica por que se
    quito "Empiece gratis" no se cuenta como si la dibujara.
    """
    arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    return [
        nodo.value
        for nodo in ast.walk(arbol)
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str)
    ]


def test_la_imagen_de_compartir_tampoco_lo_promete():
    """Ahi la promesa son pixeles, y ninguna prueba de texto la agarra.

    Se comprueba sobre el guion que la dibuja, que es lo unico honesto que se
    puede comprobar sin leer una imagen.
    """
    guion = RAIZ / "herramientas" / "imagen_de_compartir.py"
    frases = frases_del_guion(guion)
    assert any("bodegas y abastos" in frase for frase in frases), (
        "La prueba no esta encontrando lo que la imagen dibuja: revisela antes "
        "de confiar en que esta en verde"
    )

    for frase in frases:
        encontradas = [p.pattern for p in PROMESAS if p.search(frase)]
        assert not encontradas, f"La imagen de compartir dibuja {encontradas}: {frase!r}"
