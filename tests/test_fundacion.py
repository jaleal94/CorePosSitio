"""Lo minimo que tiene que ser cierto desde el primer dia.

La suite arranca comprobando las promesas de la constitucion que ya se pueden
comprobar: que el sitio levanta, que nada viene de otro servidor, y que la
marca vive en un solo lugar.
"""

import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_la_portada_responde(client):
    respuesta = client.get(reverse("sitio:portada"))

    assert respuesta.status_code == 200


def test_la_marca_llega_a_la_plantilla(client):
    """Principio: el nombre vive en la configuracion, no repartido (D3)."""
    respuesta = client.get(reverse("sitio:portada"))

    assert settings.MARCA["nombre"].encode() in respuesta.content


def test_la_politica_de_contenido_no_deja_entrar_nada_de_afuera(client):
    """Principio IV: ningun recurso de otro servidor, ni rastreadores."""
    respuesta = client.get(reverse("sitio:portada"))
    politica = respuesta.headers["Content-Security-Policy"]

    assert "default-src 'self'" in politica
    assert "'unsafe-inline'" not in politica.split("script-src")[1].split(";")[0]


def test_la_hoja_de_estilos_existe_y_es_local():
    """Si no esta compilada, el sitio se ve roto y nadie se entera hasta produccion."""
    hoja = settings.RAIZ / "static" / "css" / "sitio.css"

    assert hoja.exists(), "falta compilar static/css/sitio.css con tailwindcss"
    assert hoja.stat().st_size > 0
