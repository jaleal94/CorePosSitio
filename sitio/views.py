"""Las vistas del sitio. Por ahora, una sola pagina."""

from django.shortcuts import render

from . import contenido
from .planes import INCLUIDO_EN_TODOS, PLANES


def portada(request):
    return render(
        request,
        "sitio/portada.html",
        {
            "heroe": contenido.HEROE,
            "problemas": contenido.PROBLEMAS,
            "pasos": contenido.PASOS,
            "grupos": contenido.LO_QUE_HACE,
            "no_hace": contenido.LO_QUE_NO_HACE,
            "capturas": contenido.CAPTURAS,
            "planes": PLANES,
            "incluido": INCLUIDO_EN_TODOS,
            "preguntas": contenido.PREGUNTAS,
        },
    )
