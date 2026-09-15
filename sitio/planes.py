"""El plan, declarado una sola vez.

Hay uno: 19,99 $ al mes, mas 60 $ una sola vez por la instalacion.

Ni un numero escrito a mano en una plantilla. Hay dos pruebas que lo sostienen
—una que compara estos numeros con los que Core Pos declara de verdad, y otra
que comprueba que la plantilla no los escriba por su cuenta— porque un precio
que dice una cosa en el sitio y otra en el sistema es la peor forma de empezar
una relacion con un cliente.

**Los dos numeros se comparan, no solo la mensualidad.** El de instalacion es el
mas caro de equivocar: son 60 $ que alguien lee una vez y recuerda. Si viviera
solo aqui, seria el unico numero de la pagina que nadie verifica contra el
sistema.

**El plan no tiene limites**, y por eso no se anuncia ninguno. La tentacion
seria poner "hasta 2.000 productos" para que la ficha se vea llena; seria
mentira, y aqui no se dice nada que no sea cierto.

La forma es la misma que en el producto a proposito: hace la comparacion obvia.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Plan:
    clave: str
    nombre: str
    precio_mensual: Decimal
    precio_instalacion: Decimal
    descripcion: str

    @property
    def precio_visible(self):
        """Con sus centimos: 19,99 redondeado a entero dice 20, que es otro precio."""
        return f"${self.precio_mensual:.2f}"

    @property
    def instalacion_visible(self):
        return f"${self.precio_instalacion:.2f}"


EL_PLAN = Plan(
    clave="unico",
    nombre="Core Pos",
    precio_mensual=Decimal("19.99"),
    precio_instalacion=Decimal("60"),
    descripcion="El sistema completo, sin limites de catalogo ni de personal.",
)

# Se deja el plural para que la plantilla siga recorriendo una lista: el dia que
# haya un segundo plan no habra que tocar el HTML, solo esto.
PLANES = (EL_PLAN,)

# Lo que trae. Antes se listaba aparte para que el plan de entrada no pareciera
# una version recortada; ahora no hay de que recortarse, pero la lista se queda:
# es lo que de verdad convence, y es mas larga que cualquier ficha de precio.
LO_QUE_TRAE = (
    "Punto de venta con codigo de barras",
    "Control de inventario y costos",
    "Cierre de caja diario",
    "Fiado y cobranza",
    "Compras a proveedores",
    "Reportes de ventas y ganancia",
    "Precio en divisa y cobro en bolivares",
    "Sin limite de productos, de personal ni de ventas",
    "Sus datos, exportables cuando quiera",
)
