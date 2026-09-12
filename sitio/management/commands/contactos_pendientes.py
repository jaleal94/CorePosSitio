"""Los contactos que faltan por atender.

Existe por la decision D-02: no hay aviso automatico, porque empujar un mensaje
exigiria un servicio externo y por ahi pasarian los datos de quien escribe.

La mitigacion es esto: un comando que se puede programar para que los pendientes
aparezcan donde a usted le quede comodo mirarlos.

    uv run python manage.py contactos_pendientes
"""

from django.core.management.base import BaseCommand

from sitio.servicios import enlace_de_whatsapp, sin_atender


class Command(BaseCommand):
    help = "Lista los contactos que todavia nadie atendio."

    def add_arguments(self, parser):
        parser.add_argument(
            "--enlaces",
            action="store_true",
            help="Muestra tambien el enlace de WhatsApp de cada uno.",
        )

    def handle(self, *args, **opciones):
        pendientes = list(sin_atender().order_by("creado_en"))

        if not pendientes:
            self.stdout.write(self.style.SUCCESS("No hay contactos sin atender."))
            return

        self.stdout.write(
            self.style.WARNING(
                f"{len(pendientes)} contacto{'s' if len(pendientes) != 1 else ''} sin atender:"
            )
        )
        for contacto in pendientes:
            self.stdout.write(
                f"  {contacto.creado_en:%d/%m %H:%M}  {contacto.nombre} "
                f"({contacto.comercio})  {contacto.telefono_legible}"
            )
            if contacto.mensaje:
                self.stdout.write(f'      "{contacto.mensaje[:70]}"')
            if opciones["enlaces"]:
                self.stdout.write(f"      {enlace_de_whatsapp(contacto)}")
