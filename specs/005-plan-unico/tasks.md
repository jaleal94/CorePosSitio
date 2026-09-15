# Tasks: F5 — Plan unico

**Input**: `specs/005-plan-unico/` (spec.md, plan.md)

**Depende de**: la fase equivalente en Core Pos, que va primero. La prueba que
compara los precios lee su declaracion.

---

## Fase 1 · Las promesas *(US2)*

Va primero: es la prueba que dice cuando esta hecho.

- [x] **T001** Prueba: ninguna pagina publica promete gratis ni sin tarjeta
- [x] **T002** Prueba: la imagen de compartir tampoco lo promete

## Fase 2 · El plan *(US1)*

- [x] **T003** Un solo plan en `sitio/planes.py`, con mensualidad e instalacion
- [x] **T004** Prueba: los dos precios son los del producto
- [x] **T005** La seccion de precios: una ficha, dos numeros
- [x] **T006** Prueba: ningun precio escrito a mano en la plantilla

## Fase 3 · El resto del texto *(US2, US3)*

- [x] **T007** El apoyo del titular
- [x] **T008** La descripcion para buscadores y redes
- [x] **T009** La seccion de contacto y el boton de pedir la tienda
- [x] **T010** La pagina de gracias
- [x] **T011** La pregunta frecuente de precios

## Fase 4 · Cierre

- [x] **T012** Imagen de compartir regenerada
- [x] **T013** Prueba: el peso sigue dentro del presupuesto
- [x] **T014** Actualizar README
- [x] **T015** Cerrar la fase: fusionar a `main` y etiquetar `v1.2.0`

---

## Criterio de cierre

Un plan con sus dos precios, cero promesas de gratis en todo el sitio, la
prueba que compara con el producto en verde, y el peso dentro del presupuesto.

---

## Estado

**192 pruebas en verde.** 8 nuevas: 7 de promesas y 1 de que el plan no anuncia
limites que el producto no tiene.

### Lo que cambio

| | Antes | Ahora |
|---|---|---|
| Planes en la pagina | 3 fichas en rejilla | 1 ficha centrada |
| Precio | Gratis / $12 / $35 | $19.99 al mes + $60 una vez |
| Limites anunciados | 9 cifras | ninguna |

### Las siete promesas que habia que cazar

La spec contaba seis. La prueba encontro una mas al recorrer las paginas de
verdad en vez de los archivos, que es justo la razon de haberla escrito asi:

1. El apoyo del titular — "Empiece gratis, sin tarjeta"
2. La descripcion para buscadores y para la tarjeta de WhatsApp — "Empiece gratis"
3. La entrada de la seccion de contacto — "sin compromiso y sin tarjeta"
4. El bloque de pedir la tienda — "Es gratis y no pide tarjeta"
5. El boton de la pagina de gracias — "Pedir mi tienda gratis"
6. La imagen de compartir — "Empiece gratis, sin tarjeta", en pixeles
7. **La seccion de precios** — "Sin tarjeta y sin tiempo limite", "Empiece
   gratis", "cambie de plan cuando quiera" y "si se pasa de los limites"

La septima estaba a la vista y aun asi era la mas facil de dejar: al reescribir
la ficha de precios uno mira los numeros, no la letra pequena de debajo.

### Lo que se decidio por el camino

**El boton de pedir la tienda se queda.** Pedirla no entrega nada: crea una
solicitud que espera hasta que se aprueba, y eso ahora pasa despues de cobrar.
Lo que no era cierto era como estaba escrito —"sin hablar con nadie"— cuando
ahora hay que hablar para acordar la instalacion.

**Los dos precios no se ven igual.** La mensualidad grande, la instalacion
debajo con "una sola vez" pegado. Un precio de entrada que se lee como mensual
espanta, y uno mensual que se lee como unico defrauda al llegar el segundo mes.
Hay prueba de que las palabras estan, no solo el tamano.
