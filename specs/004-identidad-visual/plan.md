# Implementation Plan: F4 — Identidad visual

**Branch**: `004-identidad-visual` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

---

## Summary

Cambiar colores es de las cosas que parecen triviales y no lo son: se toca todo
y no hay forma de revisarlo mirando. Por eso la fase se apoya en dos cosas que
ya existen —la paleta declarada en un solo sitio y el presupuesto de peso— y
agrega una tercera: **una prueba que calcula el contraste**.

El trabajo de verdad son cuatro archivos: la hoja de estilos donde vive la
paleta, el armazon donde va el logo, el guion de la imagen de compartir, y la
prueba nueva.

## Technical Context

**Dependencias nuevas**: ninguna

**Storage**: ninguno

**Pruebas**: contraste calculado sobre la paleta, paleta igual a la de Core Pos, cero indigo, peso

**Constraints**: AA en todo el texto; el presupuesto de 150 KB sigue

**Scale/Scope**: 0 modelos, 0 vistas nuevas

## Constitution Check

| Principio | Como lo cumple | Estado |
|---|---|---|
| I. Nada que no sea cierto | El logo es el suyo, no una aproximacion dibujada | PASA — depende de recibir el archivo |
| II. Un minuto para entender | El color no cambia lo que dice la pagina | N/A |
| III. El contacto nunca se pierde | No se toca | N/A |
| IV. Carga rapida | El logo en SVG pesa unos kilobytes; hay prueba de peso | PASA |
| V. Se lee en un telefono | La version reducida del logo existe para 360 px | PASA |
| VI. Mismo stack | Sin dependencias nuevas | PASA |
| VII. Lo que se dice se prueba | El contraste se calcula, no se estima | PASA — es el criterio de la fase |
| VIII. Se cierra en verde | Cierra con suite verde y etiqueta `v1.1.0` | PASA |
| IX. Espanol de Venezuela | Sin cambios de texto | N/A |
| X. Nada de datos de nadie | Sin recursos de otro servidor: el logo se sirve desde aqui | PASA |

Sin desviaciones.

## Decisiones de diseño

### 1. El contraste se calcula en la prueba, no se confia

La formula de contraste de la norma es corta y determinista. La prueba recorre
los pares de color que el sitio usa de verdad —texto sobre fondo, blanco sobre
boton— y falla con el par exacto y su cifra.

Sin esto, la unica forma de saberlo es abrir una herramienta y mirar, que es
justo lo que nadie hace cuando cambia un tono "un poquito".

### 2. La paleta sigue viviendo en la hoja de estilos

`assets/tailwind.css` ya la declara. Se cambian los valores y nada mas: el resto
del sitio usa nombres —`acento`, `tenue`, `borde`— y no cifras.

Que eso ya estuviera bien hecho es lo que hace que esta fase sea corta.

### 3. La prueba lee los colores de la hoja, no una copia

Si la prueba tuviera su propia lista de colores, comprobaria que una copia es
correcta mientras el sitio usa otra. Lee `assets/tailwind.css` y saca de ahi los
valores.

### 4. El logo en dos versiones

La completa —marca y texto— para la cabecera y el pie. La reducida —solo la
marca— para el icono de pestaña y para donde no quepa el texto.

Las dos en SVG, servidas desde el propio sitio.

### 5. El verde de marca y el verde de estado se separan a proposito

`--color-marca-verde` para la identidad. `--color-sana` para "esto esta bien".
Que sean dos nombres distintos no es pedanteria: el dia que alguien quiera
cambiar el verde de la marca no puede cambiar sin querer el que dice que la caja
cuadro.

### 6. Las capturas se regeneran al final

Si Core Pos cambia de colores, las tres capturas del sitio quedan con la paleta
vieja y el sitio se ve de dos empresas. El guion de F3 existe para esto: se
vuelve a correr y ya.

**Este es el orden que importa**: primero Core Pos, despues el sitio, y las
capturas al final. Al reves habria que rehacerlas dos veces.

## Project Structure

```text
assets/tailwind.css          la paleta, con los valores nuevos
static/img/
├── logo.svg                 completo
├── logo-marca.svg           reducido
└── favicon.svg              el de la pestaña
templates/base.html          el logo en cabecera y pie
herramientas/
└── imagen_de_compartir.py   regenerada con la marca
tests/test_identidad.py      contraste, paleta y cero indigo
```

## Orden de construccion

1. La paleta y la prueba de contraste. Primero la prueba: define lo que se puede
   usar.
2. El logo en sus dos versiones.
3. El armazon y la imagen de compartir.
4. Regenerar capturas y cerrar.

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| Queda bonito e ilegible | La prueba de contraste, que es el criterio de cierre |
| El verde de marca se confunde con el de estado | Nombres distintos y prueba de que se distinguen |
| Las capturas quedan con la paleta vieja | Se regeneran al final, y hay prueba de que existen |
| Los valores de color no son los del logo | Se toman del archivo original, no de una lectura a ojo |
