"""El contenido de la pagina: las listas largas, en un solo sitio.

Vive en Python y no en la plantilla porque son listas que se recorren, y porque
asi una prueba puede recorrerlas tambien —comprobar que ninguna frase usa
palabras de programador, por ejemplo— sin tener que leer HTML.

**Cada afirmacion de aqui describe algo que Core Pos hace hoy.** Si algo se
construye despues, se agrega despues (principio I).
"""

from dataclasses import dataclass

# ------------------------------------------------------------------- el heroe

HEROE = {
    "titulo": "Sepa lo que tiene, lo que vende y lo que gana",
    "entrada": (
        "El punto de venta para bodegas y abastos. Cobre rapido, controle su "
        "mercancia y cuadre la caja todos los dias."
    ),
    "apoyo": "Funciona en el telefono del mostrador. Empiece gratis, sin tarjeta.",
}


# --------------------------------------------------------------- el problema


@dataclass(frozen=True)
class Problema:
    queja: str
    respuesta: str


PROBLEMAS = (
    Problema(
        queja="Vendo todo el dia y no se si estoy ganando",
        respuesta=(
            "Cada venta guarda a que costo salio la mercancia, asi que la "
            "ganancia se calcula sola. Vea al cierre del dia cuanto vendio y "
            "cuanto le quedo, producto por producto."
        ),
    ),
    Problema(
        queja="Se me pierde mercancia y no se cuanta",
        respuesta=(
            "Todo lo que entra y todo lo que sale queda anotado, con quien lo "
            "hizo y por que. Cuando cuente el estante, el sistema le dice "
            "exactamente cuanto falta y cuanto vale lo que falta."
        ),
    ),
    Problema(
        queja="No se a quien le fie ni cuanto me deben",
        respuesta=(
            "Cada fiado queda con nombre, monto y fecha. Vea quien le debe, "
            "desde cuando, y ponga un limite a cada quien para que la cuenta no "
            "se le crezca sin darse cuenta."
        ),
    ),
    Problema(
        queja="El proveedor me sube y yo sigo vendiendo al mismo precio",
        respuesta=(
            "Al recibir la compra, el costo se actualiza solo, con el flete "
            "repartido. Si su precio de venta quedo corto, lo ve en el reporte "
            "de ganancia antes de que le coma el mes."
        ),
    ),
    Problema(
        queja="Cobro en bolivares pero pienso en dolares",
        respuesta=(
            "Ponga sus precios en divisa y cobre a la tasa del dia. La tasa "
            "queda congelada en cada venta, asi que una venta de la semana "
            "pasada no cambia de valor porque hoy cambio el cambio."
        ),
    ),
)


# ------------------------------------------------------------------- los pasos


@dataclass(frozen=True)
class Paso:
    numero: int
    titulo: str
    detalle: str


PASOS = (
    Paso(
        numero=1,
        titulo="Cargue lo que vende",
        detalle=(
            "Suba su lista desde una hoja de calculo, o escriba sus primeros "
            "veinte productos y siga agregando sobre la marcha. No hace falta "
            "tener el catalogo completo para empezar a cobrar."
        ),
    ),
    Paso(
        numero=2,
        titulo="Cobre",
        detalle=(
            "Escanee el codigo o busque por nombre, elija como le pagan "
            "—efectivo, pago movil, transferencia, fiado— y cobre. Abre la caja "
            "en la mañana y la cuadra en la noche."
        ),
    ),
    Paso(
        numero=3,
        titulo="Mire sus numeros",
        detalle=(
            "Cuanto vendio hoy, que producto le deja mas, que hay que reponer y "
            "que lleva meses en el estante sin moverse."
        ),
    ),
)


# ---------------------------------------------------------------- lo que hace


@dataclass(frozen=True)
class Grupo:
    titulo: str
    resuelve: str
    funciones: tuple[str, ...]


LO_QUE_HACE = (
    Grupo(
        titulo="Cobrar",
        resuelve="Para que la cola avance y ninguna venta se pierda",
        funciones=(
            "Cobro con lector de codigo de barras o buscando por nombre",
            "Efectivo, pago movil, transferencia, tarjeta y fiado, combinables",
            "Vuelto calculado en la moneda que usted elija",
            "Descuentos con limite por cajero",
            "Anulacion de una venta, que devuelve la mercancia al inventario",
            "Comprobante para imprimir en rollo de 58 u 80 mm",
        ),
    ),
    Grupo(
        titulo="Saber lo que tiene",
        resuelve="Para pedir a tiempo y no comprar lo que ya tiene",
        funciones=(
            "Existencia al dia de cada producto",
            "Costo promedio calculado solo, con el flete repartido",
            "Aviso de lo que hay que reponer y de lo que se agoto",
            "Aviso de lo que lleva meses sin venderse y cuanto dinero es",
            "Merma y consumo interno, con su motivo",
            "Historial completo de cada producto: de donde salio cada unidad",
        ),
    ),
    Grupo(
        titulo="Cuadrar la caja",
        resuelve="Para saber cada noche si el dinero esta completo",
        funciones=(
            "Apertura con fondo inicial, por persona y por turno",
            "Cierre con el conteo de lo que hay y la diferencia calculada",
            "Ingresos, retiros y gastos del dia",
            "Impuesto sobre el pago en divisa, configurable",
        ),
    ),
    Grupo(
        titulo="Comprar y contar",
        resuelve="Para que lo que dice el sistema sea lo que hay en el estante",
        funciones=(
            "Compras a proveedor, con recepcion parcial de lo que llego",
            "Flete repartido entre los productos, dentro del costo",
            "Devolucion al proveedor",
            "Conteo fisico desde el telefono, sin ver lo que el sistema espera",
            "Diferencias valorizadas y ajuste con justificacion",
        ),
    ),
    Grupo(
        titulo="Fiar y cobrar",
        resuelve="Para que el cuaderno de fiados no se moje ni se pierda",
        funciones=(
            "Ficha de cliente con su limite de credito",
            "Fiado desde el mismo cobro, combinado con efectivo",
            "Abonos con recibo, que entran a la caja del dia",
            "Estado de cuenta y reporte de quien debe desde cuando",
        ),
    ),
    Grupo(
        titulo="Vigilar",
        resuelve="Para saber quien hizo que, el dia que algo no cuadre",
        funciones=(
            "Roles: quien cobra, quien ajusta inventario, quien ve los costos",
            "Registro de cada anulacion, ajuste y cambio de precio",
            "De una venta se llega a cada movimiento que produjo, y de vuelta",
            "Sus datos exportables completos, cuando quiera",
        ),
    ),
)


# El limite del producto, dicho antes de que alguien pierda su tiempo. Esto
# ahorra llamadas y evita la peor conversacion posible: la que descubre a mitad
# de camino que el sistema no servia para su caso.
LO_QUE_NO_HACE = (
    "No emite factura fiscal homologada ni trabaja con impresora fiscal.",
    "No maneja comandas de restaurante, mesas ni cocina.",
    "No funciona sin internet: hace falta conexion para cobrar.",
    "No lleva nomina ni contabilidad formal.",
    "No hace reportes que junten varias sucursales en uno solo.",
)


# ------------------------------------------------------------------ preguntas


@dataclass(frozen=True)
class Pregunta:
    pregunta: str
    respuesta: str


PREGUNTAS = (
    Pregunta(
        pregunta="¿Que pasa si se va la luz o se cae internet?",
        respuesta=(
            "No va a poder cobrar mientras no haya conexion, y preferimos "
            "decirlo antes que prometer lo contrario. Lo que si garantizamos es "
            "que ninguna venta se pierde ni se cobra dos veces cuando la "
            "conexion falla a mitad: si el envio se repite, se guarda una sola."
        ),
    ),
    Pregunta(
        pregunta="¿Tengo que cargar todo mi catalogo para empezar?",
        respuesta=(
            "No. Empiece con lo que mas vende, veinte o treinta productos, y "
            "vaya agregando mientras cobra. Si ya tiene una lista en una hoja "
            "de calculo, se sube de una vez y el sistema le dice fila por fila "
            "que entro y que no."
        ),
    ),
    Pregunta(
        pregunta="¿Sirve en el telefono o necesito una computadora?",
        respuesta=(
            "Sirve en el telefono, y esta hecho pensando en eso: se cobra con "
            "una mano, de pie en el mostrador. Para cargar el catalogo desde un "
            "archivo o revisar reportes largos, una computadora es mas comoda."
        ),
    ),
    Pregunta(
        pregunta="¿Quien puede ver mis datos?",
        respuesta=(
            "Solo usted y las personas a las que usted le de acceso, con el rol "
            "que usted decida. Los datos de su negocio no se mezclan con los de "
            "ningun otro comercio, y quien administra la plataforma no ve sus "
            "productos, sus ventas ni sus clientes."
        ),
    ),
    Pregunta(
        pregunta="¿Y si despues me quiero ir?",
        respuesta=(
            "Se lleva todo. Descarga un archivo con su catalogo, su inventario, "
            "sus ventas, sus clientes y sus compras, en un formato que abre "
            "Excel. No hay que pedirle permiso a nadie ni esperar."
        ),
    ),
    Pregunta(
        pregunta="¿Cuanto cuesta y hay que pagar por adelantado?",
        respuesta=(
            "El plan de entrada es gratis y no pide tarjeta. Los otros dos se "
            "pagan por mes y se puede cambiar de plan cuando quiera. Si se pasa "
            "de los limites de su plan, el sistema le avisa, pero nunca lo deja "
            "sin poder vender."
        ),
    ),
    Pregunta(
        pregunta="¿Me sirve si tengo dos locales?",
        respuesta=(
            "Si, pero cada local lleva su propio inventario y su propia caja, "
            "como negocios separados. Todavia no hay un reporte que sume los "
            "dos en uno solo."
        ),
    ),
)


# Las capturas que van a entrar en F3. Se declaran ahora, con su pie escrito,
# para que la seccion tenga su forma definitiva desde ya y las imagenes solo
# ocupen un hueco que ya existe.
@dataclass(frozen=True)
class Captura:
    archivo: str
    pie: str
    alto: str  # proporcion reservada, para que el diseño no salte al cargar

    @property
    def ruta(self):
        return f"img/{self.archivo}"


CAPTURAS = (
    Captura(
        "cobro.webp",
        "El cobro, en el telefono del mostrador",
        "aspect-[420/860]",
    ),
    Captura(
        "panel.webp",
        "El panel del dia: cuanto vendio y cuanto le quedo",
        "aspect-[1100/800]",
    ),
    Captura(
        "inventario.webp",
        "Lo que hay en el estante, y lo que hay que reponer",
        "aspect-[1100/800]",
    ),
)


# Las secciones del menu, en el orden en que aparecen.
SECCIONES_DEL_MENU = (
    ("problema", "El problema"),
    ("como-funciona", "Como funciona"),
    ("lo-que-hace", "Lo que hace"),
    ("precios", "Precios"),
    ("preguntas", "Preguntas"),
)
