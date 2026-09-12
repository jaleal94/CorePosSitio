"""Los tres planes, declarados una sola vez.

Ni un numero de plan escrito a mano en una plantilla: la pagina recorre esto.
Hay dos pruebas que lo sostienen —una que compara estos numeros con los que
Core Pos cobra de verdad, y otra que comprueba que la plantilla no los escriba
por su cuenta— porque un precio que dice una cosa en el sitio y otra en el
sistema es la peor forma de empezar una relacion con un cliente.

La forma es la misma que en el producto a proposito: hace la comparacion obvia
y el dia que se genere automaticamente no habra que traducir nada.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Plan:
    clave: str
    nombre: str
    precio_mensual: Decimal
    productos: int
    personal: int
    ventas_por_mes: int
    descripcion: str
    # Para quien es, dicho como lo diria ella. No sale del producto: es venta.
    para_quien: str
    destacado: bool = False

    @property
    def es_gratuito(self):
        return self.precio_mensual == 0

    @property
    def precio_visible(self):
        return "Gratis" if self.es_gratuito else f"${self.precio_mensual:.0f}"

    @property
    def limites(self):
        """Los tres limites, listos para la plantilla."""
        return [
            f"Hasta {self.productos:,} productos".replace(",", "."),
            f"{self.personal} {'persona' if self.personal == 1 else 'personas'} con acceso",
            f"{self.ventas_por_mes:,} ventas al mes".replace(",", "."),
        ]


PLANES = (
    Plan(
        clave="basico",
        nombre="Basico",
        precio_mensual=Decimal("0"),
        productos=300,
        personal=2,
        ventas_por_mes=1500,
        descripcion="Para empezar: una bodega chica con una o dos personas.",
        para_quien="Si esta empezando o quiere probarlo sin arriesgar nada.",
    ),
    Plan(
        clave="comercio",
        nombre="Comercio",
        precio_mensual=Decimal("12"),
        productos=2000,
        personal=6,
        ventas_por_mes=10000,
        descripcion="Para un abasto con varias cajas y un encargado de inventario.",
        para_quien="Si tiene dos cajas, alguien encargado del inventario, y fia.",
        destacado=True,
    ),
    Plan(
        clave="cadena",
        nombre="Cadena",
        precio_mensual=Decimal("35"),
        productos=20000,
        personal=25,
        ventas_por_mes=60000,
        descripcion="Para un comercio grande, con catalogo amplio y mucho personal.",
        para_quien="Si maneja un catalogo grande y varios turnos de personal.",
    ),
)

# Lo que trae cualquier plan. Se lista aparte para que no parezca que el plan de
# entrada es una version recortada: es el mismo sistema, con otros limites.
INCLUIDO_EN_TODOS = (
    "Punto de venta con codigo de barras",
    "Control de inventario y costos",
    "Cierre de caja diario",
    "Fiado y cobranza",
    "Compras a proveedores",
    "Reportes de ventas y ganancia",
    "Precio en divisa y cobro en bolivares",
    "Sus datos, exportables cuando quiera",
)
