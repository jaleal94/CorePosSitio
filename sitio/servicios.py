"""Guardar el contacto, y armar la respuesta.

La regla de la fase, y del principio III: **el contacto se guarda antes que
nada, y nada de lo que venga despues puede tumbarlo**. Por eso guardar tiene su
propia transaccion y lo demas ocurre fuera de ella.
"""

from urllib.parse import quote

from django.conf import settings
from django.db import IntegrityError, transaction

from .models import Contacto, solo_digitos

# Lo que se promete en la pagina de gracias. Vive aqui y no escrito en el texto
# porque es una promesa que hay que poder cumplir, y porque cambiarla en un solo
# sitio evita que la pagina diga una cosa y el correo de respuesta otra.
PLAZO_DE_RESPUESTA = "el mismo dia"


@transaction.atomic
def registrar_contacto(*, datos, origen="", ip=None):
    """Guarda el contacto y lo devuelve, junto con si es nuevo.

    Si ese telefono ya escribio, se actualiza lo que conto y la fecha, y se
    conserva el trabajo del operador: su estado y sus notas son suyos.

    No se comprueba antes de insertar: entre la comprobacion y la insercion hay
    una ventana, y es justo donde cae el segundo envio de alguien impaciente.
    """
    telefono = solo_digitos(datos["telefono"])

    try:
        # El bloque propio es imprescindible: sin el, la restriccion violada
        # deja la transaccion abortada y la consulta de abajo falla tambien.
        # Con el, solo se deshace este punto de guardado.
        with transaction.atomic():
            contacto = Contacto.objects.create(
                nombre=datos["nombre"].strip(),
                comercio=datos["comercio"].strip(),
                telefono=telefono,
                correo=(datos.get("correo") or "").strip().lower(),
                mensaje=(datos.get("mensaje") or "").strip(),
                origen=origen,
                origen_ip=ip,
            )
        return contacto, True
    except IntegrityError:
        pass  # Ya escribio antes. Se actualiza lo suyo, nunca lo nuestro.

    contacto = Contacto.objects.get(telefono=telefono)
    contacto.nombre = datos["nombre"].strip()
    contacto.comercio = datos["comercio"].strip()
    if datos.get("correo"):
        contacto.correo = datos["correo"].strip().lower()
    if datos.get("mensaje"):
        # Se suma, no se pisa: lo segundo que escribio suele ser lo importante.
        contacto.mensaje = f"{contacto.mensaje}\n\n{datos['mensaje'].strip()}".strip()
    contacto.save()
    return contacto, False


def enlace_de_whatsapp(contacto):
    """El enlace para responderle, con el mensaje ya escrito.

    Que lo llame por su nombre y mencione su comercio no es adorno: es la
    diferencia entre un mensaje que parece automatico y uno que parece de una
    persona que leyo lo que escribio.
    """
    marca = settings.MARCA["nombre"]
    texto = (
        f"Hola {contacto.nombre.split(' ')[0]}, le escribo de {marca}. "
        f"Vi que dejo sus datos para {contacto.comercio}. "
        "¿Le queda bien que le muestre como quedaria su negocio?"
    )
    return f"https://wa.me/{contacto.telefono}?text={quote(texto)}"


def sin_atender():
    from .models import EstadoContacto

    return Contacto.objects.filter(estado=EstadoContacto.NUEVO)
