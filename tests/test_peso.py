"""El presupuesto de peso: menos de 150 KB (principio IV).

El publico abre esto con datos moviles, en un telefono barato, con una conexion
que va y viene. Un sitio que tarda es un sitio que nadie ve, y el peso crece sin
que nadie lo note: una tipografia aqui, una biblioteca alla.

Se mide **comprimido**, que es como viaja por la red. Medir el archivo sin
comprimir seria medir algo que nadie descarga.
"""

import gzip
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.peso

PRESUPUESTO_KB = 150

RAIZ_ESTATICA = Path(settings.RAIZ) / "static"


# Las imagenes ya vienen comprimidas: volver a comprimirlas no las achica y
# mediria algo que el servidor no hace.
YA_COMPRIMIDOS = {".webp", ".png", ".jpg", ".jpeg", ".avif"}


def comprimido(ruta):
    crudo = ruta.read_bytes()
    if ruta.suffix.lower() in YA_COMPRIMIDOS:
        return len(crudo)
    return len(gzip.compress(crudo, 9))


def recursos_de_la_portada(cuerpo):
    """Lo que el navegador descarga **al abrir** la pagina.

    Las imagenes marcadas para cargar mas tarde no cuentan: solo se descargan si
    la persona baja hasta ellas, y quien no baja no paga esos datos. Contarlas
    aqui seria medir algo que no le pasa a casi nadie.
    """
    rutas = re.findall(r'<link[^>]+href="/static/([^"]+)"', cuerpo)
    rutas += re.findall(r'<script[^>]+src="/static/([^"]+)"', cuerpo)

    for etiqueta in re.findall(r"<img[^>]+>", cuerpo):
        if 'loading="lazy"' in etiqueta:
            continue
        encontrada = re.search(r'src="/static/([^"]+)"', etiqueta)
        if encontrada:
            rutas.append(encontrada.group(1))

    return [RAIZ_ESTATICA / ruta for ruta in rutas]


@pytest.mark.django_db
def test_la_primera_carga_cabe_en_el_presupuesto(client):
    respuesta = client.get(reverse("sitio:portada"))
    cuerpo = respuesta.content.decode()

    recursos = recursos_de_la_portada(cuerpo)
    assert recursos, "la pagina no carga ningun estatico: algo se rompio"

    detalle = {ruta.name: comprimido(ruta) for ruta in recursos}
    detalle["la pagina"] = len(gzip.compress(respuesta.content, 9))
    total = sum(detalle.values())

    assert total < PRESUPUESTO_KB * 1024, (
        f"la primera carga pesa {total / 1024:.0f} KB comprimidos y el presupuesto "
        f"es {PRESUPUESTO_KB} KB. Reparto: "
        + ", ".join(f"{n} {p / 1024:.0f} KB" for n, p in sorted(detalle.items()))
    )


@pytest.mark.django_db
def test_la_pagina_sola_es_liviana(client):
    """El HTML es lo unico que no se puede cachear entre visitas."""
    respuesta = client.get(reverse("sitio:portada"))

    pesa = len(gzip.compress(respuesta.content, 9))
    assert pesa < 25 * 1024, f"el HTML pesa {pesa / 1024:.0f} KB comprimidos"


def test_no_se_carga_ninguna_tipografia():
    """La del sistema carga en cero y se ve bien en todos lados."""
    hoja = (RAIZ_ESTATICA / "css" / "sitio.css").read_text(encoding="utf-8")

    assert "@font-face" not in hoja
    assert not list((RAIZ_ESTATICA).glob("**/*.woff*"))
