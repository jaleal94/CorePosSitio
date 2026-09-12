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
| F1 | La pagina: todas las secciones con su contenido real | pendiente |
| F2 | Captacion: formulario, panel de contactos y WhatsApp | pendiente |
| F3 | Cierre: privacidad, buscadores, capturas, endurecimiento | pendiente |

### Lo que garantiza la suite

- **Nada viene de afuera**: la politica de contenido no admite recursos de otro
  servidor, ni guiones en linea, ni rastreadores de terceros.
- **La marca vive en un solo sitio**: cambiarla es cambiar una linea.
- **La hoja de estilos esta compilada**: si falta, la suite lo dice antes de que
  se note en produccion.

## Comprobaciones

```bash
uv run ruff check . && uv run ruff format --check .
uv run pytest
```
