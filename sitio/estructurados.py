"""Lo que el sitio le dice a un buscador sobre si mismo.

Sale de las mismas declaraciones que la pagina: los planes de `planes.py` y las
preguntas de `contenido.py`. Si se escribiera aparte, el dia que cambie un
precio el buscador seguiria anunciando el viejo.
"""

import json

from django.conf import settings

from .contenido import HEROE, PREGUNTAS
from .planes import PLANES


def datos_del_sitio(request):
    marca = settings.MARCA
    base = f"{request.scheme}://{request.get_host()}"

    producto = {
        "@type": "SoftwareApplication",
        "name": marca["nombre"],
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "description": HEROE["entrada"],
        "url": base,
        "inLanguage": "es-VE",
        "offers": [
            {
                "@type": "Offer",
                "name": plan.nombre,
                "price": str(plan.precio_mensual),
                "priceCurrency": "USD",
                "description": plan.descripcion,
            }
            for plan in PLANES
        ],
    }

    preguntas = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": pregunta.pregunta,
                "acceptedAnswer": {"@type": "Answer", "text": pregunta.respuesta},
            }
            for pregunta in PREGUNTAS
        ],
    }

    return json.dumps(
        {"@context": "https://schema.org", "@graph": [producto, preguntas]},
        ensure_ascii=False,
    )
