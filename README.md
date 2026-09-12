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
| F3 | Cierre: privacidad, buscadores, capturas, endurecimiento | pendiente |

### Lo que garantiza la suite

- **Nada viene de afuera**: la politica de contenido no admite recursos de otro
  servidor, ni guiones en linea, ni rastreadores de terceros.
- **La marca vive en un solo sitio**: cambiarla es cambiar una linea.
- **La hoja de estilos esta compilada**: si falta, la suite lo dice antes de que
  se note en produccion.
- **Se habla en lenguaje de comercio**: una prueba recorre la pagina y falla si
  aparece una palabra de programador. La lista esta en `tests/test_contenido.py`.
- **Los precios cuadran con el producto**: se comparan contra la declaracion de
  Core Pos, y ningun numero puede estar escrito a mano en la plantilla.
- **La primera carga cabe en 150 KB** comprimidos. Hoy pesa 12 KB.
- **Se dice lo que el producto no hace**, y hay una prueba que lo exige.
- **Ningun contacto se pierde**: se guarda antes que nada, y un reenvio del mismo
  telefono actualiza en vez de duplicar, sin pisar el trabajo del operador.
- **Los robots no pasan**: trampa invisible y limite por origen, con una
  respuesta que dice "espere", no "no tiene permiso".
- **El panel no se ve sin sesion**, ni la exportacion.

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
