"""Capturas, como se comparte, y lo que entienden los buscadores."""

import json
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

from sitio.contenido import CAPTURAS
from sitio.planes import PLANES

pytestmark = pytest.mark.django_db

IMAGENES = Path(settings.RAIZ) / "static" / "img"


# ------------------------------------------------------------------ capturas


@pytest.mark.parametrize("captura", CAPTURAS, ids=lambda c: c.archivo)
def test_cada_captura_existe_en_el_disco(captura):
    """El principio I: las capturas salen del sistema real, y estan."""
    archivo = IMAGENES / captura.archivo

    assert archivo.exists(), (
        f"Falta {captura.archivo}. Se generan con: "
        "uv run --project ..\\CoreAPP python herramientas/capturas.py"
    )
    assert archivo.stat().st_size > 5000, "esa imagen esta vacia o rota"


def test_las_capturas_se_ven_en_la_pagina(client):
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    for captura in CAPTURAS:
        assert captura.archivo in cuerpo, f"{captura.archivo} no se muestra"
        assert captura.pie in cuerpo, "cada captura dice que se esta viendo"


def test_ninguna_captura_dice_pendiente(client):
    """Era el unico sitio donde se le pedia al lector que creyera sin ver."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    assert "Captura pendiente" not in cuerpo


def test_las_capturas_reservan_su_espacio(client):
    """Sin la proporcion declarada, la pagina salta mientras cargan."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    for captura in CAPTURAS:
        assert captura.alto in cuerpo


def test_las_capturas_no_se_descargan_todas_de_golpe(client):
    """Quien no baja hasta la seccion no tiene por que gastar esos datos."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    assert cuerpo.count('loading="lazy"') >= len(CAPTURAS) - 1


# ------------------------------------------------------------------ compartir


@pytest.mark.parametrize("ruta", ["/", "/gracias/", "/privacidad/"])
def test_cada_pagina_publica_se_comparte_bien(client, ruta):
    """Se va a difundir por WhatsApp: sin esto, sale una direccion pelada."""
    cuerpo = client.get(ruta).content.decode()

    for etiqueta in ["og:title", "og:description", "og:image", "og:url"]:
        assert f'property="{etiqueta}"' in cuerpo, f"falta {etiqueta} en {ruta}"


def test_la_imagen_de_compartir_existe_y_tiene_la_medida_correcta():
    """Otra medida sale recortada en WhatsApp y en las redes."""
    from PIL import Image

    archivo = IMAGENES / "compartir.png"
    assert archivo.exists(), (
        "Falta la imagen de compartir. Se genera con: "
        "uv run python herramientas/imagen_de_compartir.py"
    )

    with Image.open(archivo) as imagen:
        assert imagen.size == (1200, 630)


def test_la_descripcion_de_compartir_habla_como_la_pagina(client):
    """Nada de 'software de gestion': se habla igual que en la portada."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    descripcion = re.search(r'property="og:description" content="([^"]+)"', cuerpo).group(1)

    assert "bodegas" in descripcion.lower()
    assert "software" not in descripcion.lower()


# ---------------------------------------------------------------- buscadores


def test_el_mapa_del_sitio_lista_lo_publico(client):
    cuerpo = client.get(reverse("sitio:sitemap")).content.decode()

    assert "/privacidad/" in cuerpo
    assert "</urlset>" in cuerpo


def test_el_mapa_no_expone_nada_privado(client):
    cuerpo = client.get(reverse("sitio:sitemap")).content.decode()

    for privado in ["/contactos/", "/gracias/", "/admin/"]:
        assert privado not in cuerpo, f"el mapa expone {privado}"


def test_robots_cierra_el_panel_y_apunta_al_mapa(client):
    cuerpo = client.get(reverse("sitio:robots")).content.decode()

    assert "Disallow: /contactos/" in cuerpo
    assert "Disallow: /admin/" in cuerpo
    assert "sitemap.xml" in cuerpo


@pytest.mark.parametrize("ruta", ["/gracias/"])
def test_las_paginas_que_no_van_al_buscador_lo_dicen(client, ruta):
    cuerpo = client.get(ruta).content.decode()

    assert 'name="robots" content="noindex"' in cuerpo


# ------------------------------------------------------- datos estructurados


def test_los_datos_estructurados_salen_de_la_misma_declaracion(client):
    """Escritos aparte, el buscador anunciaria un precio viejo para siempre."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    crudo = re.search(
        r'<script type="application/ld\+json"[^>]*>(.*?)</script>', cuerpo, re.S
    ).group(1)
    datos = json.loads(crudo)

    producto = datos["@graph"][0]
    assert producto["name"] == settings.MARCA["nombre"]

    ofertas = {oferta["name"]: oferta["price"] for oferta in producto["offers"]}
    for plan in PLANES:
        assert ofertas[plan.nombre] == str(plan.precio_mensual)


def test_el_bloque_de_datos_lleva_su_marca_de_un_solo_uso(client):
    """La politica prohibe los guiones en linea; este pasa por su marca."""
    respuesta = client.get(reverse("sitio:portada"))
    cuerpo = respuesta.content.decode()

    marca = re.search(r'<script type="application/ld\+json" nonce="([^"]+)"', cuerpo)
    assert marca, "el bloque no lleva marca y la politica lo bloquearia"
    assert marca.group(1) in respuesta.headers["Content-Security-Policy"]


def test_la_politica_sigue_sin_permitir_guiones_en_linea_sueltos(client):
    """La marca permite ese bloque; cualquier otro guion en linea sigue fuera."""
    politica = client.get(reverse("sitio:portada")).headers["Content-Security-Policy"]
    guiones = politica.split("script-src")[1].split(";")[0]

    assert "'unsafe-inline'" not in guiones


# ---------------------------------------------------------------- los errores


def test_la_pagina_de_no_encontrado_ofrece_salida(client):
    respuesta = client.get("/una-direccion-que-no-existe/")

    assert respuesta.status_code == 404
    cuerpo = respuesta.content.decode()
    assert "no existe" in cuerpo
    assert "wa.me" in cuerpo, "tiene que ofrecer escribirnos"
