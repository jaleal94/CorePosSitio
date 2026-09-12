"""Genera las capturas del sitio, desde Core Pos de verdad.

El principio I dice que las capturas salen del sistema real. Este guion es lo
que hace que eso sea sostenible: una captura tomada a mano no se puede rehacer,
y una captura que no se puede rehacer envejece hasta que miente.

**Core Pos se usa como biblioteca: se lee, no se toca.** El guion agrega su
carpeta al camino de importacion, apunta la base de datos a una propia por
variable de entorno, y se ejecuta con el entorno del producto:

    uv run --project ..\\CoreAPP python herramientas/capturas.py

Las pantallas exigen sesion iniciada. En vez de pelear con un navegador sin
cabeza y sus galletas, se usa el cliente de pruebas de Django —que si sabe
iniciar sesion— para obtener el HTML ya renderizado, se guarda en disco con las
rutas de los estaticos apuntando al disco, y **eso** es lo que fotografia el
navegador. Es mas simple y no necesita que el servidor este levantado.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import uuid
from decimal import Decimal
from pathlib import Path

SITIO = Path(__file__).resolve().parents[1]
PRODUCTO = Path(os.environ.get("CORE_POS_REPO", SITIO.parent / "CoreAPP"))
DESTINO = SITIO / "static" / "img"

# Base propia, creada y tirada por este guion. La del desarrollo no se toca.
BASE_DEMO = "coreapp_demo"

NAVEGADORES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]

# Que se fotografia, con que tamaño y a que archivo. El cobro va en proporcion
# de telefono porque es donde se cobra, de pie en el mostrador.
PANTALLAS = [
    {"ruta": "/vender/", "archivo": "cobro.png", "ancho": 420, "alto": 860},
    {"ruta": "/panel/", "archivo": "panel.png", "ancho": 1100, "alto": 800},
    {"ruta": "/inventario/", "archivo": "inventario.png", "ancho": 1100, "alto": 800},
]


# --------------------------------------------------------------- preparacion


def arrancar_django():
    """Carga Core Pos apuntando a la base de la demostracion."""
    sys.path.insert(0, str(PRODUCTO))
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.dev"

    import environ

    lector = environ.Env()
    environ.Env.read_env(PRODUCTO / ".env")
    # Se redirige la base **antes** de que Django lea la configuracion. El
    # lector del producto no pisa lo que ya esta en el entorno, asi que esto
    # manda.
    os.environ["DATABASE_URL"] = re.sub(r"/[^/]+$", f"/{BASE_DEMO}", lector("DATABASE_URL"))

    import django

    django.setup()

    # El cliente de pruebas se presenta como `testserver`. Se permite aqui, en
    # memoria y solo mientras corre este guion: la configuracion del producto no
    # se toca.
    from django.conf import settings

    if "testserver" not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, "testserver"]


def crear_base():
    import psycopg
    from django.conf import settings

    url = settings.DATABASES["default"]
    administrativa = (
        f"postgres://{url['USER']}:{url['PASSWORD']}@{url['HOST']}:{url['PORT']}/postgres"
    )
    with psycopg.connect(administrativa, autocommit=True) as cx:
        cx.execute(f'DROP DATABASE IF EXISTS "{BASE_DEMO}" WITH (FORCE)')
        cx.execute(f'CREATE DATABASE "{BASE_DEMO}"')
    print(f"  base '{BASE_DEMO}' creada de cero")

    from django.core.management import call_command

    call_command("migrate", verbosity=0)
    print("  migraciones aplicadas")


# ------------------------------------------------------------ la bodega falsa

# Nombres de una bodega venezolana inventada. Se reconocen como ejemplo y al
# mismo tiempo se ven creibles: unos datos de mentira evidente restan tanta
# confianza como unos datos reales.
PRODUCTOS = [
    ("HAR001", "Harina P.A.N. 1 kg", "3.20", "2.45", 48),
    ("ARR001", "Arroz Primor 1 kg", "2.10", "1.60", 62),
    ("ACE001", "Aceite Vatel 1 L", "4.50", "3.60", 24),
    ("AZU001", "Azucar Montalban 1 kg", "1.90", "1.45", 35),
    ("PAS001", "Pasta Ronco 1 kg", "2.40", "1.85", 40),
    ("CAF001", "Cafe Fama de America 200 g", "3.80", "3.00", 18),
    ("MAL001", "Malta Maltin Polar 355 ml", "1.10", "0.80", 96),
    ("LEC001", "Leche en polvo 400 g", "5.60", "4.50", 12),
    ("MAR001", "Margarina Mavesa 500 g", "2.80", "2.20", 15),
    ("PAP001", "Papel higienico 4 rollos", "3.40", "2.70", 8),
    ("JAB001", "Jabon azul panela", "1.20", "0.85", 30),
    ("DET001", "Detergente Las Llaves 1 kg", "2.60", "2.05", 6),
]


def sembrar():
    """Una bodega con catalogo, inventario y un dia de ventas."""
    import datetime

    from apps.caja.servicios import abrir_sesion
    from apps.catalogo.models import Categoria, Producto
    from apps.configuracion.models import Alicuota, Serie, TipoDeSerie
    from apps.configuracion.servicios import cargar_tasa
    from apps.cuentas.models import Usuario
    from apps.inventario.servicios import registrar_movimiento
    from apps.inventario.tipos import TipoMovimiento
    from apps.tiendas.models import Membresia, Tienda
    from apps.tiendas.permisos import Rol
    from apps.ventas.metodos import MetodoPago
    from apps.ventas.servicios import agregar_al_carrito, carrito_de, confirmar_venta
    from django_scopes import scope

    tienda = Tienda.objects.create(
        codigo="la-milagrosa",
        nombre_comercial="Bodega La Milagrosa",
        identificacion_fiscal="J405558881",
        moneda_referencia="USD",
        moneda_cobro="VES",
    )
    duena = Usuario.objects.crear_con_correo(
        correo="duena@lamilagrosa.test", nombre_completo="Carmen Rodriguez", clave=uuid.uuid4().hex
    )
    Membresia.objects.create(usuario=duena, tienda=tienda, rol=Rol.ADMIN)

    with scope(tienda=tienda):
        Alicuota.objects.create(
            tienda=tienda, nombre="Exento", porcentaje=0, es_predeterminada=True
        )
        Serie.objects.create(tienda=tienda, tipo=TipoDeSerie.VENTA, prefijo="V")
        Serie.objects.create(tienda=tienda, tipo=TipoDeSerie.PRODUCTO, prefijo="P")
        cargar_tasa(tienda=tienda, valor=Decimal("38.50"), autor=duena)

        viveres = Categoria.objects.create(tienda=tienda, nombre="Viveres")
        limpieza = Categoria.objects.create(tienda=tienda, nombre="Limpieza")

        creados = []
        for codigo, nombre, precio, costo, existencia in PRODUCTOS:
            producto = Producto.objects.create(
                tienda=tienda,
                codigo=codigo,
                nombre=nombre,
                categoria=limpieza if codigo[:3] in ("JAB", "DET", "PAP") else viveres,
                precio=Decimal(precio),
                costo_referencia=Decimal(costo),
                punto_reorden=Decimal("10"),
            )
            registrar_movimiento(
                tienda=tienda,
                producto=producto,
                tipo=TipoMovimiento.ENTRADA_COMPRA,
                cantidad=Decimal(existencia),
                costo_unitario=Decimal(costo),
                autor=duena,
            )
            creados.append(producto)

        abrir_sesion(tienda=tienda, usuario=duena, fondos={"USD": "20", "VES": "800"})

        # Un dia de ventas, para que el panel tenga numeros que enseñar.
        hoy = datetime.date.today()
        for numero, (indices, cantidades) in enumerate(
            [
                ([0, 6], [2, 3]),
                ([1, 3, 4], [1, 1, 2]),
                ([5, 6], [1, 6]),
                ([0, 2, 8], [3, 1, 1]),
                ([10, 6], [2, 2]),
                ([4, 1], [2, 3]),
            ]
        ):
            carrito = carrito_de(tienda, duena)
            for indice, cantidad in zip(indices, cantidades, strict=True):
                agregar_al_carrito(
                    carrito=carrito, producto=creados[indice], cantidad=Decimal(cantidad)
                )
            total = carrito.total
            confirmar_venta(
                tienda=tienda,
                carrito=carrito,
                pagos=[{"metodo": MetodoPago.EFECTIVO, "moneda": "USD", "monto": str(total)}],
                autor=duena,
                clave_idempotencia=f"demo-{numero}",
            )

        # Un carrito a medio cobrar, que es como se ve la pantalla de venta en
        # el momento en que alguien la mira por encima del hombro.
        carrito = carrito_de(tienda, duena)
        agregar_al_carrito(carrito=carrito, producto=creados[0], cantidad=Decimal("2"))
        agregar_al_carrito(carrito=carrito, producto=creados[6], cantidad=Decimal("4"))
        agregar_al_carrito(carrito=carrito, producto=creados[5], cantidad=Decimal("1"))

        # Que se vea un aviso de reposicion: es parte de lo que se vende.
        registrar_movimiento(
            tienda=tienda,
            producto=creados[11],
            tipo=TipoMovimiento.SALIDA_VENTA,
            cantidad=Decimal("4"),
            autor=duena,
        )
        print(f"  {len(creados)} productos, {hoy:%d/%m} con 6 ventas y un carrito abierto")

    return tienda, duena


# ------------------------------------------------------------- el renderizado


def renderizar(tienda, duena, carpeta):
    """Guarda el HTML de cada pantalla, con los estaticos apuntando al disco."""
    from django.test import Client
    from django_scopes import scope

    cliente = Client()
    cliente.force_login(duena, backend="apps.cuentas.autenticacion.BackendCorreoONombreUsuario")

    estaticos = (PRODUCTO / "static").as_uri()
    archivos = []

    with scope(tienda=tienda):
        for pantalla in PANTALLAS:
            respuesta = cliente.get(pantalla["ruta"], follow=True)
            if respuesta.status_code != 200:
                raise SystemExit(
                    f"{pantalla['ruta']} respondio {respuesta.status_code}; no se puede capturar"
                )

            html = respuesta.content.decode()
            # Las rutas del servidor no existen en un archivo suelto: se
            # apuntan al disco para que el navegador encuentre los estilos.
            html = html.replace('"/static/', f'"{estaticos}/')
            # Core Pos sirve dos comentarios de plantilla como texto visible
            # -son `{# #}` de varias lineas, que Django no elimina-. Se quitan
            # de la captura para no fotografiar un defecto suyo. Esta linea
            # sobra el dia que el producto lo corrija.
            html = re.sub(r"\{#(?:[^#]|#(?!\}))*#\}", "", html)
            destino = carpeta / f"{pantalla['archivo']}.html"
            destino.write_text(html, encoding="utf-8")
            archivos.append((destino, pantalla))
            print(f"  renderizada {pantalla['ruta']}")

    return archivos


def navegador():
    for ruta in NAVEGADORES:
        if ruta.exists():
            return ruta
    raise SystemExit(
        "No se encontro Edge ni Chrome. Hacen falta solo para generar las "
        "capturas, no para servir el sitio."
    )


def fotografiar(archivos, carpeta):
    """Fotografia cada HTML con el navegador sin cabeza."""
    ejecutable = navegador()
    crudas = []

    for archivo, pantalla in archivos:
        salida = carpeta / f"cruda-{pantalla['archivo']}"
        subprocess.run(
            [
                str(ejecutable),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--window-size={pantalla['ancho']},{pantalla['alto']}",
                f"--screenshot={salida}",
                archivo.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        crudas.append((salida, pantalla))
        print(f"  fotografiada {pantalla['archivo']}")

    return crudas


def optimizar(crudas):
    """Redimensiona y comprime: las imagenes entran al presupuesto de peso."""
    from PIL import Image

    DESTINO.mkdir(parents=True, exist_ok=True)
    for cruda, pantalla in crudas:
        with Image.open(cruda) as imagen:
            imagen = imagen.convert("RGB")
            # El doble del ancho que ocupa en pantalla: se ve nitido en
            # telefonos de pantalla densa sin pesar el doble de lo necesario.
            ancho_final = min(imagen.width, 900)
            proporcion = ancho_final / imagen.width
            imagen = imagen.resize((ancho_final, int(imagen.height * proporcion)), Image.LANCZOS)
            destino = DESTINO / pantalla["archivo"].replace(".png", ".webp")
            imagen.save(destino, "WEBP", quality=78, method=6)
            print(f"  {destino.name}: {destino.stat().st_size / 1024:.0f} KB")


# ------------------------------------------------------------------- entrada


def main():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument(
        "--conservar-base",
        action="store_true",
        help="No borra la base de la demostracion al terminar.",
    )
    opciones = analizador.parse_args()

    if not PRODUCTO.exists():
        raise SystemExit(
            f"No se encontro Core Pos en {PRODUCTO}. Ponga CORE_POS_REPO apuntando a su carpeta."
        )

    print("Cargando Core Pos como biblioteca...")
    arrancar_django()

    print("Preparando la base de la demostracion...")
    crear_base()

    print("Sembrando la bodega de ejemplo...")
    tienda, duena = sembrar()

    with tempfile.TemporaryDirectory() as temporal:
        carpeta = Path(temporal)
        print("Renderizando las pantallas...")
        archivos = renderizar(tienda, duena, carpeta)
        print("Fotografiando...")
        crudas = fotografiar(archivos, carpeta)
        print("Optimizando...")
        optimizar(crudas)

    if not opciones.conservar_base:
        import psycopg
        from django.conf import settings
        from django.db import connections

        connections.close_all()
        url = settings.DATABASES["default"]
        administrativa = (
            f"postgres://{url['USER']}:{url['PASSWORD']}@{url['HOST']}:{url['PORT']}/postgres"
        )
        with psycopg.connect(administrativa, autocommit=True) as cx:
            cx.execute(f'DROP DATABASE IF EXISTS "{BASE_DEMO}" WITH (FORCE)')
        print(f"Base '{BASE_DEMO}' borrada.")

    print(f"\nListo. Las capturas estan en {DESTINO.relative_to(SITIO)}")


if __name__ == "__main__":
    main()
