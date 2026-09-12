# Implementation Plan: F1 — La pagina

**Branch**: `001-la-pagina` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

---

## Summary

Una sola pagina, nueve secciones, sin base de datos. Lo dificil no es el
codigo: es que cada frase pase la prueba de "esto lo diria una bodeguera".

La decision que ordena la fase es donde vive el contenido. Va en las plantillas,
no en la base de datos, porque cambiarlo es un commit revisable y no una edicion
sin rastro. Lo unico que sale de una declaracion aparte son los planes, porque
tienen que poder compararse con el producto.

## Technical Context

**Dependencias nuevas**: ninguna

**Storage**: ninguno. Esta fase no toca la base de datos

**Pruebas**: palabras vetadas, presupuesto de peso, planes contra el producto, y que cada seccion este presente

**Constraints**: menos de 150 KB comprimidos; legible a 360 px; sin guiones en linea

**Scale/Scope**: 1 vista, ~10 plantillas, 0 modelos

## Constitution Check

| Principio | Como lo cumple | Estado |
|---|---|---|
| I. Nada que no sea cierto | Cada funcion listada existe hoy; hay una seccion de lo que el producto no hace | PASA |
| II. Un minuto para entender | Prueba automatica de palabras vetadas | PASA |
| III. El contacto nunca se pierde | No aplica todavia: el formulario llega en F2 | N/A |
| IV. Carga rapida | Prueba de presupuesto de peso; nada de otro servidor | PASA — es el criterio de la fase |
| V. Se lee en un telefono | Diseñado a 360 px primero | PASA |
| VI. Mismo stack | Sin dependencias nuevas | PASA |
| VII. Lo que se dice se prueba | Los planes se comparan con los del producto | PASA — con la salvedad de abajo |
| VIII. Se cierra en verde | Cierra con suite verde y etiqueta `v0.2.0-f1` | PASA |
| IX. Espanol de Venezuela | Todo el contenido en la voz del publico | PASA |
| X. Nada de datos de nadie | Sin rastreadores | PASA |

### La salvedad del principio VII, escrita

El principio pide que los precios del sitio se comparen con los del producto.
Los dos viven en repositorios distintos, asi que la prueba busca Core Pos en una
ruta configurable —`CORE_POS_REPO`, y por omision la carpeta hermana— y compara
si lo encuentra.

**En integracion continua no lo va a encontrar**, porque ahi solo esta este
repositorio. Es decir: la comparacion protege al desarrollador y no al
despliegue.

Se acepta por ahora, con dos mitigaciones:
- Cuando no encuentra el producto, la prueba no pasa en silencio: se salta con
  un mensaje que dice que la garantia no se verifico.
- Hay ademas una prueba que si corre siempre: que los numeros de la pagina
  salgan de la declaracion unica y no escritos a mano en la plantilla. Eso evita
  el error mas probable, que es cambiar el plan en un sitio y olvidar el otro.

La alternativa seria un archivo de instantanea versionado aqui y un comando que
lo refresque desde el producto. Queda anotado para F3 si la comparacion se
vuelve critica.

## Decisiones de diseño

### 1. El contenido vive en las plantillas

Sin gestor de contenido y sin tabla de textos. Cambiar una frase es un commit
que alguien puede revisar, y que queda en la historia con su razon.

**Rechazado**: un modelo `Seccion` editable desde el admin. Suena comodo y
significa que el texto de venta cambia sin revision, sin historia y sin prueba.

### 2. Una sola pagina, con anclas

El publico llega de un enlace de WhatsApp y no va a navegar. Todo en una
pagina, con la cabecera fija para que el boton de contacto nunca este lejos.

La excepcion son las paginas legales y la de gracias: esas si son aparte,
porque se enlazan desde el pie y no forman parte del recorrido de venta.

### 3. Los planes, en una declaracion

`sitio/planes.py`, con la misma forma que en el producto. La plantilla los
recorre. Ni un numero escrito a mano en el HTML.

### 4. Las preguntas frecuentes se pliegan sin JavaScript

`<details>` y `<summary>` nativos. Funcionan sin guiones, se pueden buscar con
Ctrl+F aunque esten cerrados, y no cuestan un byte.

**Rechazado**: un componente con Alpine. Mas control del estilo, y una
dependencia y un riesgo para algo que el navegador ya hace.

### 5. El hueco de las capturas se reserva ahora

Las capturas llegan en F3, pero su espacio se deja marcado con su proporcion
exacta. Si no, el diseño se descuadra el dia que entren y hay que rehacer la
seccion.

### 6. La prueba de peso mide lo que carga el navegador

Suma la hoja de estilos y los guiones, comprimidos con gzip, tal como los sirve
el servidor. Medir el archivo sin comprimir seria medir algo que nadie
descarga.

## Project Structure

```text
sitio/
├── planes.py            los tres planes, declarados una vez
├── contenido.py         las listas largas: problemas, funciones, preguntas
├── views.py, urls.py
└── tests/

templates/
├── base.html            armazon: cabecera fija, pie, estilos
├── cotton/              componentes: boton, tarjeta, seccion
└── sitio/
    ├── portada.html     la pagina, que arma las secciones
    └── secciones/       una plantilla por seccion
```

## Orden de construccion

1. Armazon y componentes.
2. Las secciones, de arriba abajo.
3. Los planes y su prueba.
4. Las pruebas de contenido y de peso.

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| El contenido suena a folleto de software | La prueba de palabras vetadas, y releer cada frase en voz de la bodeguera |
| Prometer algo que el producto no hace | Cada funcion listada se contrasta con el codigo del producto al escribirla, y hay una seccion de lo que no hace |
| El peso se escapa sin que nadie note | Prueba de presupuesto que falla al pasarse |
| Las capturas descuadran el diseño en F3 | Se reserva su espacio con la proporcion exacta desde ahora |
