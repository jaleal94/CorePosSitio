# Tasks: F5 — Plan unico

**Input**: `specs/005-plan-unico/` (spec.md, plan.md)

**Depende de**: la fase equivalente en Core Pos, que va primero. La prueba que
compara los precios lee su declaracion.

---

## Fase 1 · Las promesas *(US2)*

Va primero: es la prueba que dice cuando esta hecho.

- [ ] **T001** Prueba: ninguna pagina publica promete gratis ni sin tarjeta
- [ ] **T002** Prueba: la imagen de compartir tampoco lo promete

## Fase 2 · El plan *(US1)*

- [ ] **T003** Un solo plan en `sitio/planes.py`, con mensualidad e instalacion
- [ ] **T004** Prueba: los dos precios son los del producto
- [ ] **T005** La seccion de precios: una ficha, dos numeros
- [ ] **T006** Prueba: ningun precio escrito a mano en la plantilla

## Fase 3 · El resto del texto *(US2, US3)*

- [ ] **T007** El apoyo del titular
- [ ] **T008** La descripcion para buscadores y redes
- [ ] **T009** La seccion de contacto y el boton de pedir la tienda
- [ ] **T010** La pagina de gracias
- [ ] **T011** La pregunta frecuente de precios

## Fase 4 · Cierre

- [ ] **T012** Imagen de compartir regenerada
- [ ] **T013** Prueba: el peso sigue dentro del presupuesto
- [ ] **T014** Actualizar README
- [ ] **T015** Cerrar la fase: fusionar a `main` y etiquetar `v1.2.0`

---

## Criterio de cierre

Un plan con sus dos precios, cero promesas de gratis en todo el sitio, la
prueba que compara con el producto en verde, y el peso dentro del presupuesto.
