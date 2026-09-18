"""Configuracion comun a los tres entornos.

Lo mismo que Core Pos, por el principio VI: quien mantiene el producto mantiene
el sitio, y dos mundos distintos terminan con uno de los dos abandonado.
"""

import warnings
from pathlib import Path

import environ
from csp.constants import NONCE, SELF, UNSAFE_EVAL, UNSAFE_INLINE

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
    # Traduce el limite de tasa a un 429 antes de que parezca falta de permisos.
    "sitio.middleware.LimiteDeTasaMiddleware",
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


def _solo_lo_que_postgres_entiende(opciones):
    """Descarta los parametros de la cadena que no son de Postgres.

    Los proveedores reparten cadenas con parametros de otras herramientas
    metidos dentro. Supabase da la suya con `?pgbouncer=true`, que es de
    Prisma; otras traen `schema` o `connection_limit`. Django los pasa tal cual
    a psycopg, y psycopg no arranca:

        ProgrammingError: invalid connection option "pgbouncer"

    Eso no se arregla explicandolo una vez, porque la misma cadena se pega
    despues en el panel del hosting y en los secretos del repositorio, y ahi
    falla en produccion. Se limpia aqui, una sola vez, para todos los entornos.

    Lo valido se le pregunta a la propia libreria en vez de escribirlo a mano:
    una lista escrita a mano envejece, y el dia que Postgres admita un
    parametro nuevo lo estariamos tirando.
    """
    from psycopg import pq

    validas = {opcion.keyword.decode() for opcion in pq.Conninfo.get_defaults()}
    sobran = sorted(set(opciones) - validas)
    if sobran:
        warnings.warn(
            "DATABASE_URL trae parametros que Postgres no entiende y se ignoran: "
            f"{', '.join(sobran)}. Son de otras herramientas.",
            stacklevel=2,
        )
    return {clave: valor for clave, valor in opciones.items() if clave in validas}


if DATABASES["default"].get("OPTIONS"):
    DATABASES["default"]["OPTIONS"] = _solo_lo_que_postgres_entiende(
        DATABASES["default"]["OPTIONS"]
    )

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
# La marca de un solo uso permite exactamente el bloque de datos estructurados
# de la portada. Relajar la politica con 'unsafe-inline' habria abierto justo la
# puerta que la politica cierra, y por un bloque que no ejecuta nada.
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        # `NONCE` permite exactamente el bloque de datos estructurados de la
        # portada, que lo lleva. `UNSAFE_EVAL` es por Alpine, que evalua las
        # expresiones de sus atributos construyendo funciones.
        "script-src": [SELF, UNSAFE_EVAL, NONCE],
        "style-src": [SELF, UNSAFE_INLINE],
        "img-src": [SELF, "data:"],
        "font-src": [SELF],
        "connect-src": [SELF],
        "form-action": [SELF],
        "frame-ancestors": ["'none'"],
        "base-uri": [SELF],
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
