# Implementation Plan: F2 — Captacion

**Branch**: `002-captacion` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

---

## Summary

Un modelo, un formulario, un panel. Poca superficie y una sola regla que manda
sobre todo: **el contacto se guarda antes que nada, y nada de lo que venga
despues puede tumbarlo**.

Es la unica fase del sitio que toca la base de datos y la unica que recibe algo
del publico sin autenticar, asi que es tambien donde se concentra el riesgo.

## Technical Context

**Dependencias nuevas**: ninguna

**Storage**: un modelo, `Contacto`

**Pruebas**: que se guarde siempre, que un reenvio no duplique, que el robot no pase, que el panel exija sesion, y que el enlace de WhatsApp lleve el mensaje correcto

**Constraints**: el formulario es publico; el panel no puede verse sin sesion

**Scale/Scope**: 1 modelo, 6 vistas

## Constitution Check

| Principio | Como lo cumple | Estado |
|---|---|---|
| I. Nada que no sea cierto | La pagina de gracias promete un plazo que se puede cumplir; no promete aviso automatico | PASA |
| II. Un minuto para entender | El formulario pide cuatro cosas, no doce | PASA |
| III. El contacto nunca se pierde | El guardado ocurre primero y en su propia transaccion | PASA — es el criterio de la fase |
| IV. Carga rapida | Sin dependencias nuevas; el formulario no agrega guiones | PASA |
| V. Se lee en un telefono | Campos con el teclado correcto y area tactil de 44 px | PASA |
| VI. Mismo stack | Sin dependencias nuevas | PASA |
| VII. Lo que se dice se prueba | El plazo de respuesta que promete la pagina sale de una constante, no del texto suelto | PASA |
| VIII. Se cierra en verde | Cierra con suite verde y etiqueta `v0.3.0-f2` | PASA |
| IX. Espanol de Venezuela | "Como se llama su negocio", "le escribimos hoy mismo" | PASA |
| X. Nada de datos de nadie | Los contactos no salen del servidor; sin servicios externos (D-02) | PASA |

Sin desviaciones.

## Decisiones de diseño

### 1. El telefono es la llave (D-01)

No el correo. En el publico de este sitio, mucha gente no tiene correo o no lo
revisa, y el telefono es lo que de verdad identifica a un comercio.

Se guarda normalizado —solo digitos— para que `0414-123.45.67` y `04141234567`
sean el mismo, que es lo que una persona esperaria.

**Rechazado**: dejar el telefono tal como lo escriben. Es mas fiel a lo que
tecleo y hace que el mismo comercio entre tres veces con tres formatos.

### 2. El reenvio actualiza, no duplica

Quien manda el formulario y no ve respuesta en una hora, lo manda otra vez. Eso
no es un error suyo: es lo normal.

Se usa la restriccion unica sobre el telefono y se captura el choque, igual que
la venta idempotente del producto. No se comprueba antes de insertar: entre la
comprobacion y la insercion hay una ventana, y es justo donde cae el segundo
envio.

Lo que se actualiza es el mensaje y la fecha; el estado y las notas del operador
no se tocan, porque son trabajo suyo.

### 3. Guardar primero, lo demas despues

El contacto se guarda en su propia transaccion. Armar el enlace, registrar de
donde vino, cualquier cosa que se agregue despues: todo eso ocurre fuera, y si
falla, el contacto ya esta.

### 4. La trampa para robots es un campo que nadie ve

Un campo con nombre creible —`sitio_web`— escondido con estilos y marcado como
`autocomplete="off"` y `tabindex="-1"`, fuera del recorrido del teclado y
anunciado a los lectores de pantalla como lo que es. Si llega lleno, se
responde igual que a un envio bueno, pero no se guarda.

Responder "gracias" a un robot es deliberado: decirle que fue detectado le
enseña a la siguiente pasada.

**Rechazado**: un captcha. Carga un guion de otro servidor —lo prohibe el
principio IV—, manda datos a un tercero —lo prohibe el X— y le pide trabajo a
una persona que ya decidio escribirnos.

### 5. El panel usa las cuentas de Django (D-03)

Es para una o dos personas. Un sistema de cuentas propio seria construir F1 de
Core Pos otra vez para nada.

### 6. El plazo que se promete sale de una constante

La pagina de gracias dice cuanto se tarda en responder. Ese numero vive en un
sitio y la prueba comprueba que la pagina lo diga: prometer "en una hora" en el
texto y no poder cumplirlo es exactamente lo que el principio I prohibe.

## Project Structure

```text
sitio/
├── models.py         Contacto
├── formularios.py    el formulario publico, con su trampa
├── servicios.py      registrar_contacto, enlace_de_whatsapp
├── views.py          + contacto, gracias, panel, cambiar_estado, exportar
├── admin.py
├── management/commands/contactos_pendientes.py
└── tests/

templates/sitio/
├── gracias.html
├── privacidad.html
└── panel/contactos.html
```

## Riesgos

| Riesgo | Mitigacion |
|---|---|
| Un contacto se pierde por un fallo posterior | Se guarda primero y aparte; hay prueba de que sobrevive a un fallo del resto |
| El formulario se llena de basura | Trampa, limite de tasa, y prueba de las dos |
| El panel queda accesible sin sesion | Prueba que lo intenta sin sesion y exige redireccion |
| Nadie mira el panel y los contactos se enfrian | El comando de pendientes, y decirlo claro en la especificacion |
