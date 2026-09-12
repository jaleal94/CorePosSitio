# Tasks: F4 — Identidad visual

**Input**: `specs/004-identidad-visual/` (spec.md, plan.md)

**Depende de**: la fase equivalente en Core Pos, que va primero. Si no, las
capturas del sitio quedan con la paleta vieja y hay que rehacerlas dos veces.

**Hizo falta**: el archivo del logo. Llego en PNG de 677 x 369, y vive en Core
Pos: aqui no hay una segunda copia.

---

## Fase 1 · La paleta *(US3)*

- [x] **T001** Prueba de contraste, que calcula sobre la paleta declarada
- [x] **T002** Paleta nueva en `assets/tailwind.css`, con sus nombres separados
- [x] **T003** Verde de marca y verde de estado, distintos y con prueba
- [x] **T004** Prueba: no queda ningun indigo en el sitio
- [x] **T005** Anillo de foco visible sobre todos los fondos

## Fase 2 · El logo *(US1)*

- [x] **T006** `logo.png` y `logo-marca.png`, servidos desde el sitio
- [x] **T007** Icono de pestaña
- [x] **T008** El logo en la cabecera, sin repetir el nombre para un lector
- [x] **T009** El logo en el pie
- [x] **T010** Prueba: el logo existe, se enlaza y tiene texto alternativo

## Fase 3 · El resto *(US2, US4)*

- [x] **T011** Imagen de compartir regenerada con la marca
- [x] **T012** Prueba: la paleta cuadra con la de Core Pos
- [x] **T013** Capturas regeneradas con la paleta nueva
- [x] **T014** Prueba: el peso sigue dentro del presupuesto
- [x] **T015** Actualizar README
- [x] **T016** Cerrar la fase: fusionar a `main` y etiquetar `v1.1.0`

---

## Criterio de cierre

El logo en su sitio, cero indigo, el contraste verificado por prueba, la paleta
igual que la del producto, y el peso dentro del presupuesto.

---

## Estado

**184 pruebas en verde.** 40 de ellas nuevas, todas de identidad.

### Lo que se midio

Los 18 pares de texto y fondo que el sitio pinta de verdad pasan el minimo de la
norma. Los mas ajustados:

| Par | Razon | Minimo |
|---|---|---|
| `atencion` sobre `lienzo` | 4,74:1 | 4,50 |
| `atencion` sobre blanco | 5,00:1 | 4,50 |
| `borde-fuerte` sobre `lienzo` | 3,07:1 | 3,00 |

La paleta cuadra con la de Core Pos color por color, leida de su hoja. Los
cuatro archivos del logo son los mismos bytes que los del producto.

Peso: 5 KB de hoja y guion comprimidos, 7 KB de la marca. El presupuesto de
150 KB sigue lejos.

### Lo que aparecio al mirar

**Los campos del formulario no tenian borde ni fondo.** Tailwind se los quita a
todo control por omision, y el sitio nunca los vistio. El resultado era que
"Dejenos sus datos y le escribimos" -lo unico que este sitio tiene que
conseguir- se veia como una lista de textos grises sueltos, sin una sola caja
donde escribir. Se visten en `@layer base`, como en el producto.

No es un defecto de color, pero se encontro mirando la pagina con la paleta
nueva, y dejarlo para otra fase habria sido dejar el sitio sin su unica
conversion.

**La imagen de compartir se habia quedado con el indigo viejo.** Tenia sus
propias cifras de color escritas a mano y un comentario que decia "sin necesitar
un logotipo que todavia no existe". Ahora lee la paleta de la hoja y trae el
logo de verdad. La imagen que mas gente ve acaba siendo la que nadie vuelve a
mirar.

**La captura del telefono salia cortada por la derecha desde F3.** Se pedian
420 px de ancho, pero en modo sin ventana Chrome y Edge no bajan de 500: la
ventana era de 500 y la foto se recortaba a 420, asi que en la captura que
enseña como se cobra faltaba justo la columna del total. Se pide 500, que es lo
que el navegador da, y la proporcion de la plantilla se ajusto.

**Sobraba el remiendo que borraba los comentarios del producto.** El guion de
capturas quitaba los `{# #}` de varias lineas que Core Pos servia como texto
visible. El producto ya los corrigio en su fase de identidad, asi que la linea
se fue.
