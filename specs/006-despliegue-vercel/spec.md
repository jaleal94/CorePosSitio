# F6 — Despliegue en Vercel

**Rama**: `006-despliegue-vercel`
**Criterio de cierre**: el sitio arranca en Vercel con la seguridad de `prod.py` intacta, y lo que serverless rompe esta arreglado y probado.

---

## Por que esta fase

El sitio esta terminado y no esta en ninguna parte. Vercel le sirve —paginas,
un formulario, cero trabajos de fondo— pero serverless cambia dos supuestos que
el codigo daba por ciertos, y ninguno de los dos falla de forma visible.

**Los dos se descubrieron mirando el codigo, no desplegando.** Es la diferencia
entre encontrarlos ahora y encontrarlos con el sitio publicado.

---

## Lo que serverless rompe

### El limite del formulario deja de limitar

`sitio/views.py` limita el contacto a 10 envios por hora y por direccion, y
`django-ratelimit` lleva esa cuenta en la cache de Django. No hay `CACHES`
declarado, asi que esa cache es la memoria del proceso.

En Vercel casi cada peticion es un proceso nuevo: la cuenta empieza de cero cada
vez. **El limite no limita y sigue pareciendo que esta puesto**, que es peor que
no tenerlo.

No es solo de Vercel: con tres trabajadores en un servidor normal, el limite
permitia el triple de lo configurado. Estaba mal desde siempre y solo se veia
con varios procesos.

### La exportacion de contactos falla, y solo en produccion

En serverless hay que conectarse por el endpoint agrupado o las funciones agotan
las conexiones. Ese agrupador es PgBouncer en modo transaccion, y ahi **los
cursores de servidor no funcionan**: el cursor se declara en una transaccion y
la siguiente lectura puede caer en otra conexion donde no existe.

`sitio/views.py` exporta los contactos con `.iterator()`, que abre uno. Habria
fallado en produccion y en ningun otro sitio.

---

## Decisiones

| # | Decision |
|---|---|
| D-01 | `config/settings/vercel.py` hereda de `prod.py` y cambia solo lo que Vercel obliga. |
| D-02 | Los estaticos los sirve la red de Vercel; Django no los toca. |
| D-03 | Sin hash en el nombre de los estaticos, porque el manifiesto no llega a la funcion. |
| D-04 | La cache va a una tabla de Postgres, no a Redis. |
| D-05 | La construccion **no** corre migraciones. |
| D-06 | Pillow pasa a dependencia de desarrollo. |

### Por que sin hash en el nombre (D-03)

El almacenamiento que agrega el hash escribe un `staticfiles.json` durante la
construccion de los estaticos. La funcion de Python es **otra construccion** y
no lo tendria; sin ese archivo, cada `{% static %}` de cada plantilla revienta.

Se pierde poder cachear para siempre. A cambio va cache de una hora con
revalidacion, y en un sitio cuya primera carga son 33 KB eso no se nota.

### Por que la cache en Postgres y no en Redis (D-04)

Redis seria mas rapido y significaria otro servicio, otra cuenta y otra factura.
Son diez escrituras por hora y por visitante. La tabla ya esta en una base que
de todos modos hace falta.

### Por que la construccion no migra (D-05)

Se dispara en cada despliegue y puede haber dos a la vez. Una migracion a medias
por una construccion cancelada deja la base en un estado que nadie pidio. Se
corren a mano, una vez, y esta escrito en el README.

---

## Requisitos funcionales

| ID | Requisito |
|---|---|
| FR-01 | Punto de entrada WSGI que Vercel reconoce |
| FR-02 | Configuracion propia que hereda la seguridad de `prod.py` |
| FR-03 | Estaticos servidos por la red, con las rutas antes del comodin |
| FR-04 | Cache compartida, con su tabla creada por migracion |
| FR-05 | Cursores de servidor apagados |
| FR-06 | `requirements.txt` que no se separe de `pyproject.toml` |
| FR-07 | Las variables de produccion documentadas |
| FR-08 | Ni `.env` ni el binario de Tailwind suben al servidor |

---

## Fuera de alcance

- **Desplegar CoreAPP.** No va en Vercel y el porque esta dicho: el carrito vive
  en el servidor con presupuesto de 200 ms, hay dos comandos diarios, y las
  exportaciones no caben en el tiempo de una funcion.
- Un dominio propio. Se agrega despues, y obliga a repasar `ALLOWED_HOSTS` y
  `CSRF_TRUSTED_ORIGINS`.
- Respaldos. Los da quien provea Postgres, y hay que confirmarlos a mano.

---

## Criterio de cierre

El sitio arranca con `config.settings.vercel`, `check --deploy` pasa sin avisos,
y la suite completa en verde.
