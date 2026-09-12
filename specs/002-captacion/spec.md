# F2 — Captacion

**Rama**: `002-captacion`
**Criterio de cierre**: un contacto enviado desde el telefono aparece en el panel y trae su enlace de WhatsApp listo para responder.

---

## Por que esta fase

F1 dejo una pagina que convence y termina en un boton que no hace nada. Esta le
pone el destino.

Es la fase que decide si el sitio sirve o es decoracion: **la unica conversion
que importa es que alguien deje sus datos**. Todo lo demas —lo bonito, lo
rapido, lo bien escrito— existe para llegar hasta aqui.

Y el principio III manda sobre todo lo que sigue: un contacto perdido es un
cliente perdido, y no hay forma de enterarse de que se perdio.

---

## Historias de usuario

### US1 — Dejar mis datos en treinta segundos *(P1)*

Una comerciante convencida llega al final de la pagina, en su telefono. Escribe
lo minimo y manda.

**Criterios de aceptacion**
1. Cuatro campos visibles: como se llama, como se llama su comercio, su
   telefono, y si quiere, un mensaje. El correo es opcional.
2. Se llena con una mano, con el teclado correcto en cada campo: el numerico
   para el telefono, el de correo para el correo.
3. Si algo falta, se dice en el campo, en lenguaje comun, sin perder lo escrito.
4. Al enviarlo, ve una pagina que le dice que sigue y en cuanto tiempo.
5. Desde esa pagina puede escribir por WhatsApp de una vez si no quiere esperar.

### US2 — Que no se pierda ninguno *(P2)*

**Criterios de aceptacion**
1. El contacto se guarda **siempre** que el formulario sea valido.
2. Queda registrado desde que seccion de la pagina pulso el boton, y desde que
   direccion llego.
3. Si la misma persona manda dos veces seguidas lo mismo, no se crean dos: se
   actualiza el mensaje del que ya estaba.
4. Nada de lo que pase despues de guardar —armar un enlace, registrar algo—
   puede hacer que el contacto se pierda.

### US3 — Que no lo llenen los robots *(P3)*

Un formulario publico sin defensa se llena de basura en una semana, y entre la
basura se pierden los buenos.

**Criterios de aceptacion**
1. Trampa para robots que no le pide nada a una persona ni molesta a un lector
   de pantalla.
2. Limite de envios por origen.
3. Un envio bloqueado responde que espere, no que no tiene permiso.

### US4 — Responderle el mismo dia *(P4)*

El operador abre el panel, ve quien escribio, y le responde por WhatsApp con un
toque.

**Criterios de aceptacion**
1. Panel privado, solo para el personal.
2. Los nuevos primero, con lo que escribieron a la vista.
3. Cada contacto trae su enlace de WhatsApp con el mensaje ya escrito, que lo
   llama por su nombre y menciona su comercio.
4. Se marca como atendido, descartado o convertido, y se le pueden poner notas.
5. Se ve cuantos hay sin atender, sin tener que contarlos.

### US5 — Llevarse la lista *(P5)*

**Criterios de aceptacion**
1. Descarga de todos los contactos en CSV, abrible en Excel.
2. La descarga es solo para el personal.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | Modelo `Contacto` con su estado, su origen y sus notas |
| FR-02 | Formulario en la seccion de contacto de la portada |
| FR-03 | Guardado atomico; lo que venga despues no puede tumbarlo |
| FR-04 | Registro de desde que seccion y desde que direccion llego |
| FR-05 | Un reenvio del mismo telefono actualiza, no duplica |
| FR-06 | Trampa para robots, invisible y sin molestar a nadie |
| FR-07 | Limite de tasa por origen, con respuesta que explica |
| FR-08 | Pagina de gracias que dice que sigue y ofrece WhatsApp |
| FR-09 | Panel privado con los contactos y su estado |
| FR-10 | Enlace de WhatsApp por contacto, con el mensaje escrito |
| FR-11 | Cambio de estado y notas desde el panel |
| FR-12 | Exportacion a CSV |
| FR-13 | Aviso de privacidad enlazado desde el formulario |

---

## Decisiones de esta fase

| # | Decision |
|---|---|
| D-01 | El telefono es la llave: es lo que de verdad identifica a un comercio aqui, y el correo muchas veces no existe o no se revisa. |
| D-02 | No hay aviso automatico a WhatsApp. El panel muestra los pendientes y arma el enlace; empujar un mensaje exigiria un servicio externo, que la constitucion descarta (principio X). |
| D-03 | El panel se protege con las cuentas de Django, no con una propia. Es para una o dos personas. |

### Lo que D-02 significa en la practica

Nadie recibe una notificacion cuando llega un contacto. Hay que abrir el panel.

Se acepta porque la alternativa —contratar un servicio que mande mensajes—
significa que los datos de quien escribe pasan por un tercero, y eso es
exactamente lo que el principio X prohibe.

Mitigacion: un comando `contactos_pendientes` que imprime los que faltan por
atender, para poder programarlo y verlo donde sea comodo.

---

## Fuera de alcance

- Aviso automatico por correo o WhatsApp (D-02).
- Seguimiento de conversaciones dentro del panel: se responde en WhatsApp.
- Formularios distintos por plan: uno solo, y el interes se anota si lo dice.

---

## Criterio de cierre

Un contacto enviado desde el formulario aparece en el panel con su enlace de
WhatsApp, un reenvio no lo duplica, un robot no pasa, y la suite queda verde.
