"""Entorno de produccion. Todo secreto llega por variable de entorno."""

from .base import *
from .base import env

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
SECRET_KEY = env("DJANGO_SECRET_KEY")

if SECRET_KEY.startswith("dev-inseguro"):
    raise RuntimeError("DJANGO_SECRET_KEY no fue configurada para produccion")

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
X_FRAME_OPTIONS = "DENY"

# --------------------------------------------------------------- la cache
#
# `sitio/views.py` limita el formulario de contacto a 10 envios por hora y por
# direccion, y `django-ratelimit` lleva esa cuenta en la cache de Django.
#
# Sin declarar nada, esa cache es la de memoria del proceso. En desarrollo hay
# un proceso y funciona; en produccion hay varios -o, en Vercel, uno nuevo casi
# por peticion- y cada uno lleva su propia cuenta. El limite deja de limitar
# justo donde hace falta, y no avisa: sigue pareciendo que esta puesto.
#
# La tabla de la base se comparte entre todos. Es mas lenta que Redis y da
# igual: son diez escrituras por hora y por visitante, no un sitio de alta
# concurrencia. La crea la migracion `sitio/0002_tabla_de_cache`.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_del_sitio",
    }
}
