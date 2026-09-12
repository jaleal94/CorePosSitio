"""La imagen que aparece cuando alguien manda el enlace por WhatsApp.

Se genera en vez de dibujarse a mano por la misma razon que las capturas: para
poder rehacerla cuando cambie el mensaje o la paleta, sin depender de abrir un
editor y acordarse de las medidas.

Los colores se leen de `assets/tailwind.css` y no se escriben aqui. Cuando esto
tenia sus propias cifras se quedo con el indigo viejo mientras el sitio ya era
azul marino: la imagen que mas gente ve acaba siendo la que nadie vuelve a
mirar.

    uv run python herramientas/imagen_de_compartir.py
"""

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITIO = Path(__file__).resolve().parents[1]
HOJA = SITIO / "assets" / "tailwind.css"
LOGO = SITIO / "static" / "img" / "logo.png"
DESTINO = SITIO / "static" / "img" / "compartir.png"

# La medida que esperan WhatsApp y las redes. Otra cualquiera sale recortada.
ANCHO, ALTO = 1200, 630

BLANCO = (255, 255, 255)


def paleta():
    """Los colores del bloque @theme, para no tener aqui una segunda copia."""
    bloque = re.search(r"@theme\s*\{(.*?)\n\}", HOJA.read_text(encoding="utf-8"), re.S)
    if not bloque:
        raise SystemExit("No se encontro el bloque @theme en assets/tailwind.css")
    return {
        nombre: tuple(int(valor[i : i + 2], 16) for i in (1, 3, 5))
        for nombre, valor in re.findall(
            r"--color-([a-z-]+):\s*(#[0-9a-fA-F]{6})\s*;", bloque.group(1)
        )
    }


def tipografia(tamano, negrita=False):
    """La del sistema. Si no esta, la de reserva: es una imagen, no un texto."""
    candidatas = ["segoeuib.ttf" if negrita else "segoeui.ttf", "arialbd.ttf", "arial.ttf"]
    for nombre in candidatas:
        try:
            return ImageFont.truetype(nombre, tamano)
        except OSError:
            continue
    return ImageFont.load_default(tamano)


def main():
    colores = paleta()

    imagen = Image.new("RGB", (ANCHO, ALTO), BLANCO)
    lienzo = ImageDraw.Draw(imagen)

    # Una banda arriba, del azul de la marca.
    lienzo.rectangle([(0, 0), (ANCHO, 12)], fill=colores["marca"])

    # El logo a la derecha, a su tamano nativo: ampliarlo lo emborrona, y una
    # marca borrosa se lee como un negocio improvisado.
    logo = Image.open(LOGO).convert("RGBA")
    imagen.paste(logo, (ANCHO - 110 - logo.width, (ALTO - logo.height) // 2), logo)

    for numero, linea in enumerate(["Sepa lo que tiene,", "lo que vende", "y lo que gana."]):
        lienzo.text(
            (80, 150 + numero * 78), linea, font=tipografia(66, True), fill=colores["texto"]
        )

    lienzo.text(
        (80, 420),
        "El punto de venta para bodegas y abastos.",
        font=tipografia(34),
        fill=colores["tenue"],
    )
    lienzo.text(
        (80, 468), "Empiece gratis, sin tarjeta.", font=tipografia(34), fill=colores["tenue"]
    )

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(DESTINO, "PNG", optimize=True)
    print(f"{DESTINO.name}: {DESTINO.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
