"""Entorno de pruebas. Misma base de datos que desarrollo y produccion."""

from .base import *

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
