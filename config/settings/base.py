"""Configuracion comun a los tres entornos.

Lo mismo que Core Pos, por el principio VI: quien mantiene el producto mantiene
el sitio, y dos mundos distintos terminan con uno de los dos abandonado.
"""

from pathlib import Path

import environ

RAIZ = Path(__file__).resolve().parents[2]

env = environ.Env(DJANGO_DEBUG=(bool, False))
environ.Env.read_env(RAIZ / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-inseguro-cambiar-en-produccion")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_cotton",
    "django_htmx",
    "sitio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [RAIZ / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sitio.contexto.marca",
            ],
            "builtins": ["django_cotton.templatetags.cotton"],
        },
    },
]

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ve"
TIME_ZONE = env("DJANGO_TIME_ZONE", default="America/Caracas")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [RAIZ / "static"]
STATIC_ROOT = RAIZ / "static_recolectado"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/admin/login/"

# ------------------------------------------------------------------- la marca
# El nombre, los contactos y la direccion del sistema viven aqui y en ningun
# otro sitio: cambiar la marca o el telefono es cambiar una linea (decision D3).
MARCA = {
    "nombre": "Core Pos",
    "descripcion": "Punto de venta e inventario para bodegas y abastos",
    "whatsapp": env("CORE_POS_WHATSAPP", default="584140000000"),
    "correo": env("CORE_POS_CORREO", default="hola@corepos.test"),
    "app_url": env("CORE_POS_APP_URL", default="http://127.0.0.1:8000"),
}

# ---------------------------------------------------- politica de contenido
# Nada viene de fuera (principio IV y X): ni tipografias, ni bibliotecas, ni
# rastreadores. Eso permite una politica casi entera "solo de aqui".
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-eval'"],  # Alpine evalua sus atributos
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "font-src": ["'self'"],
        "connect-src": ["'self'"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
        "base-uri": ["'self'"],
        "object-src": ["'none'"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "{levelname} {asctime} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": env("DJANGO_LOG_LEVEL", default="INFO")},
}
