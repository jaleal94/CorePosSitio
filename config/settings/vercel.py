"""Produccion sobre Vercel.

Hereda de `prod.py` -que es donde vive la seguridad: HTTPS forzado, HSTS,
cookies- y cambia solo lo que Vercel obliga a cambiar.

Son dos cosas, y las dos vienen de lo mismo: **en Vercel no hay un proceso que
se quede encendido**. Cada peticion puede caer en una funcion recien arrancada,
sin memoria de la anterior y sin el disco de la anterior.
"""

from .prod import *
from .prod import RAIZ

# --------------------------------------------------------------- estaticos
#
# Los archivos estaticos no los sirve Django aqui: los sirve la red de Vercel,
# desde lo que `build_files.sh` deja durante la construccion. `vercel.json`
# manda todo lo que empieza por /static/ a esa copia y nunca llega a Python.
#
# Por eso el almacenamiento no puede ser el que agrega un hash al nombre: ese
# escribe un `staticfiles.json` durante la construccion de los estaticos, y la
# funcion de Python es otra construccion distinta que no lo tendria. Sin ese
# archivo, cada `{% static %}` de cada plantilla revienta.
#
# Se pierde el hash en el nombre, que es lo que permite cachear para siempre.
# A cambio, `vercel.json` pone una cache corta y con revalidacion. Para un sitio
# de presentacion de 33 KB es un cambio que no se nota.
STATIC_ROOT = RAIZ / "estaticos_de_vercel" / "static"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# --------------------------------------------------------------- conexiones
#
# Cada funcion abre su propia conexion a Postgres y muere con ella. Mantenerlas
# vivas aqui solo consigue agotar el limite de conexiones de la base con
# conexiones que nadie va a reutilizar.
DATABASES["default"]["CONN_MAX_AGE"] = 0

# En serverless hay que conectarse por el endpoint agrupado -el que lleva
# `-pooler` en el nombre-, o cuarenta funciones a la vez agotan las conexiones
# de la base. Ese agrupador es PgBouncer en modo transaccion, y ahi **los
# cursores de servidor no funcionan**: el cursor se declara en una transaccion y
# la siguiente lectura puede caer en otra conexion distinta, donde ese cursor no
# existe.
#
# Esto no es teorico aqui: `sitio/views.py` exporta los contactos con
# `.iterator()`, que es justamente lo que abre uno. Sin esta linea, la
# exportacion falla en produccion y en ningun otro sitio.
#
# Django trae el interruptor documentado para este caso. Lo que cuesta es que
# `.iterator()` deja de ahorrar memoria y trae todo de una vez; con una lista de
# contactos de un sitio de presentacion, da igual.
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
