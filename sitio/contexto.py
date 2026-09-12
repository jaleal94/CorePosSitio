"""La marca, a mano en toda plantilla.

El nombre, el telefono y la direccion del sistema viven en la configuracion y
llegan aqui. Cambiar la marca es cambiar una linea, no buscar por veinte
plantillas (decision D3).
"""

from urllib.parse import quote

from django.conf import settings

from .contenido import SECCIONES_DEL_MENU


def marca(request):
    datos = dict(settings.MARCA)
    # El enlace de WhatsApp ya armado, para no repetir la plantilla del enlace
    # en cada boton del sitio.
    saludo = f"Hola, vi {datos['nombre']} y quiero saber mas para mi negocio."
    datos["whatsapp_url"] = f"https://wa.me/{datos['whatsapp']}?text={quote(saludo)}"
    return {"marca": datos, "secciones_del_menu": SECCIONES_DEL_MENU}
