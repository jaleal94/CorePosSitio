# Implementation Plan: F5 — Plan unico

**Branch**: `005-plan-unico` | **Date**: 2026-09-15 | **Spec**: [spec.md](./spec.md)

---

## Summary

Dos trabajos de tamano muy distinto. Uno es la seccion de precios: pasa de tres
fichas a una y gana un segundo numero. El otro, que es el de verdad, es cazar
las seis promesas de "gratis" repartidas por el sitio, incluida una que no esta
en ninguna plantilla porque vive dentro de una imagen.

Lo que hace esto abordable es que el contenido ya vive en `sitio/contenido.py` y
`sitio/planes.py`, y no en el HTML. Pero la busqueda hay que hacerla igual,
porque las promesas estan escritas con palabras distintas en cada sitio.

## Technical Context

**Dependencias nuevas**: ninguna

**Storage**: ninguno

**Pruebas**: precios contra el producto, cero promesas de gratis, peso

**Constraints**: el presupuesto de 150 KB sigue; principio I, nada que no sea cierto

**Scale/Scope**: 0 modelos, 0 vistas nuevas

## Constitution Check

| Principio | Como lo cumple | Estado |
|---|---|---|
| I. Nada que no sea cierto | Es el criterio de la fase: se quitan seis promesas que dejaron de serlo | PASA |
| II. Un minuto para entender | Un plan se entiende mas rapido que tres | PASA |
| III. El contacto nunca se pierde | No se toca el formulario | N/A |
| IV. Carga rapida | Una ficha menos; la imagen de compartir se rehace igual de pesada | PASA |
| V. Se lee en un telefono | La ficha unica se centra en vez de encogerse a un tercio | PASA |
| VI. Mismo stack | Sin dependencias nuevas | PASA |
| VII. Lo que se dice se prueba | Los dos precios se comparan con el producto | PASA |
| VIII. Se cierra en verde | Cierra con suite verde y etiqueta `v1.2.0` | PASA |
| IX. Espanol de Venezuela | Cambia texto, en el mismo idioma | PASA |
| X. Nada de datos de nadie | No se toca | N/A |

Sin desviaciones.

## Decisiones de diseño

### 1. La prueba de las promesas recorre paginas, no archivos

Buscar "gratis" en las plantillas encontraria cinco de las seis. La sexta esta
en la descripcion que se arma en `contenido.py`, y una septima podria aparecer
manana en cualquier sitio. La prueba pide cada pagina publica al servidor y
mira lo que sale, que es lo que la gente lee.

La imagen de compartir es el caso que ninguna prueba de texto agarra: ahi la
promesa son pixeles. Esa se comprueba de la unica forma honesta, mirando que el
guion que la genera no escriba esa frase.

### 2. Una ficha, centrada, con los dos numeros a distinta altura

Tres fichas en rejilla se convierten en una. Dejarla ocupando un tercio de la
pantalla la haria parecer un resto de lo que hubo.

Los dos precios no pueden verse igual: 19,99 al mes y 60 una vez son cosas
distintas y la ficha tiene que decirlo con el tamano, no solo con la palabra.

### 3. `Plan` pierde casi todo

Se van `es_gratuito`, `destacado`, `para_quien` y `limites`. Con un solo plan,
destacar no destaca nada y "para quien" ya lo dice el titular de la pagina.

## Project Structure

```text
sitio/planes.py                 un plan, dos precios
sitio/contenido.py              el apoyo del titular y la pregunta de precios
templates/base.html             la descripcion para buscadores y redes
templates/sitio/portada.html    precios, contacto y el boton de pedir
templates/sitio/gracias.html    el boton de pedir
herramientas/imagen_de_compartir.py
tests/test_precios.py           los dos precios contra el producto
tests/test_promesas.py          cero gratis en todo el sitio
```

## Orden de construccion

1. La prueba de las promesas. Primero, porque es la que dice cuando esta hecho.
2. `planes.py` y la seccion de precios.
3. El resto del texto: titular, descripcion, contacto, gracias, preguntas.
4. La imagen de compartir.
5. Cerrar.

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| Queda un "gratis" en una pagina que nadie mira | La prueba recorre todas las publicas |
| Queda la promesa dentro de la imagen | Prueba sobre el guion que la genera |
| El precio de la pagina se separa del que se cobra | Prueba que compara los dos numeros con el producto |
| Alguien escribe 19,99 a mano en la plantilla | La prueba de numeros a mano, que ya existe |
