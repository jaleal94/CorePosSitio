# F1 — La pagina

**Rama**: `001-la-pagina`
**Criterio de cierre**: se lee entera en un telefono de 360 px y pesa menos de 150 KB.

---

## Por que esta fase

F0 dejo el andamiaje. Esta escribe lo unico que la gente va a ver.

El trabajo real aqui **no es tecnico, es de contenido**. Una pagina de
presentacion se gana o se pierde en la primera frase, y la tentacion es
describir lo que el sistema hace por dentro —modulos, kardex, multi-tenant— en
vez de lo que le pasa a quien lo usa.

La regla que gobierna toda la fase: si una frase del sitio no la diria una
bodeguera, no va.

---

## Historias de usuario

### US1 — Entender en un minuto *(P1)*

Una comerciante abre el enlace que le pasaron por WhatsApp, en su telefono,
entre cliente y cliente. En la primera pantalla sabe que es esto, si es para
ella, y que hacer si le interesa.

**Criterios de aceptacion**
1. La primera pantalla dice que es, para quien es y que resuelve.
2. Ni una palabra tecnica en toda la pagina: ni kardex, ni multi-tenant, ni
   SaaS, ni "nube", ni "modulo".
3. El boton de contacto se ve sin bajar, en 360 px de ancho.
4. Se entiende sin haber usado nunca un punto de venta.

### US2 — Reconocerse en el problema *(P2)*

Antes de que le vendan nada, lee lo que le pasa todos los dias y piensa "eso me
pasa a mi".

**Criterios de aceptacion**
1. Los problemas se enuncian en su voz, en primera persona.
2. Cada problema tiene enfrente lo que el sistema hace al respecto, sin
   exagerar.
3. Ningun problema listado se resuelve con algo que el producto no tenga.

### US3 — Saber que no es complicado *(P3)*

El miedo que frena no es el precio: es "esto es muy complicado para mi".

**Criterios de aceptacion**
1. Tres pasos, no mas, de como se empieza.
2. Se dice cuanto toma poner el catalogo y que se puede subir desde un archivo.
3. Se dice explicitamente que funciona en el telefono.

### US4 — Ver lo que hace *(P4)*

Quiere saber si cubre lo que necesita, sin leer un manual.

**Criterios de aceptacion**
1. Las funciones se agrupan por lo que resuelven, no por modulo.
2. Cada funcion listada existe hoy en el producto.
3. Lo que el producto **no** hace se dice tambien: quien necesita facturacion
   fiscal homologada o comandas de restaurante tiene que enterarse aqui, no
   despues de tres llamadas.

### US5 — Verlo de verdad *(P5)*

Ver el sistema, no una ilustracion.

**Criterios de aceptacion**
1. Capturas reales del producto.
2. Con datos de ejemplo evidentes, nunca de un comercio real.
3. Cada captura dice que se esta viendo.

### US6 — Saber cuanto cuesta *(P6)*

Es la primera pregunta de todo el mundo.

**Criterios de aceptacion**
1. Los tres planes con su precio y sus limites.
2. Se ve claro que el plan de entrada es gratis y que no pide tarjeta.
3. Los numeros salen de una sola declaracion, no escritos por la pagina.
4. Una prueba compara esos numeros con los que Core Pos cobra de verdad.

### US7 — Resolver la duda que la frena *(P7)*

Las preguntas que llegarian por WhatsApp, respondidas antes.

**Criterios de aceptacion**
1. Al menos seis preguntas, plegables.
2. Incluyen las incomodas: que pasa si se va la luz, si se va internet, si me
   quiero ir, quien ve mis datos.
3. Las respuestas son ciertas aunque no sean comodas.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | Pagina unica con las nueve secciones del PRD y navegacion por anclas |
| FR-02 | Armazon de plantilla con cabecera, pie y componentes reutilizables |
| FR-03 | Planes declarados una sola vez y consumidos por la plantilla |
| FR-04 | Prueba que compara los planes del sitio con los de Core Pos |
| FR-05 | Preguntas frecuentes plegables, sin guiones en linea |
| FR-06 | Cabecera fija con el boton de contacto siempre visible |
| FR-07 | Los botones de contacto llevan al ancla del formulario, que llega en F2 |
| FR-08 | Enlace de WhatsApp con el mensaje ya escrito |
| FR-09 | Prueba de que ninguna palabra vetada aparece en la pagina |
| FR-10 | Prueba de presupuesto de peso: menos de 150 KB comprimidos |

---

## El contenido, decidido aqui

Que quede en la especificacion y no solo en la plantilla es deliberado: el
contenido es el producto de esta fase, y cambiarlo es una decision, no un
retoque.

### La frase del heroe

> **Sepa lo que tiene, lo que vende y lo que gana.**
> El punto de venta para bodegas y abastos: cobre rapido, controle su
> mercancia y cuadre la caja todos los dias.

### Los cinco problemas, en su voz

| Lo que dice ella | Lo que hace el sistema |
|---|---|
| "Vendo todo el dia y no se si gano" | Cada venta guarda a que costo salio, asi que el margen sale solo |
| "Se me pierde la mercancia y no se cuanta" | Cada entrada y cada salida quedan anotadas; el estante se cuenta y se cuadra |
| "No se a quien le fie ni cuanto" | Cada fiado queda con nombre, monto y fecha, y se ve quien debe y desde cuando |
| "El proveedor me sube y yo sigo vendiendo igual" | El costo se actualiza al recibir la compra y avisa si el precio quedo corto |
| "Cobro en bolivares y pienso en dolares" | Precio en divisa, cobro a la tasa del dia, y la tasa queda congelada en cada venta |

### Los tres pasos

1. **Cargue lo que vende.** Suba su lista desde una hoja de calculo o escriba
   los primeros veinte productos. Toma menos de lo que teme.
2. **Cobre.** Escanee o busque, elija como le pagan, cobre. La caja se abre en
   la mañana y se cuadra en la noche.
3. **Mire sus numeros.** Cuanto vendio, que deja mas, que hay que reponer, que
   lleva meses sin moverse.

### Palabras vetadas

Una prueba falla si alguna aparece en la pagina: `kardex`, `multi-tenant`,
`multitenant`, `SaaS`, `tenant`, `backend`, `API`, `stack`, `deploy`,
`dashboard`, `onboarding`.

Son las palabras con las que se describe el sistema por dentro. En la pagina no
significan nada para quien la lee.

---

## Fuera de alcance

- El formulario de contacto y su guardado: es F2. Aqui los botones llevan al
  ancla, que en F2 se llena.
- Las capturas reales del sistema: se toman en F3, cuando haya una bodega de
  demostracion con datos presentables. Aqui va el hueco con su medida, para
  que el diseño no se descuadre despues.
- Etiquetas para compartir en redes y mapa del sitio: F3.

---

## Criterio de cierre

La pagina completa se lee en 360 px, pesa menos de 150 KB comprimidos, ninguna
palabra vetada aparece en ella, y los precios cuadran con los de Core Pos.
