"""Que lo que se sube a Vercel sea lo que el sitio necesita.

Vercel no entiende `uv` ni `pyproject.toml`: instala lo que diga
`requirements.txt`. Son dos listas de dependencias para el mismo proyecto, y
dos listas se separan solas.

Cuando se separan, no falla nada aqui: falla el despliegue, o peor, arranca y
revienta la primera vez que alguien entra. Esta prueba las mantiene juntas.

El resto comprueba la configuracion del despliegue, que es codigo aunque no lo
parezca: un orden de rutas al reves deja el sitio sin estilos, y una migracion
dentro de la construccion puede dejar la base a medias.
"""

import json
import re
import tomllib
from pathlib import Path

from django.conf import settings

RAIZ = Path(settings.RAIZ)


def declaradas_en_pyproject():
    """Los nombres de las dependencias de ejecucion, normalizados."""
    datos = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    nombres = set()
    for linea in datos["project"]["dependencies"]:
        # "psycopg[binary]>=3.2" -> "psycopg"
        nombres.add(re.split(r"[\[><=!~;]", linea)[0].strip().lower().replace("_", "-"))
    return nombres


def instaladas_por_vercel():
    texto = (RAIZ / "requirements.txt").read_text(encoding="utf-8")
    nombres = set()
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        nombres.add(re.split(r"[\[><=!~;]", linea)[0].strip().lower().replace("_", "-"))
    return nombres


# ------------------------------------------------------------- dependencias


def test_requirements_trae_todo_lo_que_el_sitio_declara():
    """Si se agrega una dependencia y se olvida regenerar, esto lo dice.

    Se regenera con:
        uv export --no-dev --no-hashes --no-annotate --no-header \\
            --format requirements-txt > requirements.txt
    """
    faltan = declaradas_en_pyproject() - instaladas_por_vercel()
    assert not faltan, (
        f"requirements.txt no trae {sorted(faltan)}. Vercel instala de ahi, "
        "no de pyproject.toml: regenerelo."
    )


def test_lo_que_solo_usan_las_herramientas_no_viaja_al_servidor():
    """Pillow solo lo usan los guiones de `herramientas/`, que se corren a mano."""
    assert "pillow" not in instaladas_por_vercel()


# ------------------------------------------------------------- configuracion


def vercel_json():
    return json.loads((RAIZ / "vercel.json").read_text(encoding="utf-8"))


def test_los_estaticos_se_resuelven_antes_que_el_resto():
    """Vercel toma la primera ruta que coincide.

    Si el comodin quedara primero, cada archivo de estilos entraria a Django,
    que en produccion no los sirve. El sitio se veria sin una sola linea de CSS
    y el despliegue diria que todo salio bien.
    """
    rutas = [ruta["src"] for ruta in vercel_json()["routes"]]
    assert rutas.index("/static/(.*)") < rutas.index("/(.*)")


def test_el_punto_de_entrada_expone_lo_que_vercel_busca():
    texto = (RAIZ / "api" / "index.py").read_text(encoding="utf-8")
    assert re.search(r"^app = ", texto, re.M), "Vercel busca una variable llamada `app`"
    assert "config.settings.vercel" in texto


def test_la_construccion_no_corre_migraciones():
    """Se dispara en cada despliegue y puede haber dos a la vez.

    Una migracion a medias por una construccion cancelada deja la base en un
    estado que nadie pidio. Las migraciones se corren a mano, una vez.
    """
    guion = (RAIZ / "build_files.sh").read_text(encoding="utf-8")
    assert "collectstatic" in guion
    assert "manage.py migrate" not in guion


def test_los_cursores_de_servidor_estan_apagados():
    """Los agrupadores de conexiones funcionan en modo transaccion.

    Ahi un cursor de servidor se declara en una transaccion y la siguiente
    lectura puede caer en otra conexion, donde ese cursor no existe.

    No es teorico: la exportacion de contactos usa `.iterator()`, que abre uno.
    Sin esto, esa pantalla falla en produccion y en ningun otro sitio.

    Se lee el archivo en vez de importarlo: importarlo arrastra `prod.py`, que
    se niega a cargarse sin las variables de produccion puestas -y hace bien-.
    """
    ajustes = (RAIZ / "config" / "settings" / "vercel.py").read_text(encoding="utf-8")
    assert 'DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True' in ajustes

    vistas = (RAIZ / "sitio" / "views.py").read_text(encoding="utf-8")
    assert ".iterator()" in vistas, (
        "Si ya nadie usa .iterator(), esta prueba y su ajuste pueden revisarse"
    )


def test_el_env_nunca_sube():
    assert ".env" in (RAIZ / ".vercelignore").read_text(encoding="utf-8")


def test_la_carpeta_de_estaticos_generados_no_se_versiona():
    """La genera la construccion; versionarla es garantizar que quede vieja."""
    destino = settings.STATIC_ROOT if hasattr(settings, "STATIC_ROOT") else None
    assert destino is not None
    ignorados = (RAIZ / ".gitignore").read_text(encoding="utf-8")
    assert "estaticos_de_vercel" in ignorados
