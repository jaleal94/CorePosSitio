#!/usr/bin/env bash
# Lo que Vercel corre para dejar los archivos estaticos en su red.
#
# Solo recolecta estaticos. **No corre migraciones**, y eso es a proposito: la
# construccion se dispara en cada despliegue y puede haber dos a la vez. Una
# migracion a medias por una construccion cancelada deja la base en un estado
# que nadie pidio. Las migraciones se corren aparte, y esta en el README.
set -euo pipefail

ENTORNO=".venv-de-construccion"

echo "--- que hay en esta maquina"
command -v python3 >/dev/null || { echo "::error::No hay python3 en la maquina de construccion"; exit 1; }
python3 --version

# El Python de la maquina de construccion esta gestionado y protegido: instalar
# paquetes dentro da `externally-managed-environment` (PEP 668). No es un
# capricho de Vercel, es lo normal en las distribuciones modernas, y lo que esa
# norma espera es exactamente esto: un entorno propio, aparte.
echo "--- entorno virtual propio"
python3 -m venv "$ENTORNO"

# En Vercel -Linux- el interprete queda en bin/. En Windows queda en Scripts/.
# Se mira cual existe para poder probar este mismo guion antes de subirlo: cada
# despliegue fallido son diez minutos, y probarlo aqui cuesta uno.
if [ -x "$ENTORNO/bin/python" ]; then
  PY="$ENTORNO/bin/python"
else
  PY="$ENTORNO/Scripts/python.exe"
fi
"$PY" --version

# `collectstatic` no toca la base de datos ni firma nada: solo copia archivos.
# Pero los ajustes heredan de prod.py, que exige estas variables para arrancar.
# Se les da un valor de respaldo para que la construccion no dependa de si las
# variables del panel llegaron hasta aqui: lo que se recolecta es el mismo
# archivo con cualquiera de los dos valores.
export DJANGO_SETTINGS_MODULE="config.settings.vercel"
export DJANGO_DEBUG="${DJANGO_DEBUG:-False}"
export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS:-localhost}"
export DATABASE_URL="${DATABASE_URL:-postgres://nadie:nadie@localhost:5432/nada}"
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-clave-de-construccion-que-no-firma-nada-solo-copia-archivos}"

echo "--- instalando dependencias"
"$PY" -m pip install --disable-pip-version-check --quiet --upgrade pip
"$PY" -m pip install --disable-pip-version-check --quiet -r requirements.txt

echo "--- recolectando estaticos"
"$PY" manage.py collectstatic --noinput --clear

echo "--- listo"
echo "$(find estaticos_de_vercel -type f | wc -l) archivos en estaticos_de_vercel/static"
