"""Genera los archivos del logo del sitio, desde el mismo original que el producto.

El original de la marca vive en Core Pos, en `assets/marca/logo.png`, y de ahi
salen tambien los archivos del producto. Tener una sola copia es a proposito: si
hubiera dos, el dia que alguien reemplace una se quedaria la otra, y el sitio y
el sistema se verian de dos empresas parecidas.

Por la misma razon esto no reimplementa el recorte ni la limpieza: importa las
del producto. La herramienta de alla es la que sabe como esta armado el archivo.

Produce:

    static/img/logo-marca.png    solo la C y la flecha, para la cabecera
    static/img/logo.png          la marca completa, para el pie
    static/img/favicon.png       el icono de la pestana
    static/img/icono-180.png     el icono de la pantalla de inicio

Correr con el producto al lado:

    uv run python herramientas/marca.py

Si el producto esta en otro sitio:  CORE_POS_REPO=D:\\ruta\\CoreAPP
"""

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "static" / "img"

# Donde buscar el producto. Por omision, la carpeta hermana; la misma
# convencion que usa tests/test_precios.py.
PRODUCTO = Path(os.environ.get("CORE_POS_REPO", RAIZ.parent / "CoreAPP"))


def main():
    if not (PRODUCTO / "herramientas" / "marca.py").exists():
        raise SystemExit(
            f"No se encontro Core Pos en {PRODUCTO}.\n"
            "Indique donde esta con la variable CORE_POS_REPO."
        )

    sys.path.insert(0, str(PRODUCTO / "herramientas"))
    import marca as producto
    from PIL import Image

    original = Image.open(producto.ORIGINAL).convert("RGBA")
    plano = producto._plano(original)
    bandas = producto._bandas(plano)
    arriba = bandas[0]

    solo_marca = original.crop(
        producto._caja_con_tinta(plano, (0, arriba[0], original.width, arriba[1] + 1))
    )
    completo = original.crop(
        producto._caja_con_tinta(plano, (0, 0, original.width, original.height))
    )
    producto._sin_ruido(solo_marca)
    producto._sin_ruido(completo)

    DESTINO.mkdir(parents=True, exist_ok=True)
    producto._paleta_corta(solo_marca).save(DESTINO / "logo-marca.png", "PNG", optimize=True)
    producto._paleta_corta(completo).save(DESTINO / "logo.png", "PNG", optimize=True)
    producto._paleta_corta(producto._sobre_blanco(solo_marca, 48, 3)).save(
        DESTINO / "favicon.png", "PNG", optimize=True
    )
    producto._paleta_corta(producto._sobre_blanco(solo_marca, 180, 18)).save(
        DESTINO / "icono-180.png", "PNG", optimize=True
    )

    for archivo in ("logo-marca.png", "logo.png", "favicon.png", "icono-180.png"):
        ruta = DESTINO / archivo
        imagen = Image.open(ruta)
        medidas = f"{imagen.width:>4} x {imagen.height:<4}"
        print(f"  {archivo:<18} {medidas} {ruta.stat().st_size:>6} bytes")


if __name__ == "__main__":
    main()
