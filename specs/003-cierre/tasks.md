# Tasks: F3 — Cierre

**Input**: `specs/003-cierre/` (spec.md, plan.md)

---

## Fase 1 · Las capturas *(US1)*

- [x] **T001** Guion `herramientas/capturas.py`, con Core Pos como biblioteca
- [x] **T002** Datos de ejemplo de una bodega inventada, reconocible como tal
- [x] **T003** Renderizado con sesion iniciada de las tres pantallas
- [x] **T004** Fotografiado con el navegador sin cabeza, en su proporcion
- [x] **T005** Optimizacion de las imagenes al generarlas
- [x] **T006** Las capturas en la seccion "Asi se ve"
- [x] **T007** Prueba: las tres capturas existen y estan enlazadas

## Fase 2 · Compartir y buscadores *(US2, US3)*

- [x] **T008** [US2] Etiquetas para compartir en las tres paginas publicas
- [x] **T009** [US2] Imagen de portada para compartir
- [x] **T010** [US3] Mapa del sitio
- [x] **T011** [US3] `robots.txt` que cierra el panel
- [x] **T012** [US3] La pagina de gracias y el panel, sin indexar
- [x] **T013** [US3] Datos estructurados con marca de un solo uso
- [x] **T014** [US2] Prueba: las etiquetas estan en cada pagina publica
- [x] **T015** [US3] Prueba: el mapa lista lo publico y nada privado

## Fase 3 · Cierre *(US4)*

- [x] **T016** [US4] Paginas de error 404 y 500
- [x] **T017** Prueba: el peso sigue cumpliendose con las imagenes
- [x] **T018** Actualizar README
- [x] **T019** Cerrar la fase: fusionar a `main` y etiquetar `v1.0.0`

---

## Estado

Todas las tareas completadas el 2026-09-11. Suite: 144 passed.

Medidas al cerrar:
- Primera carga **33 KB** comprimidos; la pagina entera con sus tres capturas,
  **75 KB**. El presupuesto es 150.
- Las tres capturas salen del sistema real, generadas por un guion reproducible.

Lo que aparecio al fotografiar las pantallas, y es lo mas valioso de la fase:

Las primeras capturas salieron con texto raro arriba: comentarios de plantilla
visibles. La causa es que en Django `{# #}` **es de una sola linea**, y un
comentario escrito asi en varias no se elimina: se sirve como texto. Django no
avisa.

El sitio tenia seis, repartidos entre el armazon y la portada, visibles en todas
sus paginas. Se corrigieron pasandolos a `{% comment %}` y hay una prueba que
recorre las tres paginas publicas y falla si vuelve a pasar.

**Core Pos tiene el mismo defecto**, con dos comentarios en su armazon que se
ven en todas sus pantallas. No se corrigio, porque el producto no se toca en
este trabajo: queda reportado. El guion de capturas los quita antes de
fotografiar, para no retratar un defecto suyo, y esa linea sobra el dia que se
arregle alla.

## Criterio de cierre

Capturas reales en la pagina, el enlace se comparte con imagen, los buscadores
tienen su mapa, y el peso sigue por debajo de 150 KB.
