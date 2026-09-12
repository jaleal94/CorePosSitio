# Implementation Plan: F3 — Cierre

**Branch**: `003-cierre` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

---

## Summary

Tres trabajos distintos que comparten una cosa: son los que quedan cuando el
sitio ya funciona, y por eso son los que nunca se hacen.

El grueso es el primero: **las capturas**. Es la unica parte de la fase con
dificultad real, porque las pantallas del sistema exigen sesion iniciada y datos
dentro, y porque el producto no se puede tocar.

## Technical Context

**Dependencias nuevas**: `pillow` para optimizar las imagenes generadas

**Storage**: ninguno nuevo

**Pruebas**: que las capturas existan y esten enlazadas, que las etiquetas de compartir esten, y que el peso siga cumpliendose con las imagenes dentro

**Constraints**: el presupuesto de 150 KB ahora incluye imagenes; el producto no se modifica

**Scale/Scope**: 1 guion de herramienta, 3 vistas nuevas, 0 modelos

## Constitution Check

| Principio | Como lo cumple | Estado |
|---|---|---|
| I. Nada que no sea cierto | Las capturas salen del sistema real, generadas por un guion reproducible | PASA — es el criterio de la fase |
| II. Un minuto para entender | Las etiquetas de compartir hablan en el mismo lenguaje que la pagina | PASA |
| III. El contacto nunca se pierde | No se toca lo de F2 | N/A |
| IV. Carga rapida | Las imagenes entran al presupuesto y hay prueba | PASA |
| V. Se lee en un telefono | La captura del cobro va en proporcion de telefono | PASA |
| VI. Mismo stack | Una dependencia nueva, solo de herramienta | PASA |
| VII. Lo que se dice se prueba | Las capturas se generan del sistema, no se dibujan | PASA |
| VIII. Se cierra en verde | Cierra con suite verde y etiqueta `v1.0.0` | PASA |
| IX. Espanol de Venezuela | Los datos de ejemplo son de una bodega venezolana | PASA |
| X. Nada de datos de nadie | Sin medicion de visitas ni servicios externos | PASA |

Sin desviaciones.

## Decisiones de diseño

### 1. Core Pos se usa como biblioteca, no se toca (D-01)

El guion agrega la carpeta del producto al camino de importacion, apunta la
base de datos a una propia por variable de entorno, y corre con el entorno del
producto:

```
uv run --project ..\CoreAPP python herramientas/capturas.py
```

Se probo antes de escribir la fase y funciona: la configuracion del producto lee
su `.env` sin pisar lo que ya esta en el entorno, asi que la base se puede
redirigir desde fuera.

**Rechazado**: copiar una prueba dentro del repositorio del producto para que
renderice las pantallas. Es lo mas comodo y significa tocar lo que se dijo que
no se toca.

**Rechazado**: capturar a mano con el telefono. No se puede rehacer, y una
captura que no se puede rehacer envejece hasta que miente.

### 2. Se renderiza con el cliente de pruebas y se fotografia el archivo

Las pantallas exigen sesion. En vez de pelear con un navegador sin cabeza y sus
galletas, el guion usa el cliente de pruebas de Django —que si sabe iniciar
sesion— para obtener el HTML ya renderizado, lo guarda en disco con las rutas
de los estaticos apuntando al disco, y **eso** es lo que fotografia el navegador.

Es mas simple, mas rapido y no depende de que el servidor este levantado.

### 3. La base de la demostracion se crea y se tira (D-02)

`coreapp_demo`, creada por el guion, migrada por el guion y borrada al final si
se pide. La base de desarrollo del producto no se toca ni se lee.

### 4. Los datos de ejemplo se reconocen como ejemplo

"Bodega La Milagrosa", productos de verdad de una bodega venezolana —harina
P.A.N., Malta, cafe—, precios plausibles. Nadie puede confundirlos con los de un
comercio real, y al mismo tiempo se ven creibles.

### 5. Los datos estructurados usan una marca de un solo uso (D-04)

`django-csp` puede emitir una marca por respuesta. El bloque de datos
estructurados la lleva; cualquier otro guion en linea sigue bloqueado.

**Rechazado**: agregar `'unsafe-inline'` a la politica. Abriria justo la puerta
que la politica cierra, y por un bloque de datos que no ejecuta nada.

### 6. Las imagenes se optimizan al generarlas

El guion recorta, redimensiona y guarda en formato comprimido. El presupuesto de
peso pasa a incluirlas, y la prueba de peso ya existente las va a contar sola
porque mira lo que la pagina carga.

## Project Structure

```text
herramientas/
└── capturas.py          genera los datos, renderiza y fotografia

sitio/
├── sitemaps.py          el mapa del sitio
├── views.py             + robots, error 404 y 500
└── templates/sitio/errores/

static/img/              las capturas y la imagen de compartir
```

## Orden de construccion

1. El guion de capturas, que es el trabajo de verdad.
2. Las capturas en la pagina.
3. Compartir y buscadores.
4. Errores y cierre.

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| El guion deja de funcionar cuando el producto cambie | Es una herramienta, no parte del sitio: si falla, se arregla al rehacer capturas, y el sitio no se cae |
| Las capturas tumban el presupuesto | Se optimizan al generarlas y la prueba de peso las cuenta |
| Se filtran datos de un comercio real | La base de la demostracion es propia y los datos son inventados |
| El navegador sin cabeza no esta en el servidor | Solo hace falta para generar capturas, no para servir el sitio |
