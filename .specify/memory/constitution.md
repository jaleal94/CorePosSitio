<!--
Version: 1.0.0
Ratificada: 2026-09-11
Proyecto: Core Pos — sitio de presentacion
-->

# Constitucion del sitio de Core Pos

Este sitio no es el producto: es lo que convence a alguien de probarlo. Tiene un
solo trabajo, y todo lo que sigue existe para protegerlo: que una comerciante
que nunca oyo hablar de esto entienda en un minuto si le sirve, y sepa como
pedirlo.

Los principios son innegociables. Una desviacion se escribe en el plan de la
fase, con su razon y su costo; no se decide en silencio dentro de un archivo.

## I. Nada que no sea cierto

No hay testimonios inventados, ni cifras de clientes que no existen, ni
capturas de pantalla de funciones que no estan construidas. Las capturas salen
del sistema de verdad, con datos de ejemplo evidentes.

Un sitio de presentacion vive de la confianza de quien lo lee, y esa confianza
se pierde una sola vez. Ademas, quien vende a bodegas de barrio vende por
recomendacion: una promesa incumplida vuelve.

**Regla practica:** si una afirmacion del sitio no se puede demostrar hoy en el
producto, no se escribe. Si describe algo que viene despues, se dice que viene
despues.

## II. Un minuto para entender

La primera pantalla dice que es, para quien es y que problema resuelve, en
lenguaje de comercio y sin una sola palabra tecnica. Ni "multi-tenant", ni
"kardex", ni "SaaS", ni "stack".

Quien llega no sabe lo que es un punto de venta en la nube; sabe que se le
pierde mercancia y que no cuadra la caja.

## III. El contacto nunca se pierde

Cada persona que deja sus datos queda guardada, con lo que escribio y desde
donde llego. El aviso puede fallar, el correo puede rebotar, WhatsApp puede
estar caido: el registro en la base es lo que no puede faltar.

Un contacto perdido es un cliente perdido, y no hay forma de enterarse.

## IV. Carga rapida con conexion mala

Presupuesto duro: **menos de 150 KB** de estilos y guiones comprimidos, y nada
que venga de otro servidor. Sin tipografias externas, sin bibliotecas de
terceros por red, sin rastreadores de nadie.

El publico abre esto con datos moviles, en un telefono barato, en un pais con
conexion intermitente. Un sitio que tarda es un sitio que nadie ve.

## V. Se lee en un telefono

Todo se diseña primero para 360 px de ancho. El sitio se mira mayormente desde
el telefono, muchas veces mientras se atiende el mostrador.

## VI. Mismo stack que el producto

Django, PostgreSQL, Tailwind, HTMX y Alpine, con `uv` y Ruff, igual que Core
Pos. No se introduce una tecnologia distinta para ahorrar una tarde: quien
mantenga esto es quien mantiene el producto, y dos mundos distintos se traducen
en uno de los dos abandonado.

## VII. Lo que se dice se prueba

Cada afirmacion verificable del sitio —los precios, los limites de los planes,
las funciones que se listan— tiene una prueba automatica que la compara contra
lo que Core Pos hace de verdad. Cuando el producto cambie, el sitio falla la
suite antes de mentir.

## VIII. Se cierra en verde

Cada fase termina con la suite en verde, commit y etiqueta anotada. Nunca se
etiqueta algo que no pasa sus pruebas.

## IX. Espanol de Venezuela

Los textos hablan como habla el publico: bodega, abasto, fiado, cuadrar la
caja, mercancia. Las cifras, fechas y monedas en formato local.

## X. Nada de datos de nadie

El sitio no instala rastreadores de terceros ni comparte los contactos con
ningun servicio externo. Si algun dia hace falta medir visitas, se mide con
algo que corra en el propio servidor.

Quien deja su telefono espera que lo llame el negocio, no que su dato circule.

---

## Gobierno

Cambiar un principio exige una version nueva de este documento y una nota que
diga que cambio y por que.

**Version**: 1.0.0 · **Ratificada**: 2026-09-11
