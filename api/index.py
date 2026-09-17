"""Punto de entrada para Vercel.

Vercel busca en cada archivo de `api/` una variable llamada `app` y la trata
como una aplicacion WSGI. Esto es todo lo que hace falta: Django ya trae la
suya.

El archivo vive en `api/` y no en la raiz porque es la convencion de Vercel, y
por eso hay que poner la raiz del proyecto en la ruta de importacion: sin esto,
`config.settings` no se encuentra.
"""

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.vercel")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
