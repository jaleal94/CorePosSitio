# PRD — Sitio de presentacion de Core Pos

**Version**: 0.1 · **Fecha**: 2026-09-11

---

## 1. Que es esto

El sitio publico de **Core Pos**: el punto de venta y control de inventario
para bodegas, abastos y comercios pequeños.

No es el producto. Es lo que hace que alguien decida probarlo, y lo que recoge
sus datos para poder llamarlo.

## 2. A quien le habla

**La dueña de una bodega de barrio.** Tiene entre 100 y 2.000 productos, una o
dos personas atendiendo, y lleva las cuentas en un cuaderno y en la cabeza.

Lo que le duele, en sus palabras:

- **"No se si estoy ganando."** Vende todo el dia y al cerrar no sabe si el
  dinero que hay en la gaveta esta bien o le falta.
- **"Se me pierde la mercancia."** No sabe cuanto tiene de nada hasta que lo
  busca en el estante y no esta.
- **"No se a quien le fie."** Lo anota en un cuaderno que se moja, se pierde, o
  lo lleva alguien que ya no trabaja ahi.
- **"Me sube el proveedor y yo sigo vendiendo al mismo precio."** El costo sube
  y el precio se queda, y el margen se lo come la inflacion.
- **"Dos monedas."** Cobra en bolivares a la tasa del dia y piensa en dolares.

Lo que **no** es el publico: cadenas grandes, restaurantes con comandas,
comercios que necesitan facturacion fiscal homologada. Decirlo evita perder
tiempo de los dos lados.

## 3. Que tiene que lograr el sitio

En orden de importancia:

1. **Que deje sus datos.** Es la unica conversion que importa.
2. **Que entienda que le sirve.** Antes de dejar sus datos.
3. **Que sepa cuanto cuesta.** Es la pregunta que todo el mundo hace primero.
4. **Que confie.** Ver el sistema de verdad, no promesas.

## 4. Las secciones, y por que estan

| Seccion | Que hace | Por que |
|---|---|---|
| **Heroe** | Una frase que dice que es y para quien, y el boton de contacto | Un minuto para entender (principio II) |
| **El problema** | Las cinco frases de la seccion 2, en su voz | Se reconoce antes de que le vendan nada |
| **Como funciona** | Tres pasos: carga su catalogo, cobra, mira sus numeros | Quita el miedo a "esto es muy complicado para mi" |
| **Lo que hace** | Las funciones agrupadas por lo que resuelven, no por modulo | Nadie compra "modulo M7"; compra saber que tiene |
| **Verlo funcionando** | Capturas reales del sistema | Confianza. Y separa de quien solo tiene una pagina bonita |
| **Precios** | Los tres planes con sus limites y su precio | La pregunta mas frecuente, respondida sin pedir nada |
| **Preguntas** | Las seis que van a llegar igual por WhatsApp | Responderlas antes ahorra conversaciones y objeciones |
| **Contacto** | El formulario, corto | La conversion |
| **Pie** | Que es, quien lo hace, como escribir | Cierre y segunda oportunidad de contacto |

## 5. Requisitos funcionales

### Contenido

| ID | Requisito | Prio |
|---|---|---|
| RF-01 | Pagina unica, con las secciones de la seccion 4 y navegacion por anclas | M |
| RF-02 | Los planes y sus limites se muestran desde una sola declaracion, no repetidos por la pagina | M |
| RF-03 | Capturas reales del producto, con datos de ejemplo evidentes | M |
| RF-04 | Seccion de preguntas frecuentes, plegable | S |
| RF-05 | Pagina aparte de aviso de privacidad: que se guarda y para que | M |
| RF-06 | Pagina de gracias tras dejar los datos, que diga que sigue | M |

### Contacto

| ID | Requisito | Prio |
|---|---|---|
| RF-07 | Formulario corto: nombre, comercio, telefono, correo opcional, mensaje opcional | M |
| RF-08 | El contacto se guarda siempre, con su origen y desde que pagina llego | M |
| RF-09 | Enlace de WhatsApp armado con el mensaje ya escrito, para responder de una vez | M |
| RF-10 | Limite de tasa por origen en el envio | M |
| RF-11 | Trampa para robots que no moleste a una persona | S |
| RF-12 | Panel privado con los contactos, su estado y sus notas | M |
| RF-13 | Marcar un contacto como atendido, descartado o convertido | S |
| RF-14 | Exportar los contactos a CSV | C |

### Tecnicos

| ID | Requisito | Prio |
|---|---|---|
| RNF-01 | Menos de 150 KB de estilos y guiones comprimidos | M |
| RNF-02 | Ningun recurso servido desde otro dominio | M |
| RNF-03 | Operable y legible a 360 px | M |
| RNF-04 | Contraste AA y navegacion por teclado | M |
| RNF-05 | Datos estructurados y etiquetas para compartir en redes | S |
| RNF-06 | Mapa del sitio y `robots.txt` | S |
| RNF-07 | Sin rastreadores de terceros | M |
| RNF-08 | Los precios del sitio se comparan con los de Core Pos en una prueba | M |

## 6. Stack

El mismo de Core Pos, por el principio VI:

| Capa | Herramienta |
|---|---|
| Lenguaje | Python 3.13, gestionado con `uv` |
| Marco | Django 5.2 LTS |
| Base de datos | PostgreSQL 17 |
| Estilos | Tailwind CSS (binario, sin Node) |
| Interactividad | HTMX 2 y Alpine 3, servidos desde el propio sitio |
| Componentes | django-cotton |
| Calidad | Ruff, pytest, pre-commit, integracion continua |

## 7. Roadmap

| Fase | Contenido | Criterio de cierre |
|---|---|---|
| **F0 — Fundacion** | Repositorio, stack, calidad, integracion continua, constitucion | La suite vacia corre en CI y el sitio levanta |
| **F1 — La pagina** | Todas las secciones con su contenido real, responsive | Se lee entera en 360 px y pesa menos de 150 KB |
| **F2 — Captacion** | Formulario, guardado, WhatsApp, panel de contactos | Un contacto enviado aparece en el panel y genera su enlace |
| **F3 — Cierre** | Privacidad, buscadores, capturas, endurecimiento | Presupuesto de peso verificado y precios cuadrados con el producto |

## 8. Decisiones cerradas

| # | Decision | Consecuencia |
|---|---|---|
| D1 | **Formulario propio** con aviso por WhatsApp | El sitio necesita base de datos y panel |
| D2 | **Precios visibles**, con el plan de entrada gratis | Cambiarlos obliga a tocar una sola declaracion |
| D3 | La marca publica es **Core Pos** | El nombre vive en un solo sitio de configuracion |
| D4 | **Capturas reales, sin testimonios** | Habra seccion de testimonios cuando haya clientes que quieran aparecer |
| D5 | Proyecto y repositorio **separados de Core Pos** | El sitio se despliega y se cambia sin tocar el producto |

## 9. Lo que este sitio no hace

- No crea tiendas. Quien quiera abrir una lo hace en Core Pos; el sitio lo
  lleva hasta ahi.
- No cobra ni procesa pagos.
- No tiene blog ni gestor de contenido: el contenido vive en las plantillas y
  cambia con un commit.
- No tiene version en ingles en v1.
