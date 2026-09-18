"""Entorno de pruebas. Mismo motor que desarrollo y produccion.

La suite crea y borra una base propia -`test_<nombre>`- y la llena de datos
inventados. Contra un servidor local eso es lo que se quiere; contra el de
produccion seria crear una base dentro del servidor que atiende a los clientes.

No es un temor abstracto: paso. Al preparar el despliegue, el `.env` quedo
apuntando a Neon y `pytest` intento arrancar contra el. Lo unico que lo impidio
fue que el proveedor de internet bloquea ese puerto, y eso no es una proteccion:
es suerte.
"""

from .base import *

SERVIDOR = (DATABASES["default"].get("HOST") or "").lower()
PERMITIDOS = {"", "localhost", "127.0.0.1", "::1", "postgres", "db"}

if SERVIDOR not in PERMITIDOS and not env.bool("PRUEBAS_CONTRA_REMOTO", default=False):
    raise RuntimeError(
        f"Las pruebas apuntan a '{SERVIDOR}', que no es un servidor local.\n"
        "La suite crea y borra bases enteras: contra un servidor remoto eso no "
        "se hace sin querer.\n"
        "Revise DATABASE_URL en su .env. La cadena de produccion vive en los "
        "secretos de GitHub y en Vercel, no en la maquina de nadie."
    )

DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# Cifrado rapido: la suite no prueba la fortaleza del algoritmo.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# WhiteNoise sirve los estaticos recolectados, que en pruebas no existen y no
# hacen falta: quitarlo evita un aviso en cada peticion de la suite.
MIDDLEWARE = [m for m in MIDDLEWARE if "whitenoise" not in m]

LOGGING["loggers"] = {"django.request": {"handlers": [], "level": "CRITICAL"}}
