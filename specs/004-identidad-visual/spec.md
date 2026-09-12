# F4 — Identidad visual

**Rama**: `004-identidad-visual`
**Criterio de cierre**: el logo y su paleta gobiernan todo el sitio, con el contraste verificado por prueba.

---

## Por que esta fase

El sitio se ve limpio y se ve **generico**. El color de acento es un indigo que
no significa nada, no hay marca, y quien lo abre no se lleva ninguna imagen que
recordar.

Ahora hay un logo, y con el una paleta. Aplicarla no es pintar: es decidir que
hace cada color, y esa decision tiene consecuencias que se miden.

---

## El logo y lo que trae

Una **C** en azul marino abierta hacia la derecha, de la que sale una **flecha
hacia arriba** en verde azulado. Debajo, "Core" en el mismo azul y "Pos" en
gris.

Lee bien lo que el producto promete: algo que crece. Y los dos colores se
reparten el trabajo solos: el azul es la estructura, el verde es el movimiento.

### La paleta

| Color | Valor | Contraste sobre blanco | Para que sirve |
|---|---|---|---|
| Azul marino | `#2B4270` | **9,92:1** | Texto, botones, todo lo que lleva letra |
| Verde azulado | `#4FA898` | **2,84:1** | Solo el logo y adornos sin texto |
| Gris | `#58595B` | **7,01:1** | Texto secundario |

**El verde del logo no puede llevar texto.** Con 2,84:1 no alcanza ni para
texto grande, que pide 3:1. Un boton verde con letras blancas seria ilegible
para mucha gente, y el sitio dice que cualquiera puede usarlo.

De ahi la decision central de la fase.

---

## Decisiones

| # | Decision |
|---|---|
| D-01 | El **azul marino es el color de accion**: botones, enlaces, foco. El verde queda para el logo y para adornos que no lleven texto. |
| D-02 | Para cuando haga falta verde con letra encima se usa una **version oscurecida**, `#2E7466` (5,52:1). El logo conserva su verde original: la marca no se toca. |
| D-03 | Los colores de estado —bien, atencion, problema— se mantienen **separados del verde de marca**, para que "cuadro la caja" y "este es el boton" no se confundan. |
| D-04 | La paleta se declara **una sola vez** por proyecto, y una prueba comprueba que la del sitio y la de Core Pos son la misma. |

### Por que el azul lleva la accion, y no el verde (D-01)

Lo natural seria poner el verde en el boton de accion: es el color vivo, el que
llama. Dos razones lo impiden.

La primera es el contraste: no alcanza, y oscurecerlo hasta que alcance lo aleja
tanto del logo que deja de ser el mismo color.

La segunda es mas de fondo. En un punto de venta el verde **ya significa algo**:
dinero que entro, caja que cuadra, existencia sana. Si el verde es ademas "pulse
aqui", quien trabaja con esto diez horas al dia va a tener que decidir cada vez
que significa el verde que esta mirando. El azul marino no compite con nada y
tiene casi diez a uno de contraste.

El verde no desaparece: es del logo, de los subrayados, de las cifras que suben,
de los detalles. Sigue siendo la mitad de la identidad.

---

## Historias de usuario

### US1 — Reconocer la marca *(P1)*

**Criterios de aceptacion**
1. El logo esta en la cabecera, en el pie y en el icono de la pestaña.
2. Se ve nitido en pantallas densas y en 360 px de ancho.
3. Tiene texto alternativo, y la cabecera no repite el nombre dos veces para un
   lector de pantalla.
4. Pesa poco: no puede tumbar el presupuesto.

### US2 — Que el sitio se vea de una pieza *(P2)*

**Criterios de aceptacion**
1. Ningun color indigo queda en el sitio.
2. Los botones, los enlaces y el anillo de foco usan el azul de marca.
3. Los colores de estado siguen distinguiendose del verde de marca.
4. La imagen de compartir usa la paleta y el logo.

### US3 — Que se siga leyendo *(P3)*

Es el riesgo real de cambiar colores: que quede bonito e ilegible.

**Criterios de aceptacion**
1. Toda combinacion de texto y fondo del sitio llega a 4,5:1, o a 3:1 si es
   texto grande.
2. Hay una prueba que lo comprueba sobre la paleta declarada, no a ojo.
3. El anillo de foco se ve sobre todos los fondos.

### US4 — Que las dos partes se vean iguales *(P4)*

Quien entra al sistema desde el sitio no puede sentir que cambio de empresa.

**Criterios de aceptacion**
1. La paleta del sitio y la de Core Pos son la misma, comprobado por prueba.
2. El logo es el mismo archivo en los dos.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | El logo en SVG, servido desde el propio sitio |
| FR-02 | Version reducida —solo la marca, sin texto— para espacios chicos |
| FR-03 | Icono de pestaña en los tamaños que piden los navegadores |
| FR-04 | Paleta declarada una sola vez, en la hoja de estilos |
| FR-05 | Ningun resto del indigo anterior |
| FR-06 | Prueba de contraste sobre la paleta declarada |
| FR-07 | Prueba de que la paleta cuadra con la de Core Pos |
| FR-08 | Imagen de compartir regenerada con la marca |
| FR-09 | El presupuesto de peso se sigue cumpliendo |

---

## Lo que hace falta antes de empezar

**El archivo del logo.** En SVG si existe: escala sin perder nitidez, pesa unos
pocos kilobytes y permite recolorearlo. Si solo hay PNG, sirve con fondo
transparente y al menos 1.000 px de ancho.

Sin el, los valores de color de arriba son una lectura de la imagen, buena pero
no exacta, y la marca se veria aproximada en vez de correcta.

---

## Fuera de alcance

- Rediseñar la pagina. Esto cambia colores y pone el logo; la estructura queda.
- Un manual de marca.
- Modo oscuro.

---

## Criterio de cierre

El logo en su sitio, la paleta gobernando todo, cero indigo, el contraste
verificado por prueba y el peso dentro del presupuesto.
