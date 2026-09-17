#!/usr/bin/env bash
# Lo que Vercel corre para dejar los archivos estaticos en su red.
#
# Solo recolecta estaticos. **No corre migraciones**, y eso es a proposito: la
# construccion se dispara en cada despliegue y puede haber dos a la vez. Una
# migracion a medias por una construccion cancelada deja la base en un estado
# que nadie pidio. Las migraciones se corren a mano, una vez, desde su maquina
# contra la base de produccion. Esta en el README.
set -euo pipefail

python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet -r requirements.txt

python3 manage.py collectstatic --noinput --clear --settings=config.settings.vercel

echo "Estaticos recolectados en estaticos_de_vercel/static"
