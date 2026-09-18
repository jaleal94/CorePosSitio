# Sitio de Core Pos

El sitio publico de **Core Pos**, el punto de venta y control de inventario
para bodegas, abastos y comercios pequeños.

No es el producto: es lo que hace que alguien decida probarlo, y lo que recoge
sus datos para poder llamarlo. El producto vive en un repositorio aparte.

## Como levantarlo

Hace falta Python 3.13 con [uv](https://docs.astral.sh/uv/) y un PostgreSQL 17
corriendo.

```bash
cp .env.example .env          # y ajustar la clave de PostgreSQL
createdb -U postgres coreposweb

uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Queda en `http://127.0.0.1:8000/`.

Para trabajar los estilos, con recompilado automatico en otra terminal:

```bash
./tailwindcss.exe -i assets/tailwind.css -o static/css/sitio.css --watch
```

La hoja compilada se versiona a proposito, para que clonar y arrancar funcione
sin compilar nada. La integracion continua la recompila y falla si quedo vieja.

## Como cambiar lo que dice

- **El nombre, el telefono y el correo**: `MARCA`, en `config/settings/base.py`,
  alimentado por el `.env`. Un solo sitio (decision D3).
- **Los textos de las secciones**: las plantillas en `templates/sitio/`.
- **Los planes y sus precios**: una sola declaracion, que una prueba compara
  contra lo que Core Pos cobra de verdad (principio VII).

## Metodologia

Desarrollo guiado por especificacion, con
[Spec Kit](https://github.com/github/spec-kit), igual que el producto:
constitucion, especificacion, plan, tareas, implementacion.

- La constitucion esta en [.specify/memory/constitution.md](.specify/memory/constitution.md)
  y sus diez principios son innegociables.
- El PRD esta en [docs/PRD.md](docs/PRD.md).
- Cada fase tiene su carpeta en [specs/](specs/) y cierra con la suite en verde,
  commit y etiqueta anotada.

## Estado

| Fase | Contenido | Etiqueta |
|---|---|---|
| F0 | Fundacion: stack, calidad, integracion continua, Spec Kit | `v0.1.0-f0` |
| F1 | La pagina: todas las secciones con su contenido real | `v0.2.0-f1` |
| F2 | Captacion: formulario, panel de contactos y WhatsApp | `v0.3.0-f2` |
| F3 | Cierre: capturas reales, compartir, buscadores y errores | `v1.0.0` |
| F4 | Identidad visual: el logo, la paleta de la marca y los campos | `v1.1.0` |
| F5 | Plan unico: 19,99 $ al mes mas 60 $ de instalacion | `v1.2.0` |

### Lo que garantiza la suite

- **Nada viene de afuera**: la politica de contenido no admite recursos de otro
  servidor, ni guiones en linea, ni rastreadores de terceros.
- **La marca vive en un solo sitio**: cambiarla es cambiar una linea.
- **La hoja de estilos esta compilada**: si falta, la suite lo dice antes de que
  se note en produccion.
- **Se habla en lenguaje de comercio**: una prueba recorre la pagina y falla si
  aparece una palabra de programador. La lista esta en `tests/test_contenido.py`.
- **Los precios cuadran con el producto**: los dos -la mensualidad y la
  instalacion- se comparan contra la declaracion de Core Pos, y ninguno puede
  estar escrito a mano en la plantilla.
- **El sitio no promete nada que dejo de ser cierto**: una prueba pide cada
  pagina publica y falla si vuelve a aparecer "gratis", "sin tarjeta" o "sin
  compromiso". Tambien mira la imagen que se ve al compartir, donde la promesa
  serian pixeles que ninguna busqueda de texto encuentra.
- **La primera carga cabe en 150 KB** comprimidos. Hoy pesa 12 KB.
- **Se dice lo que el producto no hace**, y hay una prueba que lo exige.
- **Ningun contacto se pierde**: se guarda antes que nada, y un reenvio del mismo
  telefono actualiza en vez de duplicar, sin pisar el trabajo del operador.
- **Los robots no pasan**: trampa invisible y limite por origen, con una
  respuesta que dice "espere", no "no tiene permiso".
- **El panel no se ve sin sesion**, ni la exportacion.
- **Las capturas son del sistema real** y existen: si falta una, la suite lo dice.
- **Los datos estructurados salen de la misma declaracion** que los precios de
  la pagina, asi que el buscador nunca anuncia un precio viejo.
- **Ningun comentario de plantilla llega al navegador**: `{# #}` en Django es de
  una sola linea y no avisa cuando no lo es.
- **El peso aguanta con las imagenes dentro**: 33 KB la primera carga, 75 KB si
  se baja la pagina entera.
- **El contraste se calcula, no se estima**: cada par de texto y fondo que el
  sitio pinta llega al minimo de la norma, y la prueba falla nombrando el par y
  su cifra.
- **La paleta es la misma que la del producto**, leida de su propia hoja de
  estilos y no de una copia.
- **El logo es el mismo archivo**, byte a byte: hay una sola copia del original,
  y vive en Core Pos.

## Despliegue en Vercel

Los archivos estan en el repositorio: `vercel.json`, `api/index.py`,
`build_files.sh`, `requirements.txt` y `config/settings/vercel.py`. Las
variables que hay que cargar en el panel estan en `.env.produccion.example`.

Dos cosas que Vercel obliga a hacer distinto, por si alguien las toca:

**Los estaticos no los sirve Django.** Los sirve la red de Vercel, desde lo que
`build_files.sh` deja al construir. Por eso `config/settings/vercel.py` usa un
almacenamiento sin hash en el nombre: el que lo agrega escribe un
`staticfiles.json` durante la construccion de los estaticos, y la funcion de
Python es otra construccion que no lo tendria. Sin ese archivo, cada
`{% static %}` revienta.

**El limite del formulario necesita una cache compartida.** `django-ratelimit`
lleva la cuenta en la cache de Django, y sin declarar ninguna esa cache es la
memoria del proceso. En Vercel casi cada peticion es un proceso nuevo: el
limite deja de limitar y no avisa. `prod.py` declara la cache en la tabla
`cache_del_sitio`, que crea la migracion `sitio/0002`.

**Las migraciones no corren solas.** `build_files.sh` no las ejecuta a
proposito: la construccion se dispara en cada despliegue y puede haber dos a la
vez. Se corren una vez, desde su maquina, contra la base de produccion.

Antes de migrar, **compruebe a donde apunta**. El `.env` de desarrollo apunta a
la base local y las variables del entorno le ganan: si falta una, `migrate` no
falla, migra la base local y dice que todo salio bien.

```powershell
uv run python manage.py donde_estoy --settings=config.settings.vercel
uv run python manage.py migrate      --settings=config.settings.vercel
```

### El puerto importa

**Bastantes proveedores de internet bloquean el puerto 5432.** El sintoma es
`server closed the connection unexpectedly`, que parece un fallo del servidor y
es de la red. Se comprueba asi:

```powershell
Test-NetConnection SU-ANFITRION -Port 5432
```

Por eso la cadena de produccion es la del **agrupador en modo transaccion**, que
escucha en otro puerto: en Supabase el 6543. Eso resuelve las dos cosas a la
vez -las conexiones en serverless y poder migrar desde una maquina cualquiera-.

`donde_estoy` avisa si la conexion va por el 5432 y no responde.

### Si aun asi no se puede desde aqui

Esta el flujo **Migrar produccion** en GitHub Actions
(`.github/workflows/migrar.yml`). Se dispara a mano desde la pestaña Actions,
corre desde la red de GitHub, y la clave vive en los secretos del repositorio en
vez de en la maquina de nadie. Pide escribir "migrar" para confirmar, dice a que
base apunta y muestra el plan antes de aplicarlo.

Secretos que necesita: `DATABASE_URL`, `DJANGO_SECRET_KEY`, y para crear el
usuario del panel `PANEL_USUARIO`, `PANEL_CORREO` y `PANEL_CLAVE`.

Al agregar una dependencia hay que regenerar la lista que lee Vercel, porque no
entiende `uv`:

```bash
uv export --no-dev --no-hashes --no-annotate --no-header     --format requirements-txt > requirements.txt
```

Hay una prueba que falla si se olvida.

## El precio

Hay **un solo plan**: 19,99 $ al mes, mas 60 $ una sola vez por la instalacion.
Los dos numeros salen de `sitio/planes.py`, y una prueba los compara con los que
declara Core Pos en `apps/plataforma/planes.py`. Ninguno puede escribirse a mano
en la plantilla.

El sitio **capta**; no cobra. No hay pasarela de pago: quien llega deja sus
datos o pide su tienda, y el cobro se acuerda por fuera antes de aprobarla.

## La marca

El logo y los colores salen de un solo archivo: `assets/marca/logo.png` en Core
Pos. Ni el sitio ni el producto tienen una segunda copia, porque el dia que
alguien reemplace una se quedaria la otra y los dos se verian de dos empresas
parecidas.

Para rehacer los archivos del logo, con el producto al lado:

```bash
uv run python herramientas/marca.py
./tailwindcss.exe -i assets/tailwind.css -o static/css/sitio.css --minify
```

El azul marino `#274166` lleva la accion. El verde `#58AB9B` se queda en el
logo: da 2,72:1 sobre blanco, y en el producto el verde ya significa que la caja
cuadro. Por eso `--color-marca-verde` y `--color-sana` son dos nombres
distintos, y hay prueba de que no se confunden.

## Las capturas

Las tres capturas de la seccion "Asi se ve" salen del sistema de verdad, con una
bodega de ejemplo. Se regeneran cuando el sistema cambie de aspecto:

```bash
uv run --project ..\CoreAPP python herramientas/capturas.py
uv run python herramientas/imagen_de_compartir.py
```

El guion usa Core Pos **como biblioteca**: lee su codigo, corre con su entorno,
crea una base de datos aparte que despues borra, y no modifica ni un archivo del
producto. Hace falta Edge o Chrome, solo para generar; no para servir el sitio.

## El panel de contactos

Los contactos que llegan por el formulario se ven en `/contactos/`, y hace falta
una cuenta del personal:

```bash
uv run python manage.py createsuperuser
```

Cada contacto trae su enlace de WhatsApp con el mensaje ya escrito, que lo llama
por su nombre y menciona su comercio.

**No hay aviso automatico cuando llega uno** (decision D-02): empujar un mensaje
exigiria contratar un servicio externo, y por ahi pasarian los datos de quien
escribe, que es justo lo que el principio X prohibe. Para no depender de
acordarse de mirar el panel:

```bash
uv run python manage.py contactos_pendientes --enlaces
```

Ese comando se puede programar para que los pendientes aparezcan donde le quede
comodo verlos.

## Comprobaciones

```bash
uv run ruff check . && uv run ruff format --check .
uv run pytest
```
