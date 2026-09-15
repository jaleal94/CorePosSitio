# F5 — Plan unico

**Rama**: `005-plan-unico`
**Criterio de cierre**: el sitio anuncia un solo plan con sus dos precios, ni una promesa de gratis en ninguna pagina, y la prueba que compara con el producto en verde.

---

## Por que esta fase

Core Pos paso a un solo plan: **19,99 $ al mes mas 60 $ una sola vez por la
instalacion**. Se acabo el plan gratuito.

Cambiar la seccion de precios es la parte facil y es media hora. Lo que hace
esta fase es lo otro: **el sitio promete "gratis" en seis sitios distintos**, y
ninguno esta en la seccion de precios.

| Donde | Que dice hoy |
|---|---|
| El titular | "Empiece gratis, sin tarjeta" |
| La imagen que se ve al compartir por WhatsApp | "Empiece gratis, sin tarjeta" |
| La descripcion para buscadores y redes | "Empiece gratis" |
| La seccion de contacto | "sin compromiso y sin tarjeta" |
| El boton de pedir la tienda | "Es gratis y no pide tarjeta" |
| La pagina de gracias | "Pedir mi tienda gratis" |

Ese es el trabajo de verdad, y es el que importa: el primer principio de este
sitio es **nada que no sea cierto**, y ahora mismo lo mas visible de la pagina
—el titular y lo que se ve cuando alguien manda el enlace— dejaria de serlo.

---

## Decisiones

| # | Decision |
|---|---|
| D-01 | Un solo plan, con sus dos precios: la mensualidad y la instalacion. |
| D-02 | Los dos numeros salen del producto, y la prueba los compara con el. |
| D-03 | Se va toda promesa de gratis, de prueba y de "sin tarjeta". |
| D-04 | Se va el plan sin topes: no se anuncian limites porque no los hay. |
| D-05 | El boton de pedir la tienda se queda; lo que cambia es lo que dice. |

### Por que el precio de instalacion tambien se compara (D-02)

Es el mas caro de equivocar: son 60 $ que alguien lee una vez y recuerda. Si
viviera solo aqui, seria el unico numero de la pagina que nadie verifica contra
el sistema. Se declara en el producto y se compara, igual que la mensualidad.

### Por que no se anuncian limites (D-04)

Porque no los hay. La tentacion seria poner "hasta 2.000 productos" para que la
ficha se vea llena, y seria mentira. La ficha se llena con lo que el sistema
hace, que es bastante.

### Por que se queda el boton de pedir la tienda (D-05)

Pedir la tienda no entrega nada: crea una solicitud que queda en cola hasta que
quien opera la plataforma la aprueba, y eso ahora pasa **despues de cobrar**.
Asi que la puerta no regala nada y puede quedarse.

Lo que ya no es cierto es como esta escrita: dice "sin hablar con nadie", y
ahora hay que hablar para acordar la instalacion.

---

## Historias de usuario

### US1 — Que el precio de la pagina sea el que se cobra *(P1)*

**Criterios de aceptacion**
1. Se ve un solo plan.
2. Se ven los dos precios: 19,99 $ al mes y 60 $ de instalacion.
3. Los dos salen de una declaracion y ninguno esta escrito en la plantilla.
4. Una prueba los compara con los del producto.

### US2 — Que el sitio no prometa nada que ya no es cierto *(P1)*

Es el riesgo de esta fase, y el principio I del proyecto.

**Criterios de aceptacion**
1. Ninguna pagina dice "gratis", "sin tarjeta" ni "sin compromiso".
2. Tampoco la imagen que se ve al compartir.
3. Tampoco la descripcion para buscadores.
4. Una prueba recorre todas las paginas publicas y falla si vuelve alguna.

### US3 — Que se entienda que la instalacion se paga una vez *(P2)*

Un precio de entrada que se lee como mensual espanta; y uno mensual que se lee
como unico defrauda. La diferencia tiene que quedar dicha.

**Criterios de aceptacion**
1. Junto a los 60 $ dice que es una sola vez.
2. La pregunta frecuente de precios lo explica.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | Un solo plan en `sitio/planes.py`, con mensualidad e instalacion |
| FR-02 | El plan no declara limites |
| FR-03 | La seccion de precios muestra un plan, no una rejilla de tres |
| FR-04 | Ni un numero de precio escrito a mano en la plantilla |
| FR-05 | Prueba de que los dos precios son los del producto |
| FR-06 | Prueba de que ninguna pagina promete gratis |
| FR-07 | Imagen de compartir regenerada, sin la promesa vieja |
| FR-08 | La pregunta frecuente de precios, al dia |
| FR-09 | El peso sigue dentro del presupuesto |

---

## Fuera de alcance

- **Cobrar desde el sitio.** No hay pasarela ni la va a haber en esta fase: el
  sitio capta y usted cobra por fuera. Ponerlo seria otro proyecto.
- Descuentos, promociones o precio por volumen.
- Un segundo plan.

---

## Criterio de cierre

Un plan con sus dos precios, cero promesas de gratis en todo el sitio, la
prueba que compara con el producto en verde, y el peso dentro del presupuesto.
