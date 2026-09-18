# Tasks: F6 — Despliegue en Vercel

**Input**: `specs/006-despliegue-vercel/` (spec.md)

---

## Fase 1 · Lo que Vercel necesita

- [x] **T001** `api/index.py`, el punto de entrada WSGI
- [x] **T002** `vercel.json`, con los estaticos antes del comodin
- [x] **T003** `build_files.sh`, que recolecta y no migra
- [x] **T004** `requirements.txt`, que Vercel si entiende
- [x] **T005** `.vercelignore`

## Fase 2 · Lo que serverless rompe

- [x] **T006** `config/settings/vercel.py`, heredando de `prod.py`
- [x] **T007** Cache compartida en `prod.py`, y su tabla por migracion
- [x] **T008** Cursores de servidor apagados
- [x] **T009** Pillow a dependencia de desarrollo

## Fase 3 · Que no se desarme

- [x] **T010** Pruebas de despliegue
- [x] **T011** CI: comprobar los settings de Vercel y que requirements no envejezca
- [x] **T012** `.env.produccion.example` y el README
- [x] **T013** Cerrar la fase: fusionar a `main` y etiquetar `v1.3.0`

---

## Estado

**200 pruebas en verde.** 8 nuevas, todas de despliegue.

### Los dos fallos que aparecieron antes de desplegar

**El limite del formulario no limitaba.** La cache era la memoria del proceso.
Con varios procesos —o con Vercel, donde casi cada peticion es uno nuevo— cada
uno llevaba su propia cuenta. Estaba mal desde siempre y solo se ve con mas de
un trabajador. Ahora vive en una tabla de Postgres.

**La exportacion de contactos habria fallado solo en produccion.** Usa
`.iterator()`, que abre un cursor de servidor, y el agrupador que hay que usar
en serverless es PgBouncer en modo transaccion, donde esos cursores no
sobreviven. Apagados, con prueba que ademas comprueba que `.iterator()` sigue
ahi: el dia que nadie lo use, la prueba avisa de que el ajuste puede revisarse.

### Lo que me equivoque por el camino

La primera version de la prueba de los cursores **importaba**
`config.settings.vercel`, que arrastra `prod.py`, que se niega a cargarse sin
las variables de produccion. Hace bien en negarse: lo que estaba mal era la
prueba. Se comitio fallando y se corrigio en el commit siguiente.

### Lo que queda en manos de otro

**Los respaldos.** Los hace quien provea la base; hay que confirmar la
retencion y **probar una restauracion**. Un respaldo que nunca se restauro no es un respaldo, y esto
sigue sin poder comprobarlo ninguna prueba.

**La version de Python.** El proyecto pide 3.13. Si Vercel solo ofreciera 3.12,
el sitio funcionaria igual —no usa nada exclusivo de 3.13— pero habria que
aflojar `requires-python`.
