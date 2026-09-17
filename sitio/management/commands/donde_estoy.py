"""Dice a que base de datos apunta esta configuracion, antes de tocarla.

Existe por un accidente concreto y facil: el `.env` de desarrollo apunta a la
base local, y las variables del entorno le ganan. Si se corre `migrate` contra
produccion y se olvida una variable, el comando **no falla**: migra la base
local y dice que todo salio bien.

Este se corre antes y muestra a donde va. Nunca imprime la clave: un comando que
la muestra acaba con la clave pegada en una captura de pantalla.
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "Muestra a que base de datos apunta la configuracion actual"

    def handle(self, *args, **opciones):
        datos = settings.DATABASES["default"]
        self.stdout.write(f"  configuracion  {settings.SETTINGS_MODULE}")
        self.stdout.write(f"  servidor       {datos.get('HOST') or '(local)'}")
        self.stdout.write(f"  base           {datos.get('NAME')}")
        self.stdout.write(f"  usuario        {datos.get('USER')}")

        servidor = (datos.get("HOST") or "").lower()
        if servidor in ("", "localhost", "127.0.0.1"):
            self.stdout.write(self.style.WARNING("\n  Es su base LOCAL, no la de produccion."))
        elif "-pooler" not in servidor:
            self.stdout.write(
                self.style.WARNING(
                    "\n  Es una base remota, pero NO por el endpoint agrupado.\n"
                    "  Para Vercel hace falta el que lleva '-pooler' en el nombre."
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("\n  Base remota, por el endpoint agrupado."))

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT current_database(), version()")
                base, version = cursor.fetchone()
            self.stdout.write(f"\n  Conecto bien a '{base}'.")
            self.stdout.write(f"  {version.split(',')[0]}")
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"\n  No se pudo conectar: {error}"))
