# Tasks: F2 — Captacion

**Input**: `specs/002-captacion/` (spec.md, plan.md)

**Pruebas**: obligatorias. Es la unica superficie del sitio abierta a internet y
la unica que guarda algo de alguien.

---

## Fase 1 · El contacto *(US1, US2, US3)*

- [x] **T001** [US2] Modelo `Contacto` con estado, origen y notas
- [x] **T002** [US1] Formulario publico con sus cuatro campos
- [x] **T003** [US3] Trampa para robots, invisible y accesible
- [x] **T004** [US2] `registrar_contacto`: guarda primero, atomico
- [x] **T005** [US2] Un reenvio del mismo telefono actualiza, no duplica
- [x] **T006** [US1] El formulario en la seccion de contacto de la portada
- [x] **T007** [US1] Pagina de gracias, con el plazo y el enlace de WhatsApp
- [x] **T008** [US3] Limite de tasa por origen, con respuesta que explica
- [x] **T009** [US2] Prueba: el contacto se guarda con lo que escribio
- [x] **T010** [US2] Prueba: el reenvio no duplica y conserva el trabajo del operador
- [x] **T011** [US3] Prueba: un envio con la trampa llena no guarda nada
- [x] **T012** [US1] Prueba: un campo que falta se explica sin perder lo escrito

## Fase 2 · El panel *(US4, US5)*

- [x] **T013** [US4] Vista del panel, solo para el personal
- [x] **T014** [US4] Enlace de WhatsApp por contacto, con su mensaje
- [x] **T015** [US4] Cambio de estado y notas
- [x] **T016** [US4] Cuenta de los que faltan por atender
- [x] **T017** [US5] Exportacion a CSV
- [x] **T018** [US4] Comando `contactos_pendientes`
- [x] **T019** [US4] Prueba: sin sesion no se ve el panel ni la exportacion
- [x] **T020** [US4] Prueba: el enlace de WhatsApp lleva su nombre y su comercio
- [x] **T021** [US4] Registro del modelo en el admin

## Fase 3 · Cierre

- [x] **T022** [US1] Aviso de privacidad, enlazado desde el formulario
- [x] **T023** Prueba: el plazo prometido sale de la constante
- [x] **T024** Prueba: el peso sigue dentro del presupuesto
- [x] **T025** Actualizar README
- [x] **T026** Cerrar la fase: fusionar a `main` y etiquetar `v0.3.0-f2`

---

## Estado

Todas las tareas completadas el 2026-09-11. Suite: 121 pruebas en verde.

Comprobado de punta a punta contra el sitio corriendo: un contacto enviado desde
el formulario aparece en el panel con su telefono normalizado y su enlace de
WhatsApp armado con el nombre de la persona y el de su comercio.

El peso subio de 12,1 a 12,9 KB comprimidos, de 150 de presupuesto.

Dos cosas que aparecieron al construir:

- El limite de tasa respondia 403, "no tiene permiso", cuando permiso es
  exactamente lo que la persona tiene: lo que pasa es que envio demasiado
  seguido. Un mensaje de error que miente es peor que no tener ninguno, asi que
  hay un middleware que lo traduce a un 429 que explica y ofrece WhatsApp como
  salida. Es el mismo problema que aparecio en F8 del producto.
- El estado del limite se filtraba entre pruebas: la primera que enviaba diez
  formularios dejaba bloqueadas a las siguientes, y el fallo aparecia en pruebas
  que no tenian nada que ver. Se limpia la cache entre pruebas.

Y un error que no se cometio por haberlo cometido antes: el guardado captura el
choque de telefono repetido dentro de su propio punto de guardado. Sin el, la
transaccion queda abortada y la consulta siguiente falla tambien. Es el mismo
defecto que se arreglo en F9 del producto.

## Criterio de cierre

Un contacto enviado aparece en el panel con su enlace listo, un reenvio no lo
duplica, un robot no pasa, y la suite queda verde.
