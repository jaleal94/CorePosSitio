"""Que el sitio se vea de alguien, y que se vea del mismo que el producto.

Cambiar colores parece trivial y no lo es: se toca todo y no hay forma de
revisarlo mirando. El principio VII dice que lo que se afirma se prueba, y aqui
lo que se afirma es que el sitio se lee bien y que es la misma marca que el
sistema. Las dos cosas se calculan:

- el contraste de cada par de texto y fondo que el sitio pinta de verdad,
- que la paleta sea la misma que la de Core Pos, leida de su propia hoja,
- que el verde de la marca y el que informa sigan siendo dos colores,
- que el logo este, se enlace y tenga texto alternativo.

Sin esto, la unica forma de saberlo es abrir una herramienta y mirar, que es
justo lo que nadie hace cuando cambia un tono "un poquito".
"""

import math
import os
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse

RAIZ = Path(settings.RAIZ)
HOJA = RAIZ / "assets" / "tailwind.css"
PLANTILLAS = RAIZ / "templates"
IMAGENES = RAIZ / "static" / "img"

# Donde buscar el producto. La misma convencion que test_precios.py.
PRODUCTO = Path(os.environ.get("CORE_POS_REPO", RAIZ.parent / "CoreAPP"))
HOJA_DEL_PRODUCTO = PRODUCTO / "assets" / "tailwind.css"

TEXTO_NORMAL = 4.5
TEXTO_GRANDE = 3.0
NO_TEXTO = 3.0  # bordes de controles y graficos (1.4.11)

BLANCO = "#FFFFFF"
LOGOS = ("logo.png", "logo-marca.png", "favicon.png", "icono-180.png")

# El PNG de paleta corta mueve cada canal como mucho una unidad. Lo que esta
# tolerancia busca no es esa unidad: es que el logo y la hoja dejen de ser el
# mismo color.
DERIVA = 3.0


# ------------------------------------------------------------------ la paleta


def paleta_de(hoja):
    """Los colores del bloque @theme de una hoja, sea la de aqui o la de alla."""
    bloque = re.search(r"@theme\s*\{(.*?)\n\}", hoja.read_text(encoding="utf-8"), re.S)
    assert bloque, f"No se encontro el bloque @theme en {hoja}"
    colores = dict(re.findall(r"--color-([a-z-]+):\s*(#[0-9a-fA-F]{6})\s*;", bloque.group(1)))
    assert colores, f"{hoja} no declara ningun color en hexadecimal"
    return colores


PALETA = paleta_de(HOJA)


def _rgb(valor):
    valor = valor.lstrip("#")
    return tuple(int(valor[i : i + 2], 16) for i in (0, 2, 4))


def _luminancia(valor):
    def canal(v):
        v = v / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    rojo, verde, azul = (canal(x) for x in _rgb(valor))
    return 0.2126 * rojo + 0.7152 * verde + 0.0722 * azul


def contraste(uno, otro):
    a, b = _luminancia(uno), _luminancia(otro)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def color(nombre):
    assert nombre in PALETA, f"La paleta no declara --color-{nombre}"
    return PALETA[nombre]


def _valor(nombre):
    return nombre if nombre.startswith("#") else color(nombre)


# ----------------------------------------------------------------- contraste

PARES = [
    ("texto", "lienzo", TEXTO_NORMAL, "el cuerpo de la pagina"),
    ("texto", "superficie", TEXTO_NORMAL, "el cuerpo dentro de una ficha"),
    ("tenue", "lienzo", TEXTO_NORMAL, "los subtitulos y el pie"),
    ("tenue", "superficie", TEXTO_NORMAL, "los subtitulos dentro de una ficha"),
    ("tenue", "acento-suave", TEXTO_NORMAL, "el texto de relleno de los campos"),
    ("acento-fuerte", "superficie", TEXTO_NORMAL, "los enlaces"),
    ("acento-fuerte", "lienzo", TEXTO_NORMAL, "los enlaces sobre el fondo"),
    ("acento-fuerte", "acento-suave", TEXTO_NORMAL, "el menu con el puntero encima"),
    (BLANCO, "acento", TEXTO_NORMAL, "el boton de Quiero probarlo"),
    (BLANCO, "acento-fuerte", TEXTO_NORMAL, "ese boton con el puntero encima"),
    ("sana", "superficie", TEXTO_NORMAL, "las marcas de lo que si trae el plan"),
    ("sana", "lienzo", TEXTO_NORMAL, "esas marcas sobre el fondo"),
    ("atencion", "superficie", TEXTO_NORMAL, "el error de un campo"),
    ("atencion", "lienzo", TEXTO_NORMAL, "las quejas entrecomilladas"),
    ("marca", "superficie", TEXTO_NORMAL, "el nombre de la marca"),
    ("marca-verde", "marca", NO_TEXTO, "la flecha del logo sobre la C"),
    ("borde-fuerte", "superficie", NO_TEXTO, "el borde de los campos"),
    ("borde-fuerte", "lienzo", NO_TEXTO, "el borde de los campos sobre el fondo"),
]


@pytest.mark.parametrize("frente,fondo,minimo,donde", PARES, ids=[p[3] for p in PARES])
def test_cada_par_de_color_llega_al_minimo(frente, fondo, minimo, donde):
    razon = contraste(_valor(frente), _valor(fondo))
    assert razon >= minimo, (
        f"{frente} sobre {fondo} da {razon:.2f}:1 y hace falta {minimo}:1 ({donde})"
    )


@pytest.mark.parametrize("fondo", ("lienzo", "superficie", "acento-suave"))
def test_el_anillo_de_foco_se_ve_sobre_todos_los_fondos(fondo):
    """Hay quien navega el formulario con el tabulador. Si el foco no se ve, no se llena."""
    razon = contraste(color("acento"), color(fondo))
    assert razon >= NO_TEXTO, f"El anillo de foco sobre {fondo} da {razon:.2f}:1"


# ------------------------------------------------- la misma marca que alla


def test_la_paleta_es_la_misma_que_la_del_producto():
    """Quien llega aqui y despues entra al sistema tiene que reconocer que es lo mismo.

    Se lee la hoja del producto, no una copia: una copia comprobaria que la
    copia esta bien mientras el producto usa otra cosa.
    """
    if not HOJA_DEL_PRODUCTO.exists():
        pytest.skip(f"Core Pos no esta en {PRODUCTO}; indique CORE_POS_REPO")

    del_producto = paleta_de(HOJA_DEL_PRODUCTO)
    distintos = {
        nombre: (valor, del_producto[nombre])
        for nombre, valor in PALETA.items()
        if nombre in del_producto and valor.upper() != del_producto[nombre].upper()
    }
    assert not distintos, "El sitio y el producto pintan distinto:\n" + "\n".join(
        f"  {nombre}: aqui {aqui}, alla {alla}" for nombre, (aqui, alla) in distintos.items()
    )


def test_los_colores_de_la_marca_estan_declarados():
    """Son los tres del archivo del logo, y de ahi sale todo lo demas."""
    for nombre in ("marca", "marca-verde", "marca-texto"):
        assert nombre in PALETA, f"Falta --color-{nombre}"


def test_el_verde_de_la_marca_y_el_que_informa_son_dos_colores():
    """Dos nombres a proposito: cambiar la marca no puede cambiar lo que informa."""
    assert color("marca-verde") != color("sana")


# ------------------------------------------------- ningun color fuera de sitio

FAMILIAS = (
    "slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|"
    "teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
)
CLASE_DE_FABRICA = re.compile(
    rf"\b(?:bg|text|border|ring|fill|stroke|divide|from|via|to)-(?:{FAMILIAS})-\d{{2,3}}\b"
)
HEXADECIMAL = re.compile(r"#[0-9a-fA-F]{6}\b")


def plantillas():
    return sorted(PLANTILLAS.rglob("*.html"))


def test_ninguna_plantilla_usa_un_color_de_fabrica_de_tailwind():
    """El indigo de antes, y cualquier otro que se cuele."""
    culpables = []
    for plantilla in plantillas():
        for hallazgo in CLASE_DE_FABRICA.findall(plantilla.read_text(encoding="utf-8")):
            culpables.append(f"{plantilla.relative_to(RAIZ)}: {hallazgo}")
    assert not culpables, "Colores de fuera de la paleta:\n" + "\n".join(culpables)


def test_ninguna_plantilla_escribe_un_color_a_mano():
    permitidos = {v.upper() for v in PALETA.values()} | {"#FFFFFF", "#000000"}
    culpables = []
    for plantilla in plantillas():
        for hallazgo in HEXADECIMAL.findall(plantilla.read_text(encoding="utf-8")):
            if hallazgo.upper() not in permitidos:
                culpables.append(f"{plantilla.relative_to(RAIZ)}: {hallazgo}")
    assert not culpables, "Colores escritos a mano:\n" + "\n".join(culpables)


# ---------------------------------------------------------------------- logo


@pytest.mark.parametrize("archivo", LOGOS)
def test_el_logo_existe_y_pesa_poco(archivo):
    ruta = IMAGENES / archivo
    assert ruta.exists(), f"Falta static/img/{archivo}"
    assert ruta.stat().st_size < 8_000, f"{archivo} pesa {ruta.stat().st_size} bytes"


@pytest.mark.parametrize("archivo", ("logo.png", "logo-marca.png"))
def test_el_logo_esta_pintado_con_los_colores_de_la_paleta(archivo):
    """Se miran los colores que cubren superficie, no los del contorno."""
    from PIL import Image

    imagen = Image.open(IMAGENES / archivo).convert("RGBA")
    de_marca = [
        _rgb(color("marca")),
        _rgb(color("marca-verde")),
        _rgb(color("marca-texto")),
        (0x58, 0x59, 0x5B),  # el gris de "Pos"
        (255, 255, 255),
    ]
    minimo = 0.01 * imagen.width * imagen.height
    solidos = [
        (rojo, verde, azul)
        for cuantos, (rojo, verde, azul, alfa) in imagen.getcolors(maxcolors=1_000_000)
        if alfa >= 250 and cuantos >= minimo
    ]
    assert solidos, f"{archivo} no tiene ninguna zona de color solida"
    for tono in solidos:
        cerca = min(math.dist(tono, referencia) for referencia in de_marca)
        assert cerca <= DERIVA, f"{archivo} pinta {tono}, que no es un color de la marca"


@pytest.mark.parametrize("archivo", LOGOS)
def test_el_logo_es_el_mismo_archivo_que_el_del_producto(archivo):
    """Byte a byte. Que sean parecidos no basta: tiene que ser el mismo."""
    alla = PRODUCTO / "static" / "img" / archivo
    if not alla.exists():
        pytest.skip(f"Core Pos no esta en {PRODUCTO}; indique CORE_POS_REPO")
    assert (IMAGENES / archivo).read_bytes() == alla.read_bytes(), (
        f"{archivo} no es el mismo archivo que el del producto; "
        "vuelva a correr herramientas/marca.py"
    )


# ---------------------------------------------------------- ya en la pagina


@pytest.mark.django_db
def test_la_portada_muestra_el_logo(client):
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    assert "img/logo-marca.png" in cuerpo, "Falta la marca en la cabecera"
    assert "img/logo.png" in cuerpo, "Falta la marca en el pie"
    assert "img/favicon.png" in cuerpo, "Falta el icono de la pestana"


@pytest.mark.django_db
def test_el_logo_no_repite_el_nombre_para_quien_no_lo_ve(client):
    """En la cabecera el nombre ya esta escrito al lado: oirlo dos veces estorba."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    cabecera = cuerpo[cuerpo.find("<header") : cuerpo.find("</header>")]
    marca = re.search(r"<img[^>]*logo-marca\.png[^>]*>", cabecera)
    assert marca, "La cabecera no trae la marca"
    assert 'alt=""' in marca.group(0), "La marca de la cabecera tiene que ser decorativa"


@pytest.mark.django_db
def test_toda_imagen_de_la_portada_tiene_texto_alternativo(client):
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    for etiqueta in re.findall(r"<img[^>]*>", cuerpo):
        assert "alt=" in etiqueta, f"Imagen sin texto alternativo: {etiqueta[:80]}"


@pytest.mark.django_db
def test_el_logo_se_sirve_desde_el_sitio(client):
    """Principio X: nada de otro servidor, tampoco la marca."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()
    for direccion in re.findall(r'<img[^>]+src="([^"]+)"', cuerpo):
        assert direccion.startswith("/static/"), f"La imagen se pide a {direccion}"
