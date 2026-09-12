"""La imagen que aparece cuando alguien manda el enlace por WhatsApp.

Se genera en vez de dibujarse a mano por la misma razon que las capturas: para
poder rehacerla cuando cambie el mensaje, sin depender de abrir un editor y
acordarse de las medidas.

    uv run python herramientas/imagen_de_compartir.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITIO = Path(__file__).resolve().parents[1]
DESTINO = SITIO / "static" / "img" / "compartir.png"

# La medida que esperan WhatsApp y las redes. Otra cualquiera sale recortada.
ANCHO, ALTO = 1200, 630

FONDO = (255, 255, 255)
TEXTO = (31, 36, 51)
TENUE = (98, 106, 128)
ACENTO = (79, 70, 229)


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
    imagen = Image.new("RGB", (ANCHO, ALTO), FONDO)
    lienzo = ImageDraw.Draw(imagen)

    # Una banda de color arriba: da identidad sin necesitar un logotipo que
    # todavia no existe.
    lienzo.rectangle([(0, 0), (ANCHO, 12)], fill=ACENTO)

    lienzo.text((80, 110), "Core Pos", font=tipografia(52, True), fill=ACENTO)

    for numero, linea in enumerate(["Sepa lo que tiene,", "lo que vende", "y lo que gana."]):
        lienzo.text((80, 200 + numero * 78), linea, font=tipografia(66, True), fill=TEXTO)

    lienzo.text(
        (80, 460),
        "El punto de venta para bodegas y abastos.",
        font=tipografia(34),
        fill=TENUE,
    )
    lienzo.text((80, 508), "Empiece gratis, sin tarjeta.", font=tipografia(34), fill=TENUE)

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(DESTINO, "PNG", optimize=True)
    print(f"{DESTINO.name}: {DESTINO.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
