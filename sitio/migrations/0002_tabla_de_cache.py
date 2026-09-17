"""La tabla donde vive la cache en produccion.

Se crea en una migracion y no a mano porque es un paso que se olvida. Y cuando
se olvida no falla el despliegue: falla el formulario de contacto la primera vez
que alguien lo envia, que es lo unico que este sitio tiene que conseguir.

`createcachetable` no hace nada si la tabla ya existe, asi que correr las
migraciones dos veces es seguro.
"""

from django.core.management import call_command
from django.db import migrations

TABLA = "cache_del_sitio"


def crear(apps, schema_editor):
    call_command("createcachetable", TABLA, database=schema_editor.connection.alias)


def borrar(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS "{TABLA}"')


class Migration(migrations.Migration):
    dependencies = [("sitio", "0001_initial")]

    operations = [migrations.RunPython(crear, borrar)]
