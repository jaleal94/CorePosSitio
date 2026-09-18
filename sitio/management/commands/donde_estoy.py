"""Dice a que base de datos apunta esta configuracion, antes de tocarla.

Existe por un accidente concreto y facil: el `.env` de desarrollo apunta a la
base local, y las variables del entorno le ganan. Si se corre `migrate` contra
produccion y se olvida una variable, el comando **no falla**: migra la base
local y dice que todo salio bien.

Este se corre antes y muestra a donde va. Nunca imprime la clave: un comando que
la muestra acaba con la clave pegada en una captura de pantalla.

No sabe de proveedores. Lo que comprueba es la forma de la conexion -si el
servidor es local, si va por un agrupador, y por que puerto-, que es lo que
importa y lo unico que sigue siendo cierto el dia que se cambie de proveedor.
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

# El puerto que bloquean muchos proveedores de internet. No es un problema del
# codigo, pero si el motivo de media hora de confusion cuando pasa, asi que
# conviene que el comando lo nombre.
PUERTO_QUE_SUELEN_BLOQUEAR = 5432

LOCALES = {"", "localhost", "127.0.0.1", "::1"}


class Command(BaseCommand):
    help = "Muestra a que base de datos apunta la configuracion actual"

    def handle(self, *args, **opciones):
        datos = settings.DATABASES["default"]
        servidor = str(datos.get("HOST") or "").lower()
        puerto = datos.get("PORT") or PUERTO_QUE_SUELEN_BLOQUEAR

        self.stdout.write(f"  configuracion  {settings.SETTINGS_MODULE}")
        self.stdout.write(f"  servidor       {servidor or '(local)'}")
        self.stdout.write(f"  puerto         {puerto}")
        self.stdout.write(f"  base           {datos.get('NAME')}")
        self.stdout.write(f"  usuario        {datos.get('USER')}")

        if servidor in LOCALES:
            self.stdout.write(self.style.WARNING("\n  Es su base LOCAL, no la de produccion."))
        elif "pooler" in servidor or "pgbouncer" in servidor:
            self.stdout.write(self.style.SUCCESS("\n  Base remota, por un agrupador."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "\n  Base remota, pero NO parece ir por un agrupador.\n"
                    "  En Vercel cada peticion abre su propia conexion: sin agrupador\n"
                    "  se agotan las de la base."
                )
            )

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT current_database(), version()")
                base, version = cursor.fetchone()
            self.stdout.write(f"\n  Conecto bien a '{base}'.")
            self.stdout.write(f"  {version.split(',')[0]}")
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"\n  No se pudo conectar: {error}"))
            if servidor not in LOCALES and int(puerto) == PUERTO_QUE_SUELEN_BLOQUEAR:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n  Va por el puerto {PUERTO_QUE_SUELEN_BLOQUEAR}, que bastantes\n"
                        "  proveedores de internet bloquean. Si su proveedor ofrece otro\n"
                        "  puerto para el agrupador, uselo. Compruebelo con:\n"
                        f"    Test-NetConnection {servidor} -Port {puerto}"
                    )
                )
