"""Que el sitio no cobre una cosa y el sistema otra.

Un precio que dice algo distinto en cada sitio es la peor forma de empezar una
relacion con un cliente, y es un error facilisimo de cometer: se cambia el plan
en el producto y nadie se acuerda del sitio.
"""

import ast
import os
import re
from decimal import Decimal
from pathlib import Path

import pytest
from django.urls import reverse

from sitio.planes import PLANES

# Donde buscar el producto. Por omision, la carpeta hermana.
RUTA_DEL_PRODUCTO = Path(
    os.environ.get("CORE_POS_REPO", Path(__file__).resolve().parents[2] / "CoreAPP")
)
DECLARACION = RUTA_DEL_PRODUCTO / "apps" / "plataforma" / "planes.py"


def planes_del_producto():
    """Lee los planes del producto sin importarlo: son dos proyectos distintos.

    Se analiza el arbol del archivo y no su texto: una expresion regular se
    rompe el dia que alguien reformatee el codigo del producto, y entonces esta
    prueba fallaria por una razon que no tiene nada que ver con los precios.
    """
    arbol = ast.parse(DECLARACION.read_text(encoding="utf-8"))
    encontrados = {}
    for nodo in ast.walk(arbol):
        if not (isinstance(nodo, ast.Call) and getattr(nodo.func, "id", "") == "Plan"):
            continue
        datos = {}
        for argumento in nodo.keywords:
            valor = argumento.value
            # `Decimal("12")` llega como llamada: interesa lo que lleva dentro.
            if isinstance(valor, ast.Call) and valor.args:
                valor = valor.args[0]
            if isinstance(valor, ast.Constant):
                datos[argumento.arg] = valor.value
        if "clave" in datos:
            encontrados[datos["clave"]] = datos
    return encontrados


@pytest.mark.skipif(
    not DECLARACION.exists(),
    reason=(
        "No se encontro Core Pos, asi que NO se verifico que los precios del "
        "sitio coincidan con los del sistema. Ponga CORE_POS_REPO apuntando al "
        "repositorio del producto para que esta garantia se compruebe."
    ),
)
def test_los_planes_del_sitio_son_los_que_cobra_el_producto():
    del_producto = planes_del_producto()

    assert {p.clave for p in PLANES} == set(del_producto), (
        "el sitio y el producto no ofrecen los mismos planes"
    )

    for plan in PLANES:
        real = del_producto[plan.clave]
        assert plan.precio_mensual == Decimal(str(real["precio_mensual"])), (
            f"el plan {plan.clave} cuesta {real['precio_mensual']} en el sistema "
            f"y el sitio dice {plan.precio_mensual}"
        )
        for limite in ("productos", "personal", "ventas_por_mes"):
            assert getattr(plan, limite) == real[limite], (
                f"el limite '{limite}' del plan {plan.clave} no cuadra: "
                f"sistema {real[limite]}, sitio {getattr(plan, limite)}"
            )


# Esta si corre siempre, aunque el producto no este a mano. Cubre el error mas
# probable: escribir un numero a mano en la plantilla y olvidarlo ahi.
def test_ningun_precio_esta_escrito_a_mano_en_la_plantilla():
    """El numero tiene que salir de la declaracion, no del HTML.

    Se miran solo los textos, no los atributos: las clases de estilo estan
    llenas de cifras (`mt-10`, `gap-1.5`) que no son precios de nada.
    """
    plantilla = (
        Path(__file__).resolve().parents[1] / "templates" / "sitio" / "portada.html"
    ).read_text(encoding="utf-8")
    seccion = plantilla.split('ancla="precios"')[1].split("</c-seccion>")[0]
    sin_atributos = re.sub(r'\w+="[^"]*"', " ", seccion)

    for plan in PLANES:
        cifras = (plan.precio_mensual, plan.productos, plan.personal, plan.ventas_por_mes)
        # Se ignoran las de una sola cifra: aparecen en cualquier texto y no
        # demuestran nada.
        for numero in (n for n in cifras if len(str(n)) > 1):
            assert not re.search(rf"{numero}", sin_atributos), (
                f"el numero {numero} esta escrito a mano en la seccion de precios. "
                "Tiene que salir de sitio/planes.py, o el dia que cambie quedara viejo."
            )


def test_la_plantilla_recorre_la_declaracion():
    """La otra mitad: que los numeros vengan de donde tienen que venir."""
    plantilla = (
        Path(__file__).resolve().parents[1] / "templates" / "sitio" / "portada.html"
    ).read_text(encoding="utf-8")
    seccion = plantilla.split('ancla="precios"')[1].split("</c-seccion>")[0]

    assert "{% for plan in planes %}" in seccion
    assert "plan.precio_visible" in seccion
    assert "plan.limites" in seccion


@pytest.mark.django_db
def test_los_tres_planes_se_ven_con_su_precio(client):
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    for plan in PLANES:
        assert plan.nombre in cuerpo
        assert plan.precio_visible in cuerpo


@pytest.mark.django_db
def test_se_dice_que_el_de_entrada_es_gratis_y_sin_tarjeta(client):
    """Es lo que quita el miedo a probarlo."""
    cuerpo = client.get(reverse("sitio:portada")).content.decode()

    assert "Gratis" in cuerpo
    assert "sin tarjeta" in cuerpo.lower()


def test_hay_exactamente_un_plan_destacado():
    """Dos destacados no destacan nada, y ninguno deja la eleccion sin guia."""
    assert sum(1 for plan in PLANES if plan.destacado) == 1
