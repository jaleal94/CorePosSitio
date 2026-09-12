"""El mapa del sitio: solo lo publico.

El panel de contactos y la pagina de gracias no entran, y ademas llevan su
propia etiqueta de no indexar. Dos candados para lo mismo, porque el mapa lo
lee un buscador educado y la etiqueta la respeta cualquiera.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PaginasPublicas(Sitemap):
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return [
            ("sitio:portada", 1.0),
            ("sitio:privacidad", 0.3),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]


MAPAS = {"paginas": PaginasPublicas}
