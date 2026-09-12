# F3 — Cierre

**Rama**: `003-cierre`
**Criterio de cierre**: las capturas son del sistema de verdad, el sitio se comparte bien por WhatsApp, y sigue dentro del presupuesto de peso.

---

## Por que esta fase

Quedan tres huecos, y el primero es el que mas pesa.

**Las capturas.** La seccion "Asi se ve" dice "Captura pendiente" tres veces.
Es el unico sitio de la pagina donde hoy se le pide al lector que crea sin ver
nada, y el principio I dice que las capturas salen del sistema de verdad.

**Como se ve cuando lo comparten.** Este sitio se va a difundir por WhatsApp, de
un comerciante a otro. Sin las etiquetas correctas, el enlace aparece como una
direccion pelada y nadie lo abre.

**Que lo encuentren.** Sin mapa del sitio ni indicaciones para los buscadores, el
sitio existe solo para quien ya tiene el enlace.

---

## Historias de usuario

### US1 — Ver el sistema antes de creerle *(P1)*

Quien lee la pagina quiere ver que existe, no que se lo cuenten.

**Criterios de aceptacion**
1. Tres capturas del sistema de verdad: el cobro, el panel del dia y el
   inventario.
2. Con datos de ejemplo evidentes, de una bodega inventada, nunca de un comercio
   real.
3. La del cobro en proporcion de telefono, porque es donde se cobra.
4. Cada una con un pie que dice que se esta viendo.
5. Pesan poco: no pueden tumbar el presupuesto de la pagina.
6. Se generan con un guion reproducible, para poder rehacerlas cuando el sistema
   cambie de aspecto.

### US2 — Que el enlace se vea bien al compartirlo *(P2)*

Alguien manda el enlace por WhatsApp a un compadre que tiene un abasto.

**Criterios de aceptacion**
1. Al pegar el enlace aparece el nombre, una frase y una imagen.
2. La imagen tiene la proporcion que WhatsApp y las redes esperan.
3. La descripcion habla de lo mismo que la pagina, no de "software de gestion".
4. Funciona igual para la portada, la pagina de gracias y la de privacidad.

### US3 — Que los buscadores lo entiendan *(P3)*

**Criterios de aceptacion**
1. Mapa del sitio con las paginas publicas.
2. `robots.txt` que deja entrar a lo publico y cierra el panel.
3. El panel de contactos y la pagina de gracias no se indexan.
4. Datos estructurados que digan que es esto y cuanto cuesta.

### US4 — Que no se rompa feo *(P4)*

**Criterios de aceptacion**
1. Paginas propias de error 404 y 500, en el mismo lenguaje del sitio.
2. La de 404 ofrece volver y escribir.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | Guion reproducible que genera las capturas desde el sistema real |
| FR-02 | Las tres capturas en la pagina, con su pie |
| FR-03 | Imagenes optimizadas, sin tumbar el presupuesto |
| FR-04 | Etiquetas para compartir, en las tres paginas publicas |
| FR-05 | Imagen de portada para compartir, con la proporcion correcta |
| FR-06 | Mapa del sitio |
| FR-07 | `robots.txt` que cierra el panel |
| FR-08 | Datos estructurados con el producto y sus planes |
| FR-09 | Paginas de error 404 y 500 |
| FR-10 | Prueba: las capturas existen y estan enlazadas |
| FR-11 | Prueba: las etiquetas de compartir estan en cada pagina publica |
| FR-12 | Prueba: el presupuesto de peso se sigue cumpliendo con las imagenes |

---

## Decisiones de esta fase

| # | Decision |
|---|---|
| D-01 | Las capturas se generan con un guion que usa Core Pos **como biblioteca**: lee su codigo, corre con su entorno, y escribe en una base de datos aparte. No se modifica ni un archivo del producto. |
| D-02 | La base de la demostracion es propia (`coreapp_demo`) y se crea y se tira con el guion. La base de desarrollo del producto no se toca. |
| D-03 | Los datos de ejemplo son de una bodega inventada, con nombres que se reconocen como de ejemplo. |
| D-04 | Los datos estructurados van en linea con una marca de un solo uso, no relajando la politica de contenido. |

### Lo que D-01 significa

El guion vive en este repositorio, en `herramientas/`, y se ejecuta con el
entorno del producto:

```
uv run --project ..\CoreAPP python herramientas/capturas.py
```

Asi las capturas se pueden rehacer cuando el sistema cambie de aspecto, sin
tener que acordarse de como se hicieron. Una captura que no se puede rehacer
envejece hasta que miente.

### Por que D-04

Los datos estructurados se leen desde un bloque en linea. La politica de
contenido prohibe los guiones en linea, y relajarla para esto abriria justo la
puerta que cierra. La salida es una marca de un solo uso por respuesta, que
permite ese bloque y ningun otro.

---

## Fuera de alcance

- Medicion de visitas. Si alguna vez hace falta, sera con algo que corra en el
  propio servidor (principio X).
- Version en ingles.
- Blog o novedades.

---

## Criterio de cierre

Las tres capturas son del sistema de verdad y se ven en la pagina, el enlace se
comparte con imagen y descripcion, los buscadores tienen su mapa, y el peso
sigue por debajo de 150 KB.
