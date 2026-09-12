"""Traduce el limite de tasa a un 429 que explica.

`django-ratelimit` levanta una excepcion que hereda de `PermissionDenied`, asi
que sin esto quien envia el formulario demasiadas veces ve "no tiene permiso".
Eso es falso —permiso tiene— y un mensaje de error que miente es peor que no
tener ninguno.
"""

from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited


class LimiteDeTasaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, excepcion):
        if not isinstance(excepcion, Ratelimited):
            return None
        return render(request, "sitio/espere.html", status=429)
