# Tasks: F1 — La pagina

**Input**: `specs/001-la-pagina/` (spec.md, plan.md)

**Pruebas**: obligatorias. El criterio de cierre es una medida, y el contenido
tiene una prueba propia porque la tentacion de hablar en tecnico es constante.

---

## Fase 1 · Armazon

- [x] **T001** `base.html`: cabecera fija, pie, estilos, guiones locales
- [x] **T002** Componentes: boton, seccion, tarjeta
- [x] **T003** Guion del sitio en archivo aparte, sin nada en linea
- [x] **T004** Navegacion por anclas, visible en telefono

## Fase 2 · Las secciones *(US1 a US5, US7)*

- [x] **T005** [US1] Heroe con su frase y el boton de contacto
- [x] **T006** [US2] Los cinco problemas, en su voz, con su respuesta
- [x] **T007** [US3] Los tres pasos de como se empieza
- [x] **T008** [US4] Lo que hace, agrupado por lo que resuelve
- [x] **T009** [US4] Lo que no hace, dicho sin rodeos
- [x] **T010** [US5] Seccion de capturas, con su espacio reservado
- [x] **T011** [US7] Preguntas frecuentes, plegables sin JavaScript
- [x] **T012** Cierre con llamada al contacto y enlace de WhatsApp
- [x] **T013** Pie con lo legal y el contacto

## Fase 3 · Precios *(US6)*

- [x] **T014** [US6] `planes.py` con los tres planes
- [x] **T015** [US6] Seccion de precios, recorriendo la declaracion
- [x] **T016** [US6] Prueba: los planes del sitio cuadran con los de Core Pos
- [x] **T017** [US6] Prueba: ningun numero de plan escrito a mano en la plantilla

## Fase 4 · Cierre

- [x] **T018** Prueba: ninguna palabra vetada aparece en la pagina
- [x] **T019** Prueba: todas las secciones estan presentes
- [x] **T020** Prueba de presupuesto: menos de 150 KB comprimidos
- [x] **T021** Prueba: nada se carga desde otro servidor
- [x] **T022** Actualizar README
- [x] **T023** Cerrar la fase: fusionar a `main` y etiquetar `v0.2.0-f1`

---

## Estado

Todas las tareas completadas el 2026-09-11. Suite: 94 pruebas en verde.

Medidas al cerrar:
- Primera carga: **12 KB** comprimidos, de un presupuesto de 150.
  (HTML 7,0 · estilos 4,5 · guion 0,5)
- Las nueve secciones presentes y la pagina completa en 360 px.
- Los tres planes cuadrando con los de Core Pos, verificado contra su codigo.

Dos pruebas que hubo que corregir porque median mal:

- La de "nada viene de afuera" contaba tambien los enlaces a WhatsApp y al
  sistema. Un enlace es un destino al que la persona decide ir, no un recurso
  que el navegador descargue al abrir. Ahora mira solo guiones, imagenes,
  marcos y hojas de estilo.
- La de "ningun precio escrito a mano" buscaba cifras en el HTML crudo y
  chocaba con las clases de estilo, que estan llenas de numeros (`mt-10`,
  `gap-1.5`). Ahora quita los atributos antes de buscar, e ignora las cifras de
  un solo digito porque no demuestran nada.

Y una decision que cambio al construir: el analizador que lee los planes del
producto empezo siendo una expresion regular y termino siendo un recorrido del
arbol sintactico. Una expresion regular se rompe el dia que alguien reformatee
el codigo del producto, y entonces la prueba fallaria por una razon que no tiene
nada que ver con los precios.

## Criterio de cierre

La pagina se lee en 360 px, pesa menos de 150 KB, sin palabras vetadas, y los
precios cuadran con el producto.
