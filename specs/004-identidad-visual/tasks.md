# Tasks: F4 — Identidad visual

**Input**: `specs/004-identidad-visual/` (spec.md, plan.md)

**Depende de**: la fase equivalente en Core Pos, que va primero. Si no, las
capturas del sitio quedan con la paleta vieja y hay que rehacerlas dos veces.

**Hace falta**: el archivo del logo. En SVG si existe; si no, PNG con fondo
transparente y al menos 1.000 px de ancho.

---

## Fase 1 · La paleta *(US3)*

- [ ] **T001** Prueba de contraste, que calcula sobre la paleta declarada
- [ ] **T002** Paleta nueva en `assets/tailwind.css`, con sus nombres separados
- [ ] **T003** Verde de marca y verde de estado, distintos y con prueba
- [ ] **T004** Prueba: no queda ningun indigo en el sitio
- [ ] **T005** Anillo de foco visible sobre todos los fondos

## Fase 2 · El logo *(US1)*

- [ ] **T006** `logo.svg` y `logo-marca.svg`, servidos desde el sitio
- [ ] **T007** Icono de pestaña
- [ ] **T008** El logo en la cabecera, sin repetir el nombre para un lector
- [ ] **T009** El logo en el pie
- [ ] **T010** Prueba: el logo existe, se enlaza y tiene texto alternativo

## Fase 3 · El resto *(US2, US4)*

- [ ] **T011** Imagen de compartir regenerada con la marca
- [ ] **T012** Prueba: la paleta cuadra con la de Core Pos
- [ ] **T013** Capturas regeneradas con la paleta nueva
- [ ] **T014** Prueba: el peso sigue dentro del presupuesto
- [ ] **T015** Actualizar README
- [ ] **T016** Cerrar la fase: fusionar a `main` y etiquetar `v1.1.0`

---

## Criterio de cierre

El logo en su sitio, cero indigo, el contraste verificado por prueba, la paleta
igual que la del producto, y el peso dentro del presupuesto.
