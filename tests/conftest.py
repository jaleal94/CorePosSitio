"""Estado compartido que debe quedar limpio entre pruebas.

`django-ratelimit` cuenta los envios en la cache, y la cache no se reinicia
entre pruebas: sin esto, la primera que envia diez formularios deja bloqueadas
a todas las siguientes, y el fallo aparece en una prueba que no tiene nada que
ver con los limites.
"""

import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def limpiar_la_cache():
    cache.clear()
    yield
    cache.clear()
