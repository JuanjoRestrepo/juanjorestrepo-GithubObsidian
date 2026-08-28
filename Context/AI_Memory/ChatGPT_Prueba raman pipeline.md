---
title: "Prueba raman pipeline"
date: 1755225456.810073
tags: [ai_memory, claude_context]
summary: ""
---

### Assistant
Buena pregunta — con los resultados que mostraste, **mi recomendación es sí**: modifica el DAG para que registre explícita y consistentemente `rows_inserted`, `rows_updated`, `rows_attempted` y si la ejecución fue `force` (en la tarea de prueba). Justificación breve:

- `rows_inserted` por sí solo no cuenta la historia (a menudo será 0 si solo hubo actualizaciones). `rows_updated` muestra cambios reales realizados por reprocesos (`force=True`) y es crítico para auditoría y para decidir si los parámetros de detección están funcionando.
- Tener ese resumen en los logs y en un pequeño XCom (resumen) permite analizar ejecuciones sin inflar la DB de metadatos de Airflow.
- Mostrar `forced` en logs ayuda a distinguir ejecuciones de prueba vs producción en los historiales.

A continuación te doy **el cambio inmediato y seguro**: reemplaza las dos funciones `peaks_task` y `peaks_test_task` en tu `Airflow/Dags/raman_pipeline.py` por las versiones siguientes. Estas:

- Llamarán a `save_peaks_to_db` como antes.
- Loguearán los campos `rows_inserted`, `rows_updated`, `rows_attempted`, `status` y `force`.
- Retornarán solo un **resumen** por archivo (lista de dicts pequeños) para XCom (evitamos devolver objetos grandes).
- Continuarán provocando fallo (raise) si `status` no es `success` — comportamiento actual.

Copia/pega estas dos funciones en el DAG (reemplazando las originales):

```python
def peaks_task(**_):
    """
    Tarea de producción: procesa todos los json del folder cleaned sin force.
    Retorna lista de resúmenes pequeños para XCom.
    """
    silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
    summaries = []
    for js in sorted(glob.glob(f"{silver_dir}/*.json")):
        # Llamada de producción (no force)
        res = save_peaks_to_db(js, tolerance=15, prominence=10)
        # Construir resumen pequeño
        summary = {
            "file": res.get("file"),
            "status": res.get("status"),
            "rows_attempted": int(res.get("rows_attempted", 0)),
            "rows_inserted": int(res.get("rows_inserted", 0)),
            "rows_updated": int(res.get("rows_updated", 0)),
            "error": res.get("error")
        }
        # Log claro y uniforme
        if summary["status"] == "success":
            logger.info(f"[PROD] {summary['file']} → inserted={summary['rows_inserted']} updated={summary['rows_updated']} attempted={summary['rows_attempted']}")
        elif summary["status"] == "no_peaks":
            logger.info(f"[PROD] {summary['file']} → no_peaks (attempted={summary['rows_attempted']})")
        else:
            logger.error(f"[PROD] {summary['file']} → status={summary['status']} error={summary['error']}")
            # Registrar y forzar retry si status=failed u otro
            log_error(f"save_peaks failed for {js}: {summary['error'] or summary['status']}")
            raise RuntimeError(f"save_peaks failed for {js}: {summary['error'] or summary['status']}")
        summaries.append(summary)
    # Para evitar XCom gigantes, devolvemos sólo el resumen
    return summaries


def peaks_test_task(max_files: int = TEST_MAX_FILES, **_):
    """
    Tarea de prueba (FORCE=True) — procesa hasta max_files y registra rows_updated.
    Retorna lista de resúmenes pequeños para XCom.
    """
    silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
    files = sorted(glob.glob(f"{silver_dir}/*.json"))
    if not files:
        logger.warning("[TEST FORCE] No hay archivos .json en silver_dir para la prueba.")
        return []

    files_to_run = files[:max_files]
    logger.info(f"[TEST FORCE] Procesando {len(files_to_run)} archivo(s) (max_files={max_files})")

    summaries = []
    for js in files_to_run:
        # Forzamos reprocesamiento
        res = save_peaks_to_db(js, tolerance=15, prominence=10, force=True)
        summary = {
            "file": res.get("file"),
            "status": res.get("status"),
            "rows_attempted": int(res.get("rows_attempted", 0)),
            "rows_inserted": int(res.get("rows_inserted", 0)),
            "rows_updated": int(res.get("rows_updated", 0)),
            "forced": True,
            "error": res.get("error")
        }
        if summary["status"] == "success":
            logger.info(f"[TEST FORCE] {summary['file']} → inserted={summary['rows_inserted']} updated={summary['rows_updated']} attempted={summary['rows_attempted']} forced={summary['forced']}")
        else:
            logger.error(f"[TEST FORCE] {summary['file']} → status={summary['status']} error={summary['error']}")
            log_error(f"[TEST FORCE] save_peaks failed for {js}: {summary['error'] or summary['status']}")
            raise RuntimeError(f"[TEST FORCE] save_peaks failed for {js}: {summary['error'] or summary['status']}")
        summaries.append(summary)

    return summaries
```

### Pasos después de pegar el cambio
1. Guardar, `git add`, `git commit`.
2. `docker-compose restart airflow`.
3. Probar la tarea de test (CLI):
```bash
docker-compose exec airflow bash
airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00
# o con la tarea de producción
airflow tasks test raman_pipeline peaks_raman 2025-08-15T00:00:00
```
4. Verificar en logs que aparezcan las líneas del `logger.info(...)` con los campos `inserted` y `updated`.

### Checks útiles (consultas)
- Verificar tabla `etl_processed_files`:
```bash
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, rows_inserted, rows_updated, rows_attempted, forced, status, processed_at FROM etl_processed_files ORDER BY processed_at DESC LIMIT 20;"
```
- Revisar XCom resumido (desde UI o CLI) si necesitas el retorno de la tarea.

---

### Comentario operativo final
Con los cambios que ya aplicaste (`rows_updated` y `forced`) y con el DAG logueando estos campos, tendrás trazabilidad completa: *quién* (prueba o producción) ejecutó, cuántos picos se intentaron, cuántos se insertaron y cuántos se actualizaron. Eso facilita decidir si un reprocesamiento con distintos parámetros valió la pena.

Si quieres, aplico yo el cambio en el DAG (te doy el `git diff`) o te lo dejo para que reemplaces tú mismo. ¿Lo aplico ahora y ejecuto una prueba `peaks_raman_test` para confirmar el logging?

### Assistant
Perfecto — procedo sin preguntas y te entrego **la modificación lista para reemplazar** en `Airflow/Dags/raman_pipeline.py` que añade una **tarea de prueba temporal** que ejecuta `save_peaks_to_db(..., force=True)` de punta a punta. También incluyo instrucciones claras (comandos) para desplegar, ejecutar el task de prueba y validar resultados.  

A continuación tienes:

1. **El DAG completo (lista para copiar/pegar y reemplazar el archivo actual).**
2. **Pasos exactos para desplegar y ejecutar la prueba (CLI + UI).**
3. **Chequeos post-ejecución y cómo revertir la modificación.**

---

# 1) Archivo `Airflow/Dags/raman_pipeline.py` — versión modificada (PRUEBA con `force=True`)

```python
# Airflow/Dags/raman_pipeline.py
import os
import glob
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Importa tus funciones ETL — asumimos PYTHONPATH ya configurado en el contenedor
from ETL.Bronze.extract_raman import extract_raman
from ETL.Silver.clean_data import clean_data
from ETL.Gold.load_to_postgres import load_to_postgres
from ETL.Gold.save_peaks import save_peaks_to_db

# ===== Config logging del DAG =====
logger = logging.getLogger("raman_pipeline")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)

# ===== Default args =====
default_args = {
    "owner": "omicas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="raman_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    # -------------------------
    # 1) BRONZE
    # -------------------------
    def bronze_task(raw_dir: str = "/opt/airflow/project/data/Raman_files", **_):
        # extract_raman debe escribir archivos en raw_dir/json o similar
        extract_raman(raw_dir)

    t_bronze = PythonOperator(
        task_id="bronze_raman",
        python_callable=bronze_task,
        op_kwargs={"raw_dir": "/opt/airflow/project/data/Raman_files"},
    )

    # -------------------------
    # 2) SILVER
    # -------------------------
    def silver_task(**_):
        bronze_dir = "/opt/airflow/project/data/Raman_files/json"
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        os.makedirs(silver_dir, exist_ok=True)
        for js in glob.glob(f"{bronze_dir}/*.json"):
            out = os.path.join(silver_dir, os.path.basename(js))
            clean_data(js, out)

    t_silver = PythonOperator(
        task_id="silver_raman",
        python_callable=silver_task,
    )

    # -------------------------
    # 3) GOLD: cargar espectros completos
    # -------------------------
    def gold_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        for js in glob.glob(f"{silver_dir}/*.json"):
            load_to_postgres(js, table_name="raman")

    t_gold = PythonOperator(
        task_id="gold_raman",
        python_callable=gold_task,
    )

    # -------------------------
    # 4) GOLD: picos detectados (producción)
    #    (mantengo la tarea original - sin force)
    # -------------------------
    def peaks_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        results = []
        for js in glob.glob(f"{silver_dir}/*.json"):
            # Llamada normal (no force) — comportamiento de producción
            res = save_peaks_to_db(js, tolerance=15, prominence=10)
            results.append(res)
            if res.get("status") != "success":
                err = res.get("error") or f"status={res.get('status')}"
                logger.error(f"save_peaks failed for {js}: {err}")
                # Marcamos fallo para que Airflow haga retry según tus default_args
                raise RuntimeError(f"save_peaks failed for {js}: {err}")
        return results

    t_peaks = PythonOperator(
        task_id="peaks_raman",
        python_callable=peaks_task,
    )

    # -------------------------
    # 5) TAREA TEMPORAL DE PRUEBA (FORCE = True)
    #    — esta tarea es la que añadirás temporalmente para la "prueba en caliente"
    # -------------------------
    def peaks_test_task(**_):
        """
        Prueba de punta-a-punta que fuerza reprocesar todos los .json del Silver:
        llama save_peaks_to_db(..., force=True) y falla si alguno no retorna 'success'.
        """
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        results = []
        for js in glob.glob(f"{silver_dir}/*.json"):
            # Aquí forzamos re-procesamiento
            res = save_peaks_to_db(js, tolerance=15, prominence=10, force=True)
            results.append(res)
            if res.get("status") != "success":
                err = res.get("error") or f"status={res.get('status')}"
                logger.error(f"[TEST FORCE] save_peaks failed for {js}: {err}")
                # Queremos que falle para validar retries / manejo de errores
                raise RuntimeError(f"[TEST FORCE] save_peaks failed for {js}: {err}")
        return results

    t_peaks_test = PythonOperator(
        task_id="peaks_raman_test",
        python_callable=peaks_test_task,
    )

    # -------------------------
    # Flujo (por defecto): Bronze -> Silver -> Gold -> Peaks (producción)
    # Para la prueba temporal: Bronze -> Silver -> Gold -> peaks_raman_test
    # -------------------------
    t_bronze >> t_silver >> t_gold >> t_peaks
    # Añadimos también la ruta de prueba (no elimina la ruta de producción)
    t_bronze >> t_silver >> t_gold >> t_peaks_test
```

> Nota: este DAG **mantiene la tarea de producción (`peaks_raman`)** y añade **`peaks_raman_test`** que hace exactamente lo mismo pero con `force=True`. Cuando la prueba termine y confirmes, borrarás `t_peaks_test` (o comentar) para volver al estado original.

---

# 2) Pasos concretos para desplegar y ejecutar la prueba

Asumo que trabajas con `docker-compose` en la raíz del repo (como antes).

A. **Actualizar el archivo en tu repo local**
- Reemplaza `Airflow/Dags/raman_pipeline.py` con el contenido anterior.
- Commit opcional:
```bash
git add Airflow/Dags/raman_pipeline.py
git commit -m "feat: add peaks_raman_test temporary task (force=True) for end-to-end test"
```

B. **No necesitas rebuild si usas bind-mounts** (según tu `docker-compose.yml` tienes `./Airflow/Dags:/opt/airflow/dags`), pero reiniciar el scheduler/web mejora el reload:
```bash
# entra al directorio del proyecto (donde está docker-compose.yml) y ejecuta:
docker-compose down
docker-compose up -d
# si prefieres evitar downtime del Postgres/MinIO puedes reiniciar solo Airflow:
docker-compose restart airflow
```

C. **Verificar que Airflow vea el DAG**
- En el contenedor:
```bash
docker-compose exec airflow bash
# dentro del contenedor:
airflow dags list | grep raman_pipeline
```
- En UI: `http://localhost:8081` → busca `raman_pipeline`.

D. **Ejecución de la tarea de prueba (dos opciones)**

**Opción 1 — CLI (rápida, ejecuta solo el task de prueba)**
```bash
# desde host
docker-compose exec airflow bash

# dentro del contenedor ejecutar:
# (elige una fecha de ejecución arbitraria; usamos 2025-08-15T00:00:00)
airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00
```
`airflow tasks test` ejecuta la función sin afectar el scheduler y te muestra los logs en la terminal.

**Opción 2 — UI (Trigger DAG completo pero en la rama de test)**
1. En Airflow UI, Trigger the DAG `raman_pipeline`.
2. En `Graph` view selecciona `peaks_raman_test` y elige **Run** (o "Run" desde el panel de la tarea) — esto ejecuta la tarea en el contexto del run.
3. Revisa logs -> `peaks_raman_test` task logs.

E. **Validar resultados**
- Logs: revisa en UI o CLI que veas líneas como:
  - `🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/...`
  - `📋 Tabla raman_peaks asegurada (public.raman_peaks).`
  - `✅ Upsert completado: N picos procesados desde ...`
- DB: desde host (o dentro del contenedor `postgres`):
```bash
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, COUNT(*) FROM raman_peaks GROUP BY json_filename ORDER BY json_filename LIMIT 10;"
```
- XCom / result: `peaks_raman_test` devuelve `results` (list); si prefieres ver XCom desde UI -> Task instance -> XCom.

---

# 3) Chequeos previos obligatorios (antes de ejecutar)

- `GOLD_DB_CONN` está definida y visible dentro del contenedor Airflow:
```bash
docker-compose exec airflow bash
echo $GOLD_DB_CONN
# o desde python:
python - <<'PY'
import os
print(os.getenv("GOLD_DB_CONN"))
PY
```
- El DAG está actualizado en `/opt/airflow/dags` dentro del contenedor.
- Asegúrate que el archivo `ETL/Gold/save_peaks.py` que ya modificamos acepta `force` y lo utiliza (tal como vimos en sesiones previas).

---

# 4) Cómo revertir (después de la prueba)

- Si la prueba funcionó y quieres volver al DAG original:
  - Simplemente elimina / comenta la tarea `t_peaks_test` y su ruta `t_bronze >> ... >> t_peaks_test`.
  - Commit y reload/restart Airflow (o `docker-compose restart airflow`) si quieres.
- Alternativamente, deja el código ahí pero **no lo ejecutes**; la rama de producción sigue siendo `peaks_raman`.

---

# 5) Recomendaciones finales y riesgos a considerar
- Esta prueba con `force=True` **rehace upserts** y puede sobrescribir filas existentes (esa es la intención de la prueba). Asegúrate que la tabla `raman_peaks` esté respaldada si tus datos en producción son sensibles.
- Si tu dataset Silver contiene muchos archivos, la tarea puede tardar y consumir recursos; vigila el consumo del contenedor y la latencia en Postgres.
- Es buena práctica limitar la prueba a uno o pocos archivos si quieres validar la lógica sin afectar toda la tabla — para ello modifica temporalmente `for js in glob.glob(...)` a iterar solo sobre `glob.glob(... )[:1]`.

---

Si quieres, hago lo siguiente ahora mismo (elige una opción):

1. **Te entrego el mismo archivo pero con la versión comentada para procesar únicamente el primer `.json`** (prueba aún más segura).
2. **Te devuelvo un patch `diff`/`git` que puedas aplicar** (por si prefieres revisión previa).
3. **Te creo el commit y te doy los comandos exactos para ejecutar la prueba en tu contenedor** (si me confirmas que puedo asumir las rutas que ya usas).

Dime cuál de las tres opciones prefieres y procedo inmediatamente.

### Human
Para mejor contexto, te dare los codigos actuales (estaba trabajando sobre save_peaks.py)

# ETL/Gold/save_peaks.py
import os
import logging
import traceback
import pandas as pd
import numpy as np
from typing import Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from ETL.Silver.inspect_peaks import inspect_peaks
from scripts.utils import parse_ids_from_filename

load_dotenv()

# --- Configuración de logs ---
LOG_DIR = os.getenv("RAMAN_LOG_DIR", "/opt/airflow/project/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "save_peaks.log")

logger = logging.getLogger("save_peaks")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    logger.addHandler(fh)

# --- SQL para asegurar la tabla raman_peaks ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.raman_peaks (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    shift_cm1 DOUBLE PRECISION NOT NULL,
    intensity DOUBLE PRECISION NOT NULL,
    peak_type VARCHAR(50) NOT NULL,
    sample_id INTEGER DEFAULT NULL,
    sensor_id INTEGER NOT NULL DEFAULT -1,
    technique TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (json_filename, shift_cm1, sensor_id)
);
"""

# --- SQL para asegurar la tabla de tracking processed files ---
CREATE_PROCESSED_SQL = """
CREATE TABLE IF NOT EXISTS public.etl_processed_files (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    rows_inserted INTEGER DEFAULT 0,
    status TEXT,
    rows_attempted INTEGER DEFAULT 0,
    UNIQUE (json_filename)
);
"""

def ensure_processed_files_columns(engine):
    """Agrega columnas faltantes a etl_processed_files si no existen."""
    with engine.begin() as conn:
        existing_cols = {
            row[0]
            for row in conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'"
            ))
        }
        if "rows_attempted" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")

def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks",
                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
    """
    Procesa un archivo JSON de Raman, detecta picos y los inserta/actualiza en Postgres.
    Retorna un dict con estadísticas para Airflow/XCom.
    """
    result = {
        "file": os.path.basename(json_path),
        "rows_inserted": 0,
        "rows_attempted": 0,
        "status": "failed",
        "error": None
    }

    logger.info(f"🔄 Procesando picos de: {json_path}")

    conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL")
    if not conn_str:
        error_msg = (
            "❌ La variable GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL no está configurada. "
            "Agrega la variable en tu .env / docker-compose.yml."
        )
        logger.critical(error_msg)
        result["error"] = error_msg
        return result

    engine = create_engine(conn_str)

    # 1️⃣ Asegurar tablas (raman_peaks + etl_processed_files)
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_TABLE_SQL))
            conn.execute(text(CREATE_PROCESSED_SQL))
        ensure_processed_files_columns(engine)
        logger.info(f"📋 Tablas aseguradas: public.{table_name}, public.etl_processed_files")
    except SQLAlchemyError as e:
        error_msg = f"Error creando tablas: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result
    except Exception:
        error_msg = f"Error inesperado creando tablas: {traceback.format_exc()}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    # 2️⃣ Skip: si ya fue procesado con éxito y no requiere reprocesar (no es force)
    if not force:
        try:
            with engine.connect() as conn:
                existing_status = conn.execute(
                    text("SELECT status FROM public.etl_processed_files WHERE json_filename = :fn"),
                    {"fn": os.path.basename(json_path)}
                ).scalar()
                if existing_status == "success":
                    logger.info(f"⏭️ {json_path} ya procesado con éxito, sin cambios.")
                    return {**result, "status": "success", "error": None}
        except Exception:
            logger.warning("⚠️ No se pudo comprobar etl_processed_files, procesando de todas formas.")

        

    # 3️⃣ Inspección de picos
    try:
        peaks_df, key_matches = inspect_peaks(json_path, plot=False, **find_peaks_kwargs)
    except Exception as e:
        error_msg = f"❌ Error inspeccionando picos: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    if peaks_df is None or peaks_df.empty:
        logger.warning(f"⚠️ No se detectaron picos en {json_path}")
        return {**result, "status": "no_peaks"}

    # Normalizar columnas
    if "shift_cm-1" in peaks_df.columns:
        peaks_df = peaks_df.rename(columns={"shift_cm-1": "shift_cm1"})
    peaks_df["json_filename"] = os.path.basename(json_path)
    if "sensor_id" not in peaks_df.columns:
        peaks_df["sensor_id"] = -1
    if "sample_id" not in peaks_df.columns:
        peaks_df["sample_id"] = None
    if "technique" not in peaks_df.columns:
        peaks_df["technique"] = None
    if "peak_type" not in peaks_df.columns:
        peaks_df["peak_type"] = "Other"

    # Parsear IDs desde filename
    sensor_val, sample_val = parse_ids_from_filename(json_path)
    if sensor_val is not None:
        peaks_df["sensor_id"] = int(sensor_val)
    if sample_val is not None:
        peaks_df["sample_id"] = int(sample_val)

    # 4️⃣ Upsert determinista
    staging_table = f"{table_name}_staging"
    rows_to_process = len(peaks_df)
    result["rows_attempted"] = rows_to_process

    try:
        with engine.begin() as conn:
            pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            logger.info(f"📊 Total antes: {pre_total}")

            peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500)

            inserted_new = conn.execute(text(f"""
                WITH new_rows AS (
                  INSERT INTO public.{table_name} 
                  (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at)
                  SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now()
                  FROM {staging_table} s
                  LEFT JOIN public.{table_name} r
                    ON r.json_filename = s.json_filename
                   AND r.shift_cm1 = s.shift_cm1
                   AND r.sensor_id = s.sensor_id
                  WHERE r.json_filename IS NULL
                  RETURNING 1
                )
                SELECT COUNT(*) FROM new_rows;
            """)).scalar()

            conn.execute(text(f"""
                UPDATE public.{table_name} t
                SET intensity = s.intensity,
                    peak_type = s.peak_type,
                    sample_id = s.sample_id,
                    detected_at = now()
                FROM {staging_table} s
                WHERE t.json_filename = s.json_filename
                  AND t.shift_cm1 = s.shift_cm1
                  AND t.sensor_id = s.sensor_id;
            """))

            post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))

        delta = post_total - pre_total
        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
        result["rows_inserted"] = inserted_new or 0
        result["status"] = "success"

    except Exception as e:
        result["error"] = f"Error en upsert: {e}"
        logger.exception(result["error"])
        return result

    # 5️⃣ Registrar archivo procesado
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, status)
                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :st)
                ON CONFLICT (json_filename) DO UPDATE
                SET processed_at = now(),
                    rows_inserted = EXCLUDED.rows_inserted,
                    rows_attempted = EXCLUDED.rows_attempted,
                    status = EXCLUDED.status;
            """), {
                "fn": os.path.basename(json_path),
                "rows_inserted": result["rows_inserted"],
                "rows_attempted": result["rows_attempted"],
                "st": result["status"]
            })
    except Exception:
        logger.exception("⚠️ No se pudo registrar en etl_processed_files")

    return result

# Airflow/Dags/raman_pipeline.py

import sys, os, glob, time, logging
from datetime import datetime, timedelta

PROJECT_ROOT = "/opt/airflow/project"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)



import sys, os, glob, time, logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from ETL.Gold.save_peaks import save_peaks_to_db
import pandas as pd

# Asegurar que /opt/airflow/project está en sys.path
PROJECT_ROOT = "/opt/airflow/project"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ETL.Bronze.extract_raman import extract_raman
from ETL.Silver.clean_data import clean_data
from ETL.Gold.load_to_postgres import load_to_postgres
from ETL.Gold.save_peaks import save_peaks_to_db

# ===== Configuración de logging doble =====
log_file_path = "/opt/airflow/logs/raman_pipeline.log"
error_log_path = "/opt/airflow/logs/raman_pipeline_errors.log"

logger = logging.getLogger("raman_pipeline")
logger.setLevel(logging.INFO)

# Handler a archivo
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# Handler a stdout (capturado por Airflow)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# Evitar duplicados si el DAG se recarga
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def log_error(msg: str):
    with open(error_log_path, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    logger.error(msg)

# ===== Default Args =====
default_args = {
    "owner": "omicas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="raman_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False
) as dag:

    # 1. BRONZE
    t_bronze = PythonOperator(
        task_id="bronze_raman",
        python_callable=extract_raman,
        op_kwargs={"raw_dir": "/opt/airflow/project/data/Raman_files"},
    )

    # 2. SILVER
    def silver_task(**_):
        bronze_dir = "/opt/airflow/project/data/Raman_files/json"
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        os.makedirs(silver_dir, exist_ok=True)
        for js in glob.glob(f"{bronze_dir}/*.json"):
            out = os.path.join(silver_dir, os.path.basename(js))
            clean_data(js, out)

    t_silver = PythonOperator(
        task_id="silver_raman",
        python_callable=silver_task,
    )

    # 3. GOLD: Espectros completos
    def gold_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        for js in glob.glob(f"{silver_dir}/*.json"):
            load_to_postgres(js, table_name="raman")

    t_gold = PythonOperator(
        task_id="gold_raman",
        python_callable=gold_task,
    )

    # 4. GOLD: Picos detectados
    def peaks_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        results = []
        for js in glob.glob(f"{silver_dir}/*.json"):
            res = save_peaks_to_db(js, tolerance=15, prominence=10)
            results.append(res)
            
            # Forzar fallo para que Airflow haga retry si la inserción no fue exitosa
            status = res.get("status")
            if status == "failed":
                err = res.get("error") or "status=failed"
                log_error(f"save_peaks failed for {js}: {err}")
                raise RuntimeError(f"save_peaks failed for {js}: {err}")
            elif status == "skipped":
                logger.info(f"save_peaks skipped {js} (already processed).")
            else:
                continue
        return results  # Airflow lo guarda en XCom


    t_peaks = PythonOperator(
        task_id="peaks_raman",
        python_callable=peaks_task,
    )

    t_bronze >> t_silver >> t_gold >> t_peaks


### Human
Puedo generar el patch completo (diff) para save_peaks.py + raman_pipeline.py y el SQL, listo para git apply. ¿Lo quieres ahora? Si sí, lo creo y te lo doy listo para aplicar. Si prefieres aplicarlo tú, te paso los archivos completos listos para pegar.

DALE PERO DAMELO YA LISTO TODO COMPLETO EN FORMATOS PYTHON POR FAVOR, NO ME GUSTA USAR ESO DE COMANDOS DESDE TERMINAL

### Human
Ayudame sigamos con esto del proyecto de omicas. Te doy el contexto 6.

Quedamos en el ultimo chat
¿Quieres que te pase el archivo completo ya fusionado con este cambio para que lo reemplaces de inmediato y lancemos la prueba? Así no tienes que hacer copy-paste de partes.
You said:
Pues ya lo hice creo. Verificame por favor de que todo este correcto y en orden, para luego hacer las pruebas en caliente # ETL/Gold/save_peaks.py import os import logging import traceback import pandas as pd import numpy as np from typing import Dict, Any from sqlalchemy import create_engine, text from sqlalchemy.exc import SQLAlchemyError from dotenv import load_dotenv from ETL.Silver.inspect_peaks import inspect_peaks from scripts.utils import parse_ids_from_filename load_dotenv() # --- Configuración de logs --- LOG_DIR = os.getenv("RAMAN_LOG_DIR", "/opt/airflow/project/logs") os.makedirs(LOG_DIR, exist_ok=True) LOG_FILE = os.path.join(LOG_DIR, "save_peaks.log") logger = logging.getLogger("save_peaks") if not logger.handlers: logger.setLevel(logging.INFO) sh = logging.StreamHandler() sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")) fh = logging.FileHandler(LOG_FILE) fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")) logger.addHandler(sh) logger.addHandler(fh) # --- SQL para asegurar la tabla raman_peaks --- CREATE_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS public.raman_peaks ( id SERIAL PRIMARY KEY, json_filename TEXT NOT NULL, shift_cm1 DOUBLE PRECISION NOT NULL, intensity DOUBLE PRECISION NOT NULL, peak_type VARCHAR(50) NOT NULL, sample_id INTEGER DEFAULT NULL, sensor_id INTEGER NOT NULL DEFAULT -1, technique TEXT, detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, UNIQUE (json_filename, shift_cm1, sensor_id) ); """ # --- SQL para asegurar la tabla de tracking processed files --- CREATE_PROCESSED_SQL = """ CREATE TABLE IF NOT EXISTS public.etl_processed_files ( id SERIAL PRIMARY KEY, json_filename TEXT NOT NULL, processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, rows_inserted INTEGER DEFAULT 0, status TEXT, rows_attempted INTEGER DEFAULT 0, UNIQUE (json_filename) ); """ def ensure_processed_files_columns(engine): """Agrega columnas faltantes a etl_processed_files si no existen.""" with engine.begin() as conn: existing_cols = { row[0] for row in conn.execute(text( "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'" )) } if "rows_attempted" not in existing_cols: conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;")) logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.") def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks", tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]: """ Procesa un archivo JSON de Raman, detecta picos y los inserta/actualiza en Postgres. Retorna un dict con estadísticas para Airflow/XCom. """ result = { "file": os.path.basename(json_path), "rows_inserted": 0, "rows_attempted": 0, "status": "failed", "error": None } logger.info(f"🔄 Procesando picos de: {json_path}") conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL") if not conn_str: error_msg = ( "❌ La variable GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL no está configurada. " "Agrega la variable en tu .env / docker-compose.yml." ) logger.critical(error_msg) result["error"] = error_msg return result engine = create_engine(conn_str) # 1️⃣ Asegurar tablas (raman_peaks + etl_processed_files) try: with engine.begin() as conn: conn.execute(text(CREATE_TABLE_SQL)) conn.execute(text(CREATE_PROCESSED_SQL)) ensure_processed_files_columns(engine) logger.info(f"📋 Tablas aseguradas: public.{table_name}, public.etl_processed_files") except SQLAlchemyError as e: error_msg = f"Error creando tablas: {e}" logger.error(error_msg) result["error"] = error_msg return result except Exception: error_msg = f"Error inesperado creando tablas: {traceback.format_exc()}" logger.error(error_msg) result["error"] = error_msg return result # 2️⃣ Skip: si ya fue procesado con éxito y no requiere reprocesar (no es force) if not force: try: with engine.connect() as conn: existing_status = conn.execute( text("SELECT status FROM public.etl_processed_files WHERE json_filename = :fn"), {"fn": os.path.basename(json_path)} ).scalar() if existing_status == "success": logger.info(f"⏭️ {json_path} ya procesado con éxito, sin cambios.") return {**result, "status": "success", "error": None} except Exception: logger.warning("⚠️ No se pudo comprobar etl_processed_files, procesando de todas formas.") # 3️⃣ Inspección de picos try: peaks_df, key_matches = inspect_peaks(json_path, plot=False, **find_peaks_kwargs) except Exception as e: error_msg = f"❌ Error inspeccionando picos: {e}" logger.error(error_msg) result["error"] = error_msg return result if peaks_df is None or peaks_df.empty: logger.warning(f"⚠️ No se detectaron picos en {json_path}") return {**result, "status": "no_peaks"} # Normalizar columnas if "shift_cm-1" in peaks_df.columns: peaks_df = peaks_df.rename(columns={"shift_cm-1": "shift_cm1"}) peaks_df["json_filename"] = os.path.basename(json_path) if "sensor_id" not in peaks_df.columns: peaks_df["sensor_id"] = -1 if "sample_id" not in peaks_df.columns: peaks_df["sample_id"] = None if "technique" not in peaks_df.columns: peaks_df["technique"] = None if "peak_type" not in peaks_df.columns: peaks_df["peak_type"] = "Other" # Parsear IDs desde filename sensor_val, sample_val = parse_ids_from_filename(json_path) if sensor_val is not None: peaks_df["sensor_id"] = int(sensor_val) if sample_val is not None: peaks_df["sample_id"] = int(sample_val) # 4️⃣ Upsert determinista staging_table = f"{table_name}_staging" rows_to_process = len(peaks_df) result["rows_attempted"] = rows_to_process try: with engine.begin() as conn: pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar() logger.info(f"📊 Total antes: {pre_total}") peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500) inserted_new = conn.execute(text(f""" WITH new_rows AS ( INSERT INTO public.{table_name} (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at) SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now() FROM {staging_table} s LEFT JOIN public.{table_name} r ON r.json_filename = s.json_filename AND r.shift_cm1 = s.shift_cm1 AND r.sensor_id = s.sensor_id WHERE r.json_filename IS NULL RETURNING 1 ) SELECT COUNT(*) FROM new_rows; """)).scalar() conn.execute(text(f""" UPDATE public.{table_name} t SET intensity = s.intensity, peak_type = s.peak_type, sample_id = s.sample_id, detected_at = now() FROM {staging_table} s WHERE t.json_filename = s.json_filename AND t.shift_cm1 = s.shift_cm1 AND t.sensor_id = s.sensor_id; """)) post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar() conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}")) delta = post_total - pre_total logger.info(f"📈 Total después: {post_total} (Δ {delta})") result["rows_inserted"] = inserted_new or 0 result["status"] = "success" except Exception as e: result["error"] = f"Error en upsert: {e}" logger.exception(result["error"]) return result # 5️⃣ Registrar archivo procesado try: with engine.begin() as conn: conn.execute(text(""" INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, status) VALUES (:fn, now(), :rows_inserted, :rows_attempted, :st) ON CONFLICT (json_filename) DO UPDATE SET processed_at = now(), rows_inserted = EXCLUDED.rows_inserted, rows_attempted = EXCLUDED.rows_attempted, status = EXCLUDED.status; """), { "fn": os.path.basename(json_path), "rows_inserted": result["rows_inserted"], "rows_attempted": result["rows_attempted"], "st": result["status"] }) except Exception: logger.exception("⚠️ No se pudo registrar en etl_processed_files") return result Ademas airflow@6dec45b5b289:/opt/airflow$ python -c "from ETL.Gold.save_peaks import save_peaks_to_db; print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))" 2025-08-15 02:22:31,757 [INFO] 🔄 Procesando picos de: /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json 2025-08-15 02:22:31,795 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files 🔎 Detectados 514 picos en /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json 2025-08-15 02:22:31,816 [INFO] 📊 Total antes: 1855 2025-08-15 02:22:31,867 [INFO] 📈 Total después: 2284 (Δ 429) {'file': 'WE-PI-CHINA-1.json', 'rows_inserted': 429, 'rows_attempted': 514, 'status': 'success', 'error': None}
ChatGPT said:
Revisé tu código y está correcto:
•	El parámetro force está bien implementado y documentado en el docstring.
•	El skip solo ocurre si force=False y ya existe el registro con estado "success".
•	El resto de la lógica de detección, normalización, inserción y registro en etl_processed_files quedó intacta.
•	No hay fugas de conexión ni problemas de logging.
•	El test que corriste en caliente confirmó que la inserción forzada funciona:
•	514 picos detectados (rows_attempted)
•	429 nuevos insertados (rows_inserted)
•	Conteo en raman_peaks pasó de 1855 → 2284 (+429), lo que cuadra con el delta registrado.
Esto significa que:
•	El flujo de detección → staging → upsert → conteo está funcionando perfectamente.
•	La lógica de force te permite reprocesar sin alterar el comportamiento en producción.
El siguiente paso lógico sería correrlo también desde el DAG con force=True en un task específico de pruebas para validar que el pipeline entero (no solo la función) maneja correctamente el caso forzado.
¿Quieres que te prepare esa modificación temporal en el DAG para probarlo de punta a punta?

Entonces mi respuesta a esta ultima pregunta es si por favor

### Human
Okay mira los resultados
docker-compose exec airflow bash -c "python - <<'PY'
╰─❯ from ETL.Gold.save_peaks import save_peaks_to_db
╰─❯ print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
╰─❯ PY"
2025-08-15 02:57:47,007 [INFO] 🔄 Procesando picos de: /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json
2025-08-15 02:57:47,052 [INFO] 🛠️ Columna rows_updated agregada a etl_processed_files.
2025-08-15 02:57:47,053 [INFO] 🛠️ Columna forced agregada a etl_processed_files.
2025-08-15 02:57:47,055 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
🔎 Detectados 514 picos en /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json
2025-08-15 02:57:47,075 [INFO] 📊 Total antes: 2284
2025-08-15 02:57:47,113 [INFO] 📈 Total después: 2284 (Δ 0)
{'file': 'WE-PI-CHINA-1.json', 'rows_inserted': 0, 'rows_updated': 0, 'rows_attempted': 514, 'status': 'success', 'error': None}

docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, rows_inserted, rows_attempted, rows_updated, forced, status FROM etl_processed_files WHERE json_filename = 'WE-PI-CHINA-1.json';"
   json_filename    | rows_inserted | rows_attempted | rows_updated | forced | status  
--------------------+---------------+----------------+--------------+--------+---------
 WE-PI-CHINA-1.json |             0 |            514 |            0 | t      | success
(1 row)

Si quieres, aplico también el cambio equivalente en el DAG para que registre en logs los valores rows_updated y forced (opcional). ¿Lo hago ahora?
Pues que consideras tu? Teniendo en cuenta los resultado anteriores?

### Assistant
Perfecto — te entrego **todo listo en Python**. Reemplaza los archivos correspondientes con los contenidos que siguen y ejecuta sólo el script de migración en Python (`db_migration.py`) una vez (usa `python db_migration.py` dentro del contenedor/entorno donde están tus variables de entorno). No necesitas usar comandos SQL manuales ni `git apply`.

Entregué 3 archivos:

- `ETL/Gold/save_peaks.py` — versión actualizada y completa (hash de archivo, params detector, skip seguro, rows_updated, forced).
- `Airflow/Dags/raman_pipeline.py` — DAG actualizado que lee los parámetros desde una Airflow Variable `raman_detector_params` (si no existe usa defaults) y pasa esos parámetros a `save_peaks_to_db`.
- `scripts/db_migration.py` — script Python que aplica la migración `ALTER TABLE` segura para agregar columnas `file_hash` y `detector_params` (idempotente).

---

### Archivo 1 — `ETL/Gold/save_peaks.py`
```python
# ETL/Gold/save_peaks.py
import os
import logging
import traceback
import pandas as pd
import numpy as np
import json
import hashlib
from typing import Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from ETL.Silver.inspect_peaks import inspect_peaks
from scripts.utils import parse_ids_from_filename

load_dotenv()

# --- Configuración de logs ---
LOG_DIR = os.getenv("RAMAN_LOG_DIR", "/opt/airflow/project/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "save_peaks.log")

logger = logging.getLogger("save_peaks")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    logger.addHandler(fh)

# --- SQL para asegurar la tabla raman_peaks ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.raman_peaks (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    shift_cm1 DOUBLE PRECISION NOT NULL,
    intensity DOUBLE PRECISION NOT NULL,
    peak_type VARCHAR(50) NOT NULL,
    sample_id INTEGER DEFAULT NULL,
    sensor_id INTEGER NOT NULL DEFAULT -1,
    technique TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (json_filename, shift_cm1, sensor_id)
);
"""

# --- SQL para asegurar la tabla de tracking processed files ---
CREATE_PROCESSED_SQL = """
CREATE TABLE IF NOT EXISTS public.etl_processed_files (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    rows_inserted INTEGER DEFAULT 0,
    status TEXT,
    rows_attempted INTEGER DEFAULT 0,
    rows_updated INTEGER DEFAULT 0,
    forced BOOLEAN DEFAULT FALSE,
    file_hash TEXT,
    detector_params JSONB,
    UNIQUE (json_filename)
);
"""

def ensure_processed_files_columns(engine):
    """Agrega columnas faltantes a etl_processed_files si no existen (idempotente)."""
    with engine.begin() as conn:
        existing_cols = {
            row[0]
            for row in conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'"
            ))
        }
        if "rows_attempted" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")
        if "rows_updated" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_updated INTEGER DEFAULT 0;"))
            logger.info("🛠️ Columna rows_updated agregada a etl_processed_files.")
        if "forced" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN forced BOOLEAN DEFAULT FALSE;"))
            logger.info("🛠️ Columna forced agregada a etl_processed_files.")
        if "file_hash" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN file_hash TEXT;"))
            logger.info("🛠️ Columna file_hash agregada a etl_processed_files.")
        if "detector_params" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN detector_params JSONB;"))
            logger.info("🛠️ Columna detector_params agregada a etl_processed_files.")

def file_md5(path: str) -> str:
    """Calcula md5 del archivo (streaming)."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize_params_json(params: dict) -> str:
    """Devuelve JSON ordenado (string) para comparación."""
    try:
        return json.dumps(params, sort_keys=True, ensure_ascii=False)
    except Exception:
        return json.dumps({}, sort_keys=True, ensure_ascii=False)

def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks",
                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
    """
    Procesa un archivo JSON de Raman, detecta picos y los inserta/actualiza en Postgres.
    Retorna un dict con estadísticas para Airflow/XCom.
    """
    result = {
        "file": os.path.basename(json_path),
        "rows_inserted": 0,
        "rows_updated": 0,
        "rows_attempted": 0,
        "status": "failed",
        "error": None
    }

    logger.info(f"🔄 Procesando picos de: {json_path}")

    conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL")
    if not conn_str:
        error_msg = (
            "❌ La variable GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL no está configurada. "
            "Agrega la variable en tu .env / docker-compose.yml."
        )
        logger.critical(error_msg)
        result["error"] = error_msg
        return result

    # pool_pre_ping ayuda a recuperar conexiones cuando Postgres se recicla
    engine = create_engine(conn_str, pool_pre_ping=True)

    # 1️⃣ Asegurar tablas (raman_peaks + etl_processed_files)
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_TABLE_SQL))
            conn.execute(text(CREATE_PROCESSED_SQL))
        ensure_processed_files_columns(engine)
        logger.info(f"📋 Tablas aseguradas: public.{table_name}, public.etl_processed_files")
    except SQLAlchemyError as e:
        error_msg = f"Error creando tablas: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result
    except Exception:
        error_msg = f"Error inesperado creando tablas: {traceback.format_exc()}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    # Preparar parámetros y hash del archivo para trazabilidad
    det_params = {"tolerance": tolerance}
    det_params.update({k: v for k, v in find_peaks_kwargs.items()})
    det_params_json = normalize_params_json(det_params)
    try:
        file_hash = file_md5(json_path)
    except Exception:
        file_hash = None
        logger.warning("No se pudo calcular file hash; continuamos sin hash.")

    # 2️⃣ Skip: si ya fue procesado con éxito y no requiere reprocesar (no es force)
    if not force:
        try:
            with engine.connect() as conn:
                row = conn.execute(
                    text("SELECT status, file_hash, detector_params FROM public.etl_processed_files WHERE json_filename = :fn"),
                    {"fn": os.path.basename(json_path)}
                ).fetchone()
                if row and row["status"] == "success":
                    existing_hash = row["file_hash"]
                    existing_params = row["detector_params"]
                    # Normalize existing params to comparable JSON string
                    try:
                        if existing_params is None:
                            existing_params_json = ""
                        else:
                            # existing_params may be a dict (from JSONB) or a string
                            if isinstance(existing_params, dict):
                                existing_params_json = json.dumps(existing_params, sort_keys=True, ensure_ascii=False)
                            else:
                                # try to parse string
                                try:
                                    parsed = json.loads(existing_params)
                                    existing_params_json = json.dumps(parsed, sort_keys=True, ensure_ascii=False)
                                except Exception:
                                    existing_params_json = str(existing_params)
                    except Exception:
                        existing_params_json = ""
                    # Only skip when file_hash and detector params match
                    if file_hash is not None and existing_hash == file_hash and existing_params_json == det_params_json:
                        logger.info(f"⏭️ {json_path} ya procesado con éxito usando los mismos parámetros; skipping.")
                        return {**result, "status": "success", "error": None}
        except Exception:
            logger.warning("⚠️ No se pudo comprobar etl_processed_files; procesando de todas formas.")

    # 3️⃣ Inspección de picos
    try:
        peaks_df, key_matches = inspect_peaks(json_path, plot=False, **find_peaks_kwargs)
    except Exception as e:
        error_msg = f"❌ Error inspeccionando picos: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    if peaks_df is None or peaks_df.empty:
        logger.warning(f"⚠️ No se detectaron picos en {json_path}")
        # Registrar igualmente que fue procesado (no_peaks)
        result["status"] = "no_peaks"
        # Registrar metadata en la tabla
        try:
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, rows_updated, forced, status, file_hash, detector_params)
                    VALUES (:fn, now(), 0, :rows_attempted, 0, :forced, :st, :file_hash, :detector_params::jsonb)
                    ON CONFLICT (json_filename) DO UPDATE
                    SET processed_at = now(),
                        rows_inserted = EXCLUDED.rows_inserted,
                        rows_attempted = EXCLUDED.rows_attempted,
                        rows_updated = EXCLUDED.rows_updated,
                        forced = EXCLUDED.forced,
                        status = EXCLUDED.status,
                        file_hash = EXCLUDED.file_hash,
                        detector_params = EXCLUDED.detector_params;
                """), {
                    "fn": os.path.basename(json_path),
                    "rows_attempted": 0,
                    "forced": bool(force),
                    "st": result["status"],
                    "file_hash": file_hash,
                    "detector_params": det_params_json
                })
        except Exception:
            logger.exception("⚠️ No se pudo registrar en etl_processed_files (no_peaks)")
        return result

    # Normalizar columnas
    if "shift_cm-1" in peaks_df.columns:
        peaks_df = peaks_df.rename(columns={"shift_cm-1": "shift_cm1"})
    peaks_df["json_filename"] = os.path.basename(json_path)
    if "sensor_id" not in peaks_df.columns:
        peaks_df["sensor_id"] = -1
    if "sample_id" not in peaks_df.columns:
        peaks_df["sample_id"] = None
    if "technique" not in peaks_df.columns:
        peaks_df["technique"] = None
    if "peak_type" not in peaks_df.columns:
        peaks_df["peak_type"] = "Other"

    # Parsear IDs desde filename
    sensor_val, sample_val = parse_ids_from_filename(json_path)
    if sensor_val is not None:
        peaks_df["sensor_id"] = int(sensor_val)
    if sample_val is not None:
        peaks_df["sample_id"] = int(sample_val)

    # 4️⃣ Upsert determinista
    staging_table = f"{table_name}_staging"
    rows_to_process = len(peaks_df)
    result["rows_attempted"] = rows_to_process

    try:
        with engine.begin() as conn:
            pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            logger.info(f"📊 Total antes: {pre_total}")

            peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500)

            inserted_new = conn.execute(text(f"""
                WITH new_rows AS (
                  INSERT INTO public.{table_name} 
                  (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at)
                  SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now()
                  FROM {staging_table} s
                  LEFT JOIN public.{table_name} r
                    ON r.json_filename = s.json_filename
                   AND r.shift_cm1 = s.shift_cm1
                   AND r.sensor_id = s.sensor_id
                  WHERE r.json_filename IS NULL
                  RETURNING 1
                )
                SELECT COUNT(*) FROM new_rows;
            """)).scalar()

            # UPDATE pero contando realmente cuántas filas cambiaron (auditable)
            updated_count = conn.execute(text(f"""
                WITH updated AS (
                  UPDATE public.{table_name} t
                  SET intensity = s.intensity,
                      peak_type = s.peak_type,
                      sample_id = s.sample_id,
                      detected_at = now()
                  FROM {staging_table} s
                  WHERE t.json_filename = s.json_filename
                    AND t.shift_cm1 = s.shift_cm1
                    AND t.sensor_id = s.sensor_id
                    AND (
                      t.intensity IS DISTINCT FROM s.intensity
                      OR t.peak_type IS DISTINCT FROM s.peak_type
                      OR t.sample_id IS DISTINCT FROM s.sample_id
                    )
                  RETURNING 1
                )
                SELECT COUNT(*) FROM updated;
            """)).scalar()

            post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))

        delta = post_total - pre_total
        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
        result["rows_inserted"] = int(inserted_new or 0)
        result["rows_updated"] = int(updated_count or 0)
        result["status"] = "success"

    except Exception as e:
        result["error"] = f"Error en upsert: {e}"
        logger.exception(result["error"])
        return result

    # 5️⃣ Registrar archivo procesado (incluye metadata)
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, rows_updated, forced, status, file_hash, detector_params)
                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :rows_updated, :forced, :st, :file_hash, :detector_params::jsonb)
                ON CONFLICT (json_filename) DO UPDATE
                SET processed_at = now(),
                    rows_inserted = EXCLUDED.rows_inserted,
                    rows_attempted = EXCLUDED.rows_attempted,
                    rows_updated = EXCLUDED.rows_updated,
                    forced = EXCLUDED.forced,
                    status = EXCLUDED.status,
                    file_hash = EXCLUDED.file_hash,
                    detector_params = EXCLUDED.detector_params;
            """), {
                "fn": os.path.basename(json_path),
                "rows_inserted": result["rows_inserted"],
                "rows_attempted": result["rows_attempted"],
                "rows_updated": result.get("rows_updated", 0),
                "forced": bool(force),
                "st": result["status"],
                "file_hash": file_hash,
                "detector_params": det_params_json
            })
    except Exception:
        logger.exception("⚠️ No se pudo registrar en etl_processed_files")

    logger.info(f"✅ Resultado: file={result['file']} inserted={result['rows_inserted']} updated={result['rows_updated']} attempted={result['rows_attempted']} status={result['status']} forced={force}")
    return result
```

---

### Archivo 2 — `Airflow/Dags/raman_pipeline.py`
```python
# Airflow/Dags/raman_pipeline.py
import sys
import os
import glob
import logging
import json
from datetime import datetime, timedelta

# Asegurar PATH del proyecto para imports relativos
PROJECT_ROOT = "/opt/airflow/project"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

# ETL functions (as in repo)
from ETL.Bronze.extract_raman import extract_raman
from ETL.Silver.clean_data import clean_data
from ETL.Gold.load_to_postgres import load_to_postgres
from ETL.Gold.save_peaks import save_peaks_to_db

# ===== Configuración de logging del DAG =====
log_file_path = "/opt/airflow/logs/raman_pipeline.log"
error_log_path = "/opt/airflow/logs/raman_pipeline_errors.log"

logger = logging.getLogger("raman_pipeline")
logger.setLevel(logging.INFO)

# Evitar duplicar handlers al recargar el DAG
if not logger.handlers:
    # File handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # Stream handler (capturado por Airflow)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)

def log_error(msg: str):
    try:
        with open(error_log_path, "a") as f:
            f.write(f"{datetime.now()} - {msg}\n")
    except Exception:
        logger.exception("No se pudo escribir en error_log_path")
    logger.error(msg)

# ===== Default args =====
default_args = {
    "owner": "omicas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Variable de entorno que controla cuantos archivos procesar en la prueba (por defecto 1)
TEST_MAX_FILES = int(os.getenv("RAMAN_TEST_MAX_FILES", "1"))

# ===== Detector params desde Airflow Variable (JSON) =====
# Crea / edita esta Variable en Airflow UI si quieres cambiar params sin editar DAG.
_raw = Variable.get("raman_detector_params", default_var='{"tolerance": 15, "prominence": 10}')
try:
    detector_params = json.loads(_raw)
except Exception:
    detector_params = {"tolerance": 15, "prominence": 10}

with DAG(
    dag_id="raman_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    # -------------------------
    # 1) BRONZE
    # -------------------------
    t_bronze = PythonOperator(
        task_id="bronze_raman",
        python_callable=extract_raman,
        op_kwargs={"raw_dir": "/opt/airflow/project/data/Raman_files"},
    )

    # -------------------------
    # 2) SILVER
    # -------------------------
    def silver_task(**_):
        bronze_dir = "/opt/airflow/project/data/Raman_files/json"
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        os.makedirs(silver_dir, exist_ok=True)
        for js in glob.glob(f"{bronze_dir}/*.json"):
            out = os.path.join(silver_dir, os.path.basename(js))
            clean_data(js, out)

    t_silver = PythonOperator(
        task_id="silver_raman",
        python_callable=silver_task,
    )

    # -------------------------
    # 3) GOLD: Espectros completos (producción)
    # -------------------------
    def gold_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        for js in glob.glob(f"{silver_dir}/*.json"):
            load_to_postgres(js, table_name="raman")

    t_gold = PythonOperator(
        task_id="gold_raman",
        python_callable=gold_task,
    )

    # -------------------------
    # 4) GOLD: Picos detectados (producción)
    # -------------------------
    def peaks_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        summaries = []
        for js in sorted(glob.glob(f"{silver_dir}/*.json")):
            res = save_peaks_to_db(js, **detector_params, force=False)
            summary = {
                "file": res.get("file"),
                "status": res.get("status"),
                "rows_attempted": int(res.get("rows_attempted", 0)),
                "rows_inserted": int(res.get("rows_inserted", 0)),
                "rows_updated": int(res.get("rows_updated", 0)),
                "error": res.get("error")
            }
            if summary["status"] == "success":
                logger.info(f"[PROD] {summary['file']} → inserted={summary['rows_inserted']} updated={summary['rows_updated']} attempted={summary['rows_attempted']}")
            elif summary["status"] == "no_peaks":
                logger.info(f"[PROD] {summary['file']} → no_peaks (attempted={summary['rows_attempted']})")
            else:
                logger.error(f"[PROD] {summary['file']} → status={summary['status']} error={summary['error']}")
                log_error(f"save_peaks failed for {js}: {summary['error'] or summary['status']}")
                raise RuntimeError(f"save_peaks failed for {js}: {summary['error'] or summary['status']}")
            summaries.append(summary)
        return summaries

    t_peaks = PythonOperator(
        task_id="peaks_raman",
        python_callable=peaks_task,
    )

    # -------------------------
    # 5) TAREA TEMPORAL DE PRUEBA (FORCE = True)
    #     Por seguridad, procesa por defecto solo TEST_MAX_FILES (env var)
    # -------------------------
    def peaks_test_task(max_files: int = TEST_MAX_FILES, **_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        files = sorted(glob.glob(f"{silver_dir}/*.json"))
        if not files:
            logger.warning("No hay archivos .json en silver_dir para la prueba.")
            return []

        files_to_run = files[:max_files]
        logger.info(f"[TEST FORCE] Procesando {len(files_to_run)} archivo(s) (max_files={max_files})")

        summaries = []
        for js in files_to_run:
            res = save_peaks_to_db(js, **detector_params, force=True)
            summary = {
                "file": res.get("file"),
                "status": res.get("status"),
                "rows_attempted": int(res.get("rows_attempted", 0)),
                "rows_inserted": int(res.get("rows_inserted", 0)),
                "rows_updated": int(res.get("rows_updated", 0)),
                "forced": True,
                "error": res.get("error")
            }
            if summary["status"] == "success":
                logger.info(f"[TEST FORCE] {summary['file']} → inserted={summary['rows_inserted']} updated={summary['rows_updated']} attempted={summary['rows_attempted']} forced={summary['forced']}")
            else:
                logger.error(f"[TEST FORCE] {summary['file']} → status={summary['status']} error={summary['error']}")
                log_error(f"[TEST FORCE] save_peaks failed for {js}: {summary['error'] or summary['status']}")
                raise RuntimeError(f"[TEST FORCE] save_peaks failed for {js}: {summary['error'] or summary['status']}")
            summaries.append(summary)
        return summaries

    t_peaks_test = PythonOperator(
        task_id="peaks_raman_test",
        python_callable=peaks_test_task,
        op_kwargs={"max_files": TEST_MAX_FILES},
    )

    # -------------------------
    # Flujo (por defecto): Bronze -> Silver -> Gold -> Peaks (producción)
    # Ruta de prueba: Bronze -> Silver -> Gold -> peaks_raman_test
    # -------------------------
    t_bronze >> t_silver >> t_gold >> t_peaks
    t_bronze >> t_silver >> t_gold >> t_peaks_test
```

---

### Archivo 3 — `scripts/db_migration.py`
```python
# scripts/db_migration.py
"""
Script Python para aplicar la migración en Postgres.
Ejecutar dentro del entorno donde GOLD_DB_CONN / SQL_ALCHEMY_CONN / POSTGRES_URL estén disponibles.
Ejemplo (dentro del contenedor): python scripts/db_migration.py
"""
import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("db_migration")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL")
if not conn_str:
    logger.error("No se encontró GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL en el entorno. Abortando.")
    raise SystemExit(1)

engine = create_engine(conn_str, pool_pre_ping=True)

MIGRATION_SQL = """
ALTER TABLE public.etl_processed_files
  ADD COLUMN IF NOT EXISTS file_hash TEXT,
  ADD COLUMN IF NOT EXISTS detector_params JSONB;
"""

def run():
    logger.info("Conectando a la base de datos...")
    try:
        with engine.begin() as conn:
            logger.info("Ejecutando migración (ALTER TABLE)...")
            conn.execute(text(MIGRATION_SQL))
        logger.info("Migración aplicada correctamente.")
    except Exception as e:
        logger.exception(f"Error aplicando migración: {e}")
        raise

if __name__ == "__main__":
    run()
```

---

## Qué debes hacer ahora (mínimo, en Python)
1. Reemplaza los archivos `ETL/Gold/save_peaks.py` y `Airflow/Dags/raman_pipeline.py` por los contenidos anteriores.
2. Coloca `scripts/db_migration.py` en `scripts/` y **ejecuta** desde el contenedor/entorno (Python) para aplicar la migración:
   ```bash
   # sólo este único comando para correr el script en Python
   python scripts/db_migration.py
   ```
   (Lo ejecutes en el contenedor Airflow o en un entorno que tenga acceso a la DB y las mismas env vars.)
3. Reinicia Airflow (si tu entorno lo requiere) para que el DAG cargue los cambios:
   - Si usas docker-compose: `docker-compose restart airflow` — (sólo si necesitas; en muchas configuraciones reemplazar el archivo y dejar que Airflow recargue puede ser suficiente).
4. Prueba con:
   - `airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00` (o ejecutar desde terminal si lo sueles hacer).
   - O ejecuta directamente (prueba rápida) en el contenedor:
     ```bash
     python - <<'PY'
     from ETL.Gold.save_peaks import save_peaks_to_db
     print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
     PY
     ```

---

Si quieres, hago ahora mismo dos cosas por ti (elige una):
1. Te doy un **diff textual** para revisar los cambios antes de pegar (por si quieres ver exactamente qué cambié).  
2. Aplico más mejoras (por ejemplo: incluir checksum de parámetros en logs, o exponer `detector_params` en la tabla `raman_peaks`), y te preparo las versiones en Python.

Dime si quieres el `diff` o que aplique la opción (2). Si quieres que simplemente lo pegue y lo pruebes, ya tienes todo lo necesario.

### Human
Okay lo ejecute y mira
airflow@a47347198099:/opt/airflow$ python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json', force=True, prominence=10, tolerance=15))
PY
2025-08-15 02:53:28,172 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
2025-08-15 02:53:28,213 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
🔎 Detectados 85 picos en /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
2025-08-15 02:53:28,231 [INFO] 📊 Total antes: 2284
2025-08-15 02:53:28,252 [INFO] 📈 Total después: 2284 (Δ 0)
{'file': 'WE-PI-CHINA-1.json', 'rows_inserted': 0, 'rows_attempted': 85, 'status': 'success', 'error': None}


3) Patch (diff) — aplicar con git apply

Guarda el siguiente contenido en un archivo save_peaks.patch en la raíz del repo y aplica:

DAMELO PERO EN EL CODIGO FINAL DESDE PYTHON
# ETL/Gold/save_peaks.py
import os
import logging
import traceback
import pandas as pd
import numpy as np
from typing import Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from ETL.Silver.inspect_peaks import inspect_peaks
from scripts.utils import parse_ids_from_filename

load_dotenv()

# --- Configuración de logs ---
LOG_DIR = os.getenv("RAMAN_LOG_DIR", "/opt/airflow/project/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "save_peaks.log")

logger = logging.getLogger("save_peaks")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    logger.addHandler(fh)

# --- SQL para asegurar la tabla raman_peaks ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.raman_peaks (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    shift_cm1 DOUBLE PRECISION NOT NULL,
    intensity DOUBLE PRECISION NOT NULL,
    peak_type VARCHAR(50) NOT NULL,
    sample_id INTEGER DEFAULT NULL,
    sensor_id INTEGER NOT NULL DEFAULT -1,
    technique TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (json_filename, shift_cm1, sensor_id)
);
"""

# --- SQL para asegurar la tabla de tracking processed files ---
CREATE_PROCESSED_SQL = """
CREATE TABLE IF NOT EXISTS public.etl_processed_files (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    rows_inserted INTEGER DEFAULT 0,
    status TEXT,
    rows_attempted INTEGER DEFAULT 0,
    UNIQUE (json_filename)
);
"""

def ensure_processed_files_columns(engine):
    """Agrega columnas faltantes a etl_processed_files si no existen."""
    with engine.begin() as conn:
        existing_cols = {
            row[0]
            for row in conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'"
            ))
        }
        if "rows_attempted" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")

def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks",
                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
    """
    Procesa un archivo JSON de Raman, detecta picos y los inserta/actualiza en Postgres.
    Retorna un dict con estadísticas para Airflow/XCom.
    """
    result = {
        "file": os.path.basename(json_path),
        "rows_inserted": 0,
        "rows_attempted": 0,
        "status": "failed",
        "error": None
    }

    logger.info(f"🔄 Procesando picos de: {json_path}")

    conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL")
    if not conn_str:
        error_msg = (
            "❌ La variable GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL no está configurada. "
            "Agrega la variable en tu .env / docker-compose.yml."
        )
        logger.critical(error_msg)
        result["error"] = error_msg
        return result

    engine = create_engine(conn_str)

    # 1️⃣ Asegurar tablas (raman_peaks + etl_processed_files)
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_TABLE_SQL))
            conn.execute(text(CREATE_PROCESSED_SQL))
        ensure_processed_files_columns(engine)
        logger.info(f"📋 Tablas aseguradas: public.{table_name}, public.etl_processed_files")
    except SQLAlchemyError as e:
        error_msg = f"Error creando tablas: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result
    except Exception:
        error_msg = f"Error inesperado creando tablas: {traceback.format_exc()}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    # 2️⃣ Skip: si ya fue procesado con éxito y no requiere reprocesar (no es force)
    if not force:
        try:
            with engine.connect() as conn:
                existing_status = conn.execute(
                    text("SELECT status FROM public.etl_processed_files WHERE json_filename = :fn"),
                    {"fn": os.path.basename(json_path)}
                ).scalar()
                if existing_status == "success":
                    logger.info(f"⏭️ {json_path} ya procesado con éxito, sin cambios.")
                    return {**result, "status": "success", "error": None}
        except Exception:
            logger.warning("⚠️ No se pudo comprobar etl_processed_files, procesando de todas formas.")

        

    # 3️⃣ Inspección de picos
    try:
        peaks_df, key_matches = inspect_peaks(json_path, plot=False, **find_peaks_kwargs)
    except Exception as e:
        error_msg = f"❌ Error inspeccionando picos: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    if peaks_df is None or peaks_df.empty:
        logger.warning(f"⚠️ No se detectaron picos en {json_path}")
        return {**result, "status": "no_peaks"}

    # Normalizar columnas
    if "shift_cm-1" in peaks_df.columns:
        peaks_df = peaks_df.rename(columns={"shift_cm-1": "shift_cm1"})
    peaks_df["json_filename"] = os.path.basename(json_path)
    if "sensor_id" not in peaks_df.columns:
        peaks_df["sensor_id"] = -1
    if "sample_id" not in peaks_df.columns:
        peaks_df["sample_id"] = None
    if "technique" not in peaks_df.columns:
        peaks_df["technique"] = None
    if "peak_type" not in peaks_df.columns:
        peaks_df["peak_type"] = "Other"

    # Parsear IDs desde filename
    sensor_val, sample_val = parse_ids_from_filename(json_path)
    if sensor_val is not None:
        peaks_df["sensor_id"] = int(sensor_val)
    if sample_val is not None:
        peaks_df["sample_id"] = int(sample_val)

    # 4️⃣ Upsert determinista
    staging_table = f"{table_name}_staging"
    rows_to_process = len(peaks_df)
    result["rows_attempted"] = rows_to_process

    try:
        with engine.begin() as conn:
            pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            logger.info(f"📊 Total antes: {pre_total}")

            peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500)

            inserted_new = conn.execute(text(f"""
                WITH new_rows AS (
                  INSERT INTO public.{table_name} 
                  (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at)
                  SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now()
                  FROM {staging_table} s
                  LEFT JOIN public.{table_name} r
                    ON r.json_filename = s.json_filename
                   AND r.shift_cm1 = s.shift_cm1
                   AND r.sensor_id = s.sensor_id
                  WHERE r.json_filename IS NULL
                  RETURNING 1
                )
                SELECT COUNT(*) FROM new_rows;
            """)).scalar()

            conn.execute(text(f"""
                UPDATE public.{table_name} t
                SET intensity = s.intensity,
                    peak_type = s.peak_type,
                    sample_id = s.sample_id,
                    detected_at = now()
                FROM {staging_table} s
                WHERE t.json_filename = s.json_filename
                  AND t.shift_cm1 = s.shift_cm1
                  AND t.sensor_id = s.sensor_id;
            """))

            post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))

        delta = post_total - pre_total
        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
        result["rows_inserted"] = inserted_new or 0
        result["status"] = "success"

    except Exception as e:
        result["error"] = f"Error en upsert: {e}"
        logger.exception(result["error"])
        return result

    # 5️⃣ Registrar archivo procesado
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, status)
                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :st)
                ON CONFLICT (json_filename) DO UPDATE
                SET processed_at = now(),
                    rows_inserted = EXCLUDED.rows_inserted,
                    rows_attempted = EXCLUDED.rows_attempted,
                    status = EXCLUDED.status;
            """), {
                "fn": os.path.basename(json_path),
                "rows_inserted": result["rows_inserted"],
                "rows_attempted": result["rows_attempted"],
                "st": result["status"]
            })
    except Exception:
        logger.exception("⚠️ No se pudo registrar en etl_processed_files")

    return result

### Assistant
Bien — gracias por ejecutar A y B. Resumen corto y análisis inmediato, luego te entrego **el patch** (lista para aplicar) que solicitaste en la Opción A.

## 1) Resumen y diagnóstico (breve y concreto)
- En la ejecución dentro del DAG `peaks_raman_test` se detectaron **85** picos porque el DAG **llama** `save_peaks_to_db(..., prominence=10, tolerance=15)` (es decir, **se le pasó `prominence=10`**).
- En tus pruebas CLI (Opción A y B) **no** pasaste `prominence=10` (usaste los valores por defecto), por eso `inspect_peaks` devolvió **514** picos tanto en `data/.../WE-PI-CHINA-1.json` como en `ETL/Silver/.../WE-PI-CHINA-1.json`.
- Conclusión: la diferencia 85 vs 514 es **parátrica** (parámetros de detección), **no** un problema con raw vs cleaned (ambos muestran 514 cuando se usan los mismos parámetros).
- `rows_inserted = 0` porque todas las combinaciones únicas `(json_filename, shift_cm1, sensor_id)` ya existen en la tabla — la función hizo UPDATEs pero no se insertaron filas nuevas (por eso `Δ = 0`).

Si quieres reproducir exactamente lo del DAG desde CLI, ejecuta (dentro del contenedor `airflow`):

```bash
python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json', force=True, prominence=10, tolerance=15))
PY
```

---

## 2) Qué te entrego ahora (solicitud Option A)
Te preparo el **patch** para `ETL/Gold/save_peaks.py` que:

1. Añade `rows_updated` al `result` y lo calcula con SQL (para saber cuántas filas fueron actualizadas).
2. Añade/asegura columnas `rows_attempted`, `rows_updated`, `forced` en `etl_processed_files`.
3. Envía `forced` (boolean) al registrar el procesamiento.
4. Usa `pool_pre_ping=True` en `create_engine` para mayor robustez.
5. Mantiene la compatibilidad con tu comportamiento actual.

A continuación tienes el **diff** listo para aplicar con `git apply`. Léelo, aplícalo y luego te doy el comando de verificación.

---

## 3) Patch (diff) — aplicar con `git apply`

Guarda el siguiente contenido en un archivo `save_peaks.patch` en la raíz del repo y aplica:

```diff
*** Begin Patch
*** Update File: ETL/Gold/save_peaks.py
@@
-from typing import Dict, Any
-from sqlalchemy import create_engine, text
-from sqlalchemy.exc import SQLAlchemyError
+from typing import Dict, Any
+from sqlalchemy import create_engine, text
+from sqlalchemy.exc import SQLAlchemyError
@@
 CREATE_PROCESSED_SQL = """
 CREATE TABLE IF NOT EXISTS public.etl_processed_files (
     id SERIAL PRIMARY KEY,
     json_filename TEXT NOT NULL,
     processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
     rows_inserted INTEGER DEFAULT 0,
-    status TEXT,
-    rows_attempted INTEGER DEFAULT 0,
+    status TEXT,
+    rows_attempted INTEGER DEFAULT 0,
+    rows_updated INTEGER DEFAULT 0,
+    forced BOOLEAN DEFAULT FALSE,
     UNIQUE (json_filename)
 );
 """
 
 def ensure_processed_files_columns(engine):
     """Agrega columnas faltantes a etl_processed_files si no existen."""
     with engine.begin() as conn:
         existing_cols = {
             row[0]
             for row in conn.execute(text(
                 "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'"
             ))
         }
-        if "rows_attempted" not in existing_cols:
-            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
-            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")
+        # Añadir columnas faltantes de manera idempotente
+        if "rows_attempted" not in existing_cols:
+            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
+            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")
+        if "rows_updated" not in existing_cols:
+            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_updated INTEGER;"))
+            logger.info("🛠️ Columna rows_updated agregada a etl_processed_files.")
+        if "forced" not in existing_cols:
+            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN forced BOOLEAN DEFAULT FALSE;"))
+            logger.info("🛠️ Columna forced agregada a etl_processed_files.")
@@
 def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks",
-                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
+                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
@@
     result = {
         "file": os.path.basename(json_path),
         "rows_inserted": 0,
+        "rows_updated": 0,
         "rows_attempted": 0,
         "status": "failed",
         "error": None
     }
@@
-    engine = create_engine(conn_str)
+    # pool_pre_ping helps a recovered DB connection in container restarts
+    engine = create_engine(conn_str, pool_pre_ping=True)
@@
     try:
         with engine.begin() as conn:
             pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
             logger.info(f"📊 Total antes: {pre_total}")
 
             peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500)
 
             inserted_new = conn.execute(text(f"""
                 WITH new_rows AS (
                   INSERT INTO public.{table_name} 
                   (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at)
                   SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now()
                   FROM {staging_table} s
                   LEFT JOIN public.{table_name} r
                     ON r.json_filename = s.json_filename
                    AND r.shift_cm1 = s.shift_cm1
                    AND r.sensor_id = s.sensor_id
                   WHERE r.json_filename IS NULL
                   RETURNING 1
                 )
                 SELECT COUNT(*) FROM new_rows;
             """)).scalar()
 
-            conn.execute(text(f"""
-                UPDATE public.{table_name} t
-                SET intensity = s.intensity,
-                    peak_type = s.peak_type,
-                    sample_id = s.sample_id,
-                    detected_at = now()
-                FROM {staging_table} s
-                WHERE t.json_filename = s.json_filename
-                  AND t.shift_cm1 = s.shift_cm1
-                  AND t.sensor_id = s.sensor_id;
-            """))
+            # UPDATE but count how many rows actually changed (auditable)
+            updated_count = conn.execute(text(f"""
+                WITH updated AS (
+                  UPDATE public.{table_name} t
+                  SET intensity = s.intensity,
+                      peak_type = s.peak_type,
+                      sample_id = s.sample_id,
+                      detected_at = now()
+                  FROM {staging_table} s
+                  WHERE t.json_filename = s.json_filename
+                    AND t.shift_cm1 = s.shift_cm1
+                    AND t.sensor_id = s.sensor_id
+                    AND (
+                      t.intensity IS DISTINCT FROM s.intensity
+                      OR t.peak_type IS DISTINCT FROM s.peak_type
+                      OR t.sample_id IS DISTINCT FROM s.sample_id
+                    )
+                  RETURNING 1
+                )
+                SELECT COUNT(*) FROM updated;
+            """)).scalar()
 
             post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
             conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
 
-        delta = post_total - pre_total
-        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
-        result["rows_inserted"] = inserted_new or 0
+        delta = post_total - pre_total
+        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
+        result["rows_inserted"] = inserted_new or 0
+        result["rows_updated"] = int(updated_count or 0)
         result["status"] = "success"
 
     except Exception as e:
         result["error"] = f"Error en upsert: {e}"
         logger.exception(result["error"])
         return result
@@
     try:
         with engine.begin() as conn:
             conn.execute(text("""
-                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, status)
-                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :st)
-                ON CONFLICT (json_filename) DO UPDATE
-                SET processed_at = now(),
-                    rows_inserted = EXCLUDED.rows_inserted,
-                    rows_attempted = EXCLUDED.rows_attempted,
-                    status = EXCLUDED.status;
+                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, rows_updated, forced, status)
+                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :rows_updated, :forced, :st)
+                ON CONFLICT (json_filename) DO UPDATE
+                SET processed_at = now(),
+                    rows_inserted = EXCLUDED.rows_inserted,
+                    rows_attempted = EXCLUDED.rows_attempted,
+                    rows_updated = EXCLUDED.rows_updated,
+                    forced = EXCLUDED.forced,
+                    status = EXCLUDED.status;
             """), {
                 "fn": os.path.basename(json_path),
-                "rows_inserted": result["rows_inserted"],
-                "rows_attempted": result["rows_attempted"],
-                "st": result["status"]
+                "rows_inserted": result["rows_inserted"],
+                "rows_attempted": result["rows_attempted"],
+                "rows_updated": result.get("rows_updated", 0),
+                "forced": bool(force),
+                "st": result["status"]
             })
     except Exception:
         logger.exception("⚠️ No se pudo registrar en etl_processed_files")
 
     return result
*** End Patch
```

Aplicar:

```bash
# en la raíz del repo
git apply save_peaks.patch
git add ETL/Gold/save_peaks.py
git commit -m "feat(raman): add rows_updated and forced recording; pool_pre_ping; ensure processed columns"
```

---

## 4) Verificación post-patch (comandos)
1. Reinicia el contenedor de airflow si hace falta (para que el nuevo código se use por Airflow tasks):
```bash
docker-compose restart airflow
```

2. Prueba desde CLI (igual que antes) para confirmar `rows_updated` aparece en el `result` y en `etl_processed_files`:

```bash
docker-compose exec airflow bash -c "python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
PY"
```

3. Verifica en Postgres:
```bash
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, rows_inserted, rows_attempted, rows_updated, forced, status FROM etl_processed_files WHERE json_filename = 'WE-PI-CHINA-1.json';"
```

---

## 5) Recomendaciones operativas rápidas
- Decide y documenta **una única fuente de verdad de parámetros** de detección (por ejemplo, archivo YAML con `tolerance`, `prominence`, `height`) y que tanto ejecución manual como DAG lean esos parámetros — así evitarás discrepancias como la que vimos.
- Para pruebas, mantén `RAMAN_TEST_MAX_FILES=1` — buen enfoque.
- Si te interesa, puedo también:
  - Cambiar el DAG para **exponer** los parámetros del detector como `Variables` de Airflow o `op_kwargs` con defaults leíbles.
  - Añadir `logging` más detallado para cada ejecución (por ejemplo, dump de parámetros usados en cada run en `etl_processed_files`).

---

¿Aplico el **patch** ahora (te lo aplico y preparo el commit/PR)?  
Si sí, lo aplico y te doy los comandos para verificar (ya listados). Si prefieres, primero ejecuto el CLI con `prominence=10` para que veas la detección de 85 desde terminal (pero ya te mostré cómo hacerlo).

### Human
Mira los resultados
airflow@a47347198099:/opt/airflow/project$ ^C
airflow@a47347198099:/opt/airflow/project$ airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00
/opt/airflow/logs/scheduler/latest already exists as a dir/file. Skip creating symlink.
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
[2025-08-15T03:04:14.609+0000] {dagbag.py:588} INFO - Filling up the DagBag from /opt/airflow/dags
✅ Pipeline ETL Omicas configurado correctamente
🚀 ¡Listo para ejecutar el pipeline Omicas!
[2025-08-15T03:04:16.027+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=non-requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman_test __airflow_temporary_run_2025-08-15T03:04:16.004990+00:00__ [None]>
[2025-08-15T03:04:16.032+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman_test __airflow_temporary_run_2025-08-15T03:04:16.004990+00:00__ [None]>
[2025-08-15T03:04:16.033+0000] {taskinstance.py:2866} INFO - Starting attempt 0 of 2
[2025-08-15T03:04:16.033+0000] {taskinstance.py:2947} WARNING - cannot record queued_duration for task peaks_raman_test because previous state change time has not been saved
[2025-08-15T03:04:16.036+0000] {taskinstance.py:2889} INFO - Executing <Task(PythonOperator): peaks_raman_test> on 2025-08-15 00:00:00+00:00
[2025-08-15T03:04:16.159+0000] {taskinstance.py:3132} INFO - Exporting env vars: AIRFLOW_CTX_DAG_OWNER='omicas' AIRFLOW_CTX_DAG_ID='raman_pipeline' AIRFLOW_CTX_TASK_ID='peaks_raman_test' AIRFLOW_CTX_EXECUTION_DATE='2025-08-15T00:00:00+00:00' AIRFLOW_CTX_DAG_RUN_ID='__airflow_temporary_run_2025-08-15T03:04:16.004990+00:00__'
[2025-08-15T03:04:16.162+0000] {taskinstance.py:731} INFO - ::endgroup::
2025-08-15 03:04:16,173 [INFO] [TEST FORCE] Procesando 1 archivo(s) (max_files=1)
[2025-08-15T03:04:16.173+0000] {raman_pipeline.py:162} INFO - [TEST FORCE] Procesando 1 archivo(s) (max_files=1)
2025-08-15 03:04:16,174 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
[2025-08-15T03:04:16.174+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
2025-08-15 03:04:16,187 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:16.187+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
🔎 Detectados 85 picos en /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
[2025-08-15T03:04:16.202+0000] {utils.py:50} INFO - Parsed sensor_id=None sample_id=1 from filename 'WE-PI-CHINA-1.json'
2025-08-15 03:04:16,204 [INFO] 📊 Total antes: 2284
[2025-08-15T03:04:16.204+0000] {save_peaks.py:184} INFO - 📊 Total antes: 2284
2025-08-15 03:04:16,223 [INFO] 📈 Total después: 2284 (Δ 0)
[2025-08-15T03:04:16.223+0000] {save_peaks.py:230} INFO - 📈 Total después: 2284 (Δ 0)
2025-08-15 03:04:16,225 [INFO] [TEST FORCE] WE-PI-CHINA-1.json → inserted=0 updated=0 attempted=85 forced=True
[2025-08-15T03:04:16.225+0000] {raman_pipeline.py:177} INFO - [TEST FORCE] WE-PI-CHINA-1.json → inserted=0 updated=0 attempted=85 forced=True
[2025-08-15T03:04:16.226+0000] {python.py:240} INFO - Done. Returned value was: [{'file': 'WE-PI-CHINA-1.json', 'status': 'success', 'rows_attempted': 85, 'rows_inserted': 0, 'rows_updated': 0, 'forced': True, 'error': None}]
[2025-08-15T03:04:16.233+0000] {taskinstance.py:340} INFO - ::group::Post task execution logs
[2025-08-15T03:04:16.233+0000] {taskinstance.py:352} INFO - Marking task as SUCCESS. dag_id=raman_pipeline, task_id=peaks_raman_test, run_id=__airflow_temporary_run_2025-08-15T03:04:16.004990+00:00__, execution_date=20250815T000000, start_date=, end_date=20250815T030416
airflow@a47347198099:/opt/airflow/project$ 
airflow@a47347198099:/opt/airflow/project$ 
airflow@a47347198099:/opt/airflow/project$ 
airflow@a47347198099:/opt/airflow/project$ airflow tasks test raman_pipeline peaks_raman 2025-08-15T00:00:00
/opt/airflow/logs/scheduler/latest already exists as a dir/file. Skip creating symlink.
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
[2025-08-15T03:04:24.517+0000] {dagbag.py:588} INFO - Filling up the DagBag from /opt/airflow/dags
✅ Pipeline ETL Omicas configurado correctamente
🚀 ¡Listo para ejecutar el pipeline Omicas!
[2025-08-15T03:04:25.956+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=non-requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman __airflow_temporary_run_2025-08-15T03:04:25.934335+00:00__ [None]>
[2025-08-15T03:04:25.962+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman __airflow_temporary_run_2025-08-15T03:04:25.934335+00:00__ [None]>
[2025-08-15T03:04:25.962+0000] {taskinstance.py:2866} INFO - Starting attempt 0 of 2
[2025-08-15T03:04:25.962+0000] {taskinstance.py:2947} WARNING - cannot record queued_duration for task peaks_raman because previous state change time has not been saved
[2025-08-15T03:04:25.965+0000] {taskinstance.py:2889} INFO - Executing <Task(PythonOperator): peaks_raman> on 2025-08-15 00:00:00+00:00
[2025-08-15T03:04:26.089+0000] {taskinstance.py:3132} INFO - Exporting env vars: AIRFLOW_CTX_DAG_OWNER='omicas' AIRFLOW_CTX_DAG_ID='raman_pipeline' AIRFLOW_CTX_TASK_ID='peaks_raman' AIRFLOW_CTX_EXECUTION_DATE='2025-08-15T00:00:00+00:00' AIRFLOW_CTX_DAG_RUN_ID='__airflow_temporary_run_2025-08-15T03:04:25.934335+00:00__'
[2025-08-15T03:04:26.091+0000] {taskinstance.py:731} INFO - ::endgroup::
2025-08-15 03:04:26,106 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 2.json
[2025-08-15T03:04:26.106+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 2.json
2025-08-15 03:04:26,119 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.119+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,121 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.121+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,122 [INFO] [PROD] WE-PI-China-1-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.122+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-1-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,123 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 3.json
[2025-08-15T03:04:26.123+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 3.json
2025-08-15 03:04:26,134 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.134+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,136 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.136+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-1-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,136 [INFO] [PROD] WE-PI-China-1-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.136+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-1-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,137 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
[2025-08-15T03:04:26.137+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
2025-08-15 03:04:26,148 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.148+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,150 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.150+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,150 [INFO] [PROD] WE-PI-CHINA-1.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.150+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-1.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,151 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 2.json
[2025-08-15T03:04:26.151+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 2.json
2025-08-15 03:04:26,163 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.163+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,164 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.164+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,165 [INFO] [PROD] WE-PI-China-2-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.165+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-2-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,165 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 3.json
[2025-08-15T03:04:26.165+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 3.json
2025-08-15 03:04:26,177 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.177+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,179 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.179+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-2-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,179 [INFO] [PROD] WE-PI-China-2-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.179+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-2-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,180 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-2.json
[2025-08-15T03:04:26.180+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-2.json
2025-08-15 03:04:26,190 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.190+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,192 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.192+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,192 [INFO] [PROD] WE-PI-CHINA-2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.192+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,193 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 2.json
[2025-08-15T03:04:26.193+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 2.json
2025-08-15 03:04:26,205 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.205+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,206 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.206+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,207 [INFO] [PROD] WE-PI-China-3-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.207+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-3-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,208 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 3.json
[2025-08-15T03:04:26.208+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 3.json
2025-08-15 03:04:26,218 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.218+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,219 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.219+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-3-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,220 [INFO] [PROD] WE-PI-China-3-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.220+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-3-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,220 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-3.json
[2025-08-15T03:04:26.220+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-3.json
2025-08-15 03:04:26,232 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.232+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,234 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.234+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,234 [INFO] [PROD] WE-PI-CHINA-3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.234+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,235 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 2.json
[2025-08-15T03:04:26.235+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 2.json
2025-08-15 03:04:26,245 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.245+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,247 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.247+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,247 [INFO] [PROD] WE-PI-China-4-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.247+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-4-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,248 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 3.json
[2025-08-15T03:04:26.248+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 3.json
2025-08-15 03:04:26,258 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.258+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,259 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.259+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-4-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,260 [INFO] [PROD] WE-PI-China-4-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.260+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-4-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,261 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-4.json
[2025-08-15T03:04:26.261+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-4.json
2025-08-15 03:04:26,272 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.272+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,274 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-4.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.274+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-4.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,275 [INFO] [PROD] WE-PI-CHINA-4.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.275+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-4.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,275 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 2.json
[2025-08-15T03:04:26.275+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 2.json
2025-08-15 03:04:26,291 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.291+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,293 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.293+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,294 [INFO] [PROD] WE-PI-China-5-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.294+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-5-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,295 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 3.json
[2025-08-15T03:04:26.295+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 3.json
2025-08-15 03:04:26,311 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.311+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,313 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.313+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-5-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,314 [INFO] [PROD] WE-PI-China-5-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.314+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-5-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,314 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-5.json
[2025-08-15T03:04:26.314+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-5.json
2025-08-15 03:04:26,332 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.332+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,334 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-5.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.334+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-5.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,335 [INFO] [PROD] WE-PI-CHINA-5.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.335+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-5.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,336 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 2.json
[2025-08-15T03:04:26.336+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 2.json
2025-08-15 03:04:26,349 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.349+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,351 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.351+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,351 [INFO] [PROD] WE-PI-China-6-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.351+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-6-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,352 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 3.json
[2025-08-15T03:04:26.352+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 3.json
2025-08-15 03:04:26,365 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.365+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,367 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 3.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.367+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-6-sensor 3.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,368 [INFO] [PROD] WE-PI-China-6-sensor 3.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.368+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-6-sensor 3.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,369 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-6.json
[2025-08-15T03:04:26.369+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-6.json
2025-08-15 03:04:26,381 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.381+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,382 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-6.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.382+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-6.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,383 [INFO] [PROD] WE-PI-CHINA-6.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.383+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-CHINA-6.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,383 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7-sensor 2.json
[2025-08-15T03:04:26.383+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7-sensor 2.json
2025-08-15 03:04:26,396 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.396+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,398 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7-sensor 2.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.398+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7-sensor 2.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,398 [INFO] [PROD] WE-PI-China-7-sensor 2.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.398+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-7-sensor 2.json → inserted=0 updated=0 attempted=0
2025-08-15 03:04:26,399 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7.json
[2025-08-15T03:04:26.399+0000] {save_peaks.py:96} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7.json
2025-08-15 03:04:26,410 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T03:04:26.410+0000] {save_peaks.py:117} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
2025-08-15 03:04:26,412 [INFO] ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7.json ya procesado con éxito, sin cambios.
[2025-08-15T03:04:26.412+0000] {save_peaks.py:138} INFO - ⏭️ /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-China-7.json ya procesado con éxito, sin cambios.
2025-08-15 03:04:26,413 [INFO] [PROD] WE-PI-China-7.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.413+0000] {raman_pipeline.py:131} INFO - [PROD] WE-PI-China-7.json → inserted=0 updated=0 attempted=0
[2025-08-15T03:04:26.413+0000] {python.py:240} INFO - Done. Returned value was: [{'file': 'WE-PI-China-1-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-1-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-1.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-2-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-2-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-3-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-3-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-4-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-4-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-4.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-5-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-5-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-5.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-6-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-6-sensor 3.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-CHINA-6.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-7-sensor 2.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}, {'file': 'WE-PI-China-7.json', 'status': 'success', 'rows_attempted': 0, 'rows_inserted': 0, 'rows_updated': 0, 'error': None}]
[2025-08-15T03:04:26.421+0000] {taskinstance.py:340} INFO - ::group::Post task execution logs
[2025-08-15T03:04:26.422+0000] {taskinstance.py:352} INFO - Marking task as SUCCESS. dag_id=raman_pipeline, task_id=peaks_raman, run_id=__airflow_temporary_run_2025-08-15T03:04:25.934335+00:00__, execution_date=20250815T000000, start_date=, end_date=20250815T030426

docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, rows_inserted, rows_updated, rows_attempted, forced, status, processed_at FROM etl_processed_files ORDER BY processed_at DESC LIMIT 20;"
        json_filename        | rows_inserted | rows_updated | rows_attempted | forced | status  |         processed_at          
-----------------------------+---------------+--------------+----------------+--------+---------+-------------------------------
 WE-PI-CHINA-1.json          |             0 |            0 |             85 | t      | success | 2025-08-15 03:04:16.224451+00
 WE-PI-China-7.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:47.232346+00
 WE-PI-China-7-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:47.114701+00
 WE-PI-CHINA-6.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:47.011157+00
 WE-PI-China-6-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.922983+00
 WE-PI-China-6-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.823083+00
 WE-PI-CHINA-5.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.71764+00
 WE-PI-China-5-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.612676+00
 WE-PI-China-5-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.467047+00
 WE-PI-CHINA-4.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.36297+00
 WE-PI-China-4-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.261506+00
 WE-PI-China-4-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.175538+00
 WE-PI-CHINA-3.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:46.079132+00
 WE-PI-China-3-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.974273+00
 WE-PI-China-3-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.849343+00
 WE-PI-CHINA-2.json          |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.750579+00
 WE-PI-China-2-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.656483+00
 WE-PI-China-2-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.566099+00
 WE-PI-China-1-sensor 3.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.368656+00
 WE-PI-China-1-sensor 2.json |             0 |            0 |                | f      | success | 2025-08-13 22:49:45.272583+00
(20 rows)

Si quieres, aplico yo el cambio en el DAG (te doy el git diff) o te lo dejo para que reemplaces tú mismo. ¿Lo aplico ahora y ejecuto una prueba peaks_raman_test para confirmar el logging?
Pues en base a todos estos resultados, que consideras como lo mejor?

### Human

import sys, os, glob, time, logging
from datetime import datetime, timedelta

### Assistant
Muy buen trabajo con las pruebas — los resultados nos dejaron claro qué estaba pasando. Aquí te doy un diagnóstico ejecutivo y un plan recomendado, con cambios concretos (SQL + Python + DAG) que puedes aplicar de inmediato para que el pipeline sea fiable, auditable y predecible.

---

# Diagnóstico resumido (1 frase)
La diferencia de conteos (514 vs 85) fue causada por parámetros distintos de `inspect_peaks` (el DAG estaba usando `prominence=10`), no por limpieza del JSON; además ahora tienes `rows_updated` y `forced` registrados, pero la lógica de *skip* sólo mira `status="success"`, por lo que no distingue si el archivo fue procesado con los mismos parámetros o con otros distintos.

---

# Objetivo operativo
Evitar reprocesos accidentales y poder decidir automáticamente cuándo reprocesar:  
- Si el mismo archivo ya fue procesado **con los mismos parámetros**, saltarlo.  
- Si el archivo cambió (contenido) o los parámetros cambiaron, reprocesar.  
- Mantener trazabilidad de **parámetros usados**, **hash del archivo**, `rows_inserted` y `rows_updated`.

---

# Cambio recomendado (alto nivel)
1. Añadir columnas a `etl_processed_files`: `file_hash TEXT`, `detector_params JSONB` (o TEXT), `forced BOOLEAN` (ya lo tienes).  
2. Modificar `save_peaks_to_db` para:
   - Calcular `file_hash` (md5) del JSON.
   - Serializar `find_peaks_kwargs` usados (por ejemplo `{"tolerance":15,"prominence":10}`) y guardarlos.
   - **Skip** sólo si `status="success"` *AND* `file_hash` igual *AND* `detector_params` igual — así se evita saltar cuando cambian parámetros.
   - Registrar `rows_inserted`, `rows_updated`, `rows_attempted`, `forced`, `file_hash`, `detector_params` en `etl_processed_files`.
3. Exponer parámetros de detección como **Airflow Variables** (o DAG `op_kwargs`), de modo que ejecuciones manuales y DAG usen fuentes únicas de verdad.
4. Mantener la tarea `peaks_raman_test` para pruebas, pero con `max_files` pequeño. Para re-procesos masivos, tener una tarea aparte y manual (o protegida) que requiera aprobación.

---

# SQL de migración / alter table (ejecuta en Postgres)

```sql
-- agrega columnas si no existen
ALTER TABLE public.etl_processed_files
  ADD COLUMN IF NOT EXISTS file_hash TEXT,
  ADD COLUMN IF NOT EXISTS detector_params JSONB,
  ADD COLUMN IF NOT EXISTS forced BOOLEAN DEFAULT FALSE;
```

(Ya añadiste `rows_updated` y `forced` — esto completa la tabla.)

---

# Código (fragmentos) — cambios mínimos y seguros

### 1) Calcular hash del archivo (Python)
```python
import hashlib
def file_md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
```

### 2) Serializar parámetros
```python
import json
det_params = {"tolerance": tolerance, **find_peaks_kwargs}
det_params_json = json.dumps(det_params, sort_keys=True, ensure_ascii=False)
```

### 3) Skip lógico (reemplaza el bloque de "Skip" en `save_peaks_to_db`)
```python
file_hash = file_md5(json_path)
result_meta = {"file_hash": file_hash, "detector_params": det_params_json}

if not force:
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text("""
                SELECT status, file_hash, detector_params
                FROM public.etl_processed_files
                WHERE json_filename = :fn
                """), {"fn": os.path.basename(json_path)}
            ).fetchone()
        if row and row["status"] == "success" and row["file_hash"] == file_hash and (row["detector_params"] or "{}") == det_params_json:
            logger.info(f"⏭️ {json_path} ya procesado con mismos parámetros; skipping.")
            return {**result, "status": "success", "error": None}
    except Exception:
        logger.warning("⚠️ No se pudo comprobar etl_processed_files; procesando de todas formas.")
```

### 4) Registrar metadata en `etl_processed_files` (INSERT/UPDATE)
Ajusta la query final para incluir `file_hash` y `detector_params`:

```sql
INSERT INTO public.etl_processed_files 
(json_filename, processed_at, rows_inserted, rows_attempted, rows_updated, forced, status, file_hash, detector_params)
VALUES (:fn, now(), :rows_inserted, :rows_attempted, :rows_updated, :forced, :st, :file_hash, :detector_params::jsonb)
ON CONFLICT (json_filename) DO UPDATE SET
  processed_at = now(),
  rows_inserted = EXCLUDED.rows_inserted,
  rows_attempted = EXCLUDED.rows_attempted,
  rows_updated = EXCLUDED.rows_updated,
  forced = EXCLUDED.forced,
  status = EXCLUDED.status,
  file_hash = EXCLUDED.file_hash,
  detector_params = EXCLUDED.detector_params;
```

Y pasar parámetros desde Python:
```python
params = {
  "fn": os.path.basename(json_path),
  "rows_inserted": result["rows_inserted"],
  "rows_attempted": result["rows_attempted"],
  "rows_updated": result.get("rows_updated", 0),
  "forced": bool(force),
  "st": result["status"],
  "file_hash": file_hash,
  "detector_params": det_params_json,
}
conn.execute(text(SQL_ABOVE), params)
```

---

# DAG: exponer parámetros como Airflow Variables y pasarlos al task
En el DAG, añade al principio:

```python
from airflow.models import Variable
detector_defaults = Variable.get("raman_detector_params", default_var='{"tolerance":15,"prominence":10}')
import json
detector_params = json.loads(detector_defaults)
```

Luego en tus llamadas:

```python
res = save_peaks_to_db(js, **detector_params, force=False)
```

Si quieres cambiar parámetros, modificas la Variable en la UI y el DAG lo tomará en la próxima ejecución.

---

# Por qué esto es lo mejor (beneficios)
- **Evita reprocesos innecesarios** (ahorras CPU y I/O).
- **Traza exacta** de qué parámetros se usaron para cada archivo.
- **Permite re-procesar selectivamente**: sólo cuando el archivo cambió o la política de detección cambió.
- **Auditable**: `rows_inserted` + `rows_updated` + `file_hash` + `detector_params` te dan evidencia completa de qué ocurrió.
- **Operable y seguro**: re-procesos masivos quedan como acción explícita (por ejemplo una DAG admin-only o un botón en UI).

---

# Política para re-procesos que te propongo (sencilla, operativa)
1. Normal run: `force=False` (skip si mismo archivo + mismos params).  
2. Manual reprocess small: `peaks_raman_test` con `force=True` y `max_files=1..5`.  
3. Full reprocess (solo admin): DAG separado `raman_reprocess_all` que itera y usa `force=True` — antes de ejecutarlo hacer backup/ snapshot de DB o confirmar por PR.

---

# Pasos concretos que puedo aplicar ahora (elige una)
- **1) Aplico los cambios mínimos en `save_peaks.py` y genero el `git diff`** (incluye file_hash + detector_params + registro).  
- **2) Además edito el DAG para leer Airflow Variable `raman_detector_params` y pasarla a `save_peaks_to_db`**.  
- **3) Te doy el SQL de migración (ya incluido arriba) y el comando para ejecutarlo**.  
- **4) Después corro en tu contenedor la prueba `peaks_raman_test` con los nuevos metadatos y te muestro resultados.**

Dime qué combinación quieres (por ejemplo: “1 y 2 — aplícalas y prueba `peaks_raman_test`”), y lo implemento/de planto el patch y te doy los comandos exactos (commit + restart + test). Si prefieres hacerlo tú, te entrego el diff listo y los pasos.

### Assistant
Perfecto — gracias por pegar el DAG. Lo revisé y aquí tienes un diagnóstico claro, puntual y la recomendación práctica para dejar todo robusto sin perder nada del código original.

---

# 1) Estado actual del DAG que mostraste
Tu `Airflow/Dags/raman_pipeline.py` actual:

- Conserva el flujo original: `bronze_raman` → `silver_raman` → `gold_raman` → `peaks_raman` y la tarea de prueba `peaks_raman_test`.
- Tiene logging robusto (file + stream) y la función `log_error` que usabas.
- Las tareas `peaks_task` y `peaks_test_task` ya fueron actualizadas por mí para:
  - Llamar `save_peaks_to_db(..., tolerance=15, prominence=10)` (producción y test).
  - Registrar un resumen (`rows_inserted`, `rows_attempted`, y — tras tu patch — `rows_updated` y `forced`).
  - Devolver un resumen pequeño para XCom (evita XCom gigantes).

En resumen: **no falta la lógica esencial**; el DAG está funcional y contiene las mejoras de observabilidad que acordamos.

---

# 2) Qué pudo haberse "perdido" (por lo que comentaste) y por qué no es crítico
Posibles motivos de la sensación "me quitaste código":

- En versiones previas había impresiones/direct messages del módulo (p. ej. `✅ Pipeline ETL Omicas configurado correctamente`) que venías viendo en logs; en la versión que te propuse no incluí ese banner textual explícito. Eso es sólo superficial — no altera el DAG ni la lógica.
- Eliminé duplicados de imports y limpiezas menores (ej.: varias inserciones repetidas de `PROJECT_ROOT` en `sys.path`) para dejar el archivo más limpio. No se eliminó funcionalidad.
- Cambié la forma en que se retorna la información (resumen vs objetos completos) para evitar problemas con XCom y para facilitar logs; eso sí cambia la *forma* del retorno, pero no la *lógica* de procesamiento.

Conclusión: **no hay pérdida funcional** — las tareas ejecutan exactamente las funciones ETL que tenías. Lo único pendiente, y recomendable, es introducir trazabilidad de parámetros y hash de archivo (ver siguiente sección).

---

# 3) Problema operativo descubierto y por qué conviene arreglarlo
Actualmente el *skip* en `save_peaks_to_db` solo comprueba `status="success"` en `etl_processed_files`. Eso significa:

- Si antes procesaste el archivo con parámetros distintos (p. ej. sin `prominence=10`) y luego el DAG lo ejecuta con `prominence=10`, el sistema **puede** estar saltando ejecuciones (si `status=success` ya existía), o ejecutando cuando no correspondía — en tu caso encontramos que la diferencia 514 vs 85 fue por **parámetros distintos** (no por cleaned/raw).
- Para tener comportamiento determinístico debes **guardar** y **comparar**:
  - hash del archivo (para saber si el contenido cambió),
  - parámetros de detección usados (para saber si la ejecución fue con los mismos parámetros).

Esto permite decidir de forma segura “skip solo si mismo archivo y mismos parámetros”.

---

# 4) Recomendación concreta (lo que yo implementaría ahora)
Ordenada, mínima e incremental:

1. **Añadir en la tabla `etl_processed_files`** (si no está) las columnas:
   - `file_hash TEXT`
   - `detector_params JSONB` (o TEXT si prefieres evitar JSONB)
   (ya tienes `rows_updated` y `forced`).

2. **Modificar `save_peaks_to_db`** para:
   - calcular `file_hash = md5(json_file)`,
   - serializar `det_params = {"tolerance": ..., **find_peaks_kwargs}` a JSON string (ordenada),
   - cambiar la lógica `skip` a: `si existe status='success' Y file_hash igual Y detector_params igual -> skip`,
   - escribir `file_hash` y `detector_params` al registrar en `etl_processed_files`.

3. **Exponer parámetros por una única fuente**:
   - Crear Airflow Variable `raman_detector_params` con JSON `{"tolerance":15,"prominence":10}` y leerla en el DAG (evita divergencias entre CLI y DAG).

4. **Mantener task de prueba** como `peaks_raman_test` con `force=True` y `max_files=1` por defecto (como ya hiciste).

5. **(Opcional)** Añadir DAG admin-only para reprocess masivo y/o crear un flag que requiera confirmación.

---

# 5) Código listo para aplicar — mínimo, seguro y compatible

A. **SQL de migración** (ejecuta en Postgres una vez):

```sql
ALTER TABLE public.etl_processed_files
  ADD COLUMN IF NOT EXISTS file_hash TEXT,
  ADD COLUMN IF NOT EXISTS detector_params JSONB;
```

B. **Snippets para integrar** — tres cambios mínimos que entrego listos para copiar/pegar:

1. `file_md5` y serializar params — poner en `ETL/Gold/save_peaks.py` cerca del inicio:

```python
import hashlib
import json

def file_md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
```

2. Antes del bloque de skip en `save_peaks_to_db`, calcula hash y det_params:

```python
# preparar parámetros de detector que vamos a usar y un hash del archivo
det_params = {"tolerance": tolerance}
det_params.update({k: v for k, v in find_peaks_kwargs.items()})
det_params_json = json.dumps(det_params, sort_keys=True, ensure_ascii=False)
file_hash = file_md5(json_path)
```

3. Reemplazar la condición de skip por:

```python
# Skip: ya fue procesado con éxito y no requiere reprocesar sólo si
# status == success AND mismo file_hash AND mismos detector params
if not force:
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT status, file_hash, detector_params FROM public.etl_processed_files WHERE json_filename = :fn"),
                {"fn": os.path.basename(json_path)}
            ).fetchone()
            if row and row["status"] == "success":
                existing_hash = row["file_hash"]
                existing_params = row["detector_params"] or {}
                # existing_params puede venir como jsonb; convertir a str ordenada para comparar
                existing_params_json = json.dumps(existing_params, sort_keys=True, ensure_ascii=False) if existing_params else ""
                if existing_hash == file_hash and existing_params_json == det_params_json:
                    logger.info(f"⏭️ {json_path} ya procesado con éxito usando los mismos parámetros; skipping.")
                    return {**result, "status": "success", "error": None}
    except Exception:
        logger.warning("⚠️ No se pudo comprobar etl_processed_files; procesando de todas formas.")
```

4. Al insertar en `etl_processed_files` (final del `save_peaks_to_db`) añade `file_hash` y `detector_params` a la query (ya te mostré la query SQL exacta en el mensaje previo).

C. **DAG** — Leer Airflow Variable y pasar parámetros (reemplaza la llamada):

Al inicio del DAG, añade:

```python
from airflow.models import Variable
import json

# default detectors params (si Variable no existe)
_detector_defaults = Variable.get("raman_detector_params", default_var='{"tolerance":15,"prominence":10}')
try:
    detector_params = json.loads(_detector_defaults)
except Exception:
    detector_params = {"tolerance": 15, "prominence": 10}
```

Y en `peaks_task` / `peaks_test_task` sustituye las llamadas:

```python
res = save_peaks_to_db(js, **detector_params, force=False)   # producción
# y
res = save_peaks_to_db(js, **detector_params, force=True)    # test
```

---

# 6) ¿Qué recomiendo que hagamos ahora? (acción inmediata)
Yo aplicaría en este orden (seguro y reversable):

1. Ejecutar el `ALTER TABLE` en Postgres para agregar `file_hash` y `detector_params`.
2. Aplicar los cambios en `save_peaks.py` (añadir `file_md5`, serializar params, nuevo skip, escribir metadata).
3. Actualizar el DAG para leer `raman_detector_params` y pasarla a `save_peaks_to_db`.
4. Commit + restart Airflow.
5. Ejecutar `airflow tasks test raman_pipeline peaks_raman_test ...` (max_files=1) y verificar:
   - en logs: que aparece `file_hash` y `detector_params` en el insert (en `etl_processed_files`),
   - que el skip funciona si vuelves a correr sin cambios,
   - que si modificas params en la Variable y vuelves a ejecutar, no se salta (porque params cambiaron).

Puedo generar **el patch completo** (diff) para `save_peaks.py` + `raman_pipeline.py` y el SQL, listo para `git apply`. ¿Lo quieres ahora? Si sí, lo creo y te lo doy listo para aplicar. Si prefieres aplicarlo tú, te paso los archivos completos listos para pegar.

---

Dime si quieres que **aplique** el cambio ahora (te doy el `git diff`/patch) o si prefieres que **te lo deje listo para pegar** (ambos formatos están OK). Yo lo preparo y te doy los comandos para verificar.

### Human
Opcion A
airflow@a47347198099:/opt/airflow/project/data$ python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
PY
2025-08-15 02:50:20,709 [INFO] 🔄 Procesando picos de: /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json
2025-08-15 02:50:20,745 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
🔎 Detectados 514 picos en /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json
2025-08-15 02:50:20,762 [INFO] 📊 Total antes: 2284
2025-08-15 02:50:20,797 [INFO] 📈 Total después: 2284 (Δ 0)
{'file': 'WE-PI-CHINA-1.json', 'rows_inserted': 0, 'rows_attempted': 514, 'status': 'success', 'error': None}

Opcion B
airflow@a47347198099:/opt/airflow$ python - <<'PY'
from ETL.Silver.inspect_peaks import inspect_peaks
p_raw, _ = inspect_peaks('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', plot=False)
p_clean, _ = inspect_peaks('/opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json', plot=False)
print("raw:", None if p_raw is None else len(p_raw))
print("clean:", None if p_clean is None else len(p_clean))
PY
🔎 Detectados 514 picos en /opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json
🔎 Detectados 514 picos en /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
raw: 514
clean: 514

Mira los resultados de A y B

### Assistant
Hecho. Abajo tienes el **archivo final completo** `ETL/Gold/save_peaks.py` con las modificaciones solicitadas integradas (conteo de `rows_updated`, columna `forced`, `pool_pre_ping=True`, y aseguramiento idempotente de columnas). Reemplaza el archivo actual por este contenido y haz commit.

```python
# ETL/Gold/save_peaks.py
import os
import logging
import traceback
import pandas as pd
import numpy as np
from typing import Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from ETL.Silver.inspect_peaks import inspect_peaks
from scripts.utils import parse_ids_from_filename

load_dotenv()

# --- Configuración de logs ---
LOG_DIR = os.getenv("RAMAN_LOG_DIR", "/opt/airflow/project/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "save_peaks.log")

logger = logging.getLogger("save_peaks")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    logger.addHandler(fh)

# --- SQL para asegurar la tabla raman_peaks ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.raman_peaks (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    shift_cm1 DOUBLE PRECISION NOT NULL,
    intensity DOUBLE PRECISION NOT NULL,
    peak_type VARCHAR(50) NOT NULL,
    sample_id INTEGER DEFAULT NULL,
    sensor_id INTEGER NOT NULL DEFAULT -1,
    technique TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (json_filename, shift_cm1, sensor_id)
);
"""

# --- SQL para asegurar la tabla de tracking processed files ---
CREATE_PROCESSED_SQL = """
CREATE TABLE IF NOT EXISTS public.etl_processed_files (
    id SERIAL PRIMARY KEY,
    json_filename TEXT NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    rows_inserted INTEGER DEFAULT 0,
    status TEXT,
    rows_attempted INTEGER DEFAULT 0,
    rows_updated INTEGER DEFAULT 0,
    forced BOOLEAN DEFAULT FALSE,
    UNIQUE (json_filename)
);
"""

def ensure_processed_files_columns(engine):
    """Agrega columnas faltantes a etl_processed_files si no existen (idempotente)."""
    with engine.begin() as conn:
        existing_cols = {
            row[0]
            for row in conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='etl_processed_files'"
            ))
        }
        if "rows_attempted" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_attempted INTEGER;"))
            logger.info("🛠️ Columna rows_attempted agregada a etl_processed_files.")
        if "rows_updated" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN rows_updated INTEGER DEFAULT 0;"))
            logger.info("🛠️ Columna rows_updated agregada a etl_processed_files.")
        if "forced" not in existing_cols:
            conn.execute(text("ALTER TABLE public.etl_processed_files ADD COLUMN forced BOOLEAN DEFAULT FALSE;"))
            logger.info("🛠️ Columna forced agregada a etl_processed_files.")

def save_peaks_to_db(json_path: str, table_name: str = "raman_peaks",
                     tolerance: float = 15, force: bool = False, **find_peaks_kwargs) -> Dict[str, Any]:
    """
    Procesa un archivo JSON de Raman, detecta picos y los inserta/actualiza en Postgres.
    Retorna un dict con estadísticas para Airflow/XCom.
    """
    result = {
        "file": os.path.basename(json_path),
        "rows_inserted": 0,
        "rows_updated": 0,
        "rows_attempted": 0,
        "status": "failed",
        "error": None
    }

    logger.info(f"🔄 Procesando picos de: {json_path}")

    conn_str = os.getenv("GOLD_DB_CONN") or os.getenv("SQL_ALCHEMY_CONN") or os.getenv("POSTGRES_URL")
    if not conn_str:
        error_msg = (
            "❌ La variable GOLD_DB_CONN/SQL_ALCHEMY_CONN/POSTGRES_URL no está configurada. "
            "Agrega la variable en tu .env / docker-compose.yml."
        )
        logger.critical(error_msg)
        result["error"] = error_msg
        return result

    # pool_pre_ping ayuda a recuperar conexiones cuando Postgres se recicla
    engine = create_engine(conn_str, pool_pre_ping=True)

    # 1️⃣ Asegurar tablas (raman_peaks + etl_processed_files)
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_TABLE_SQL))
            conn.execute(text(CREATE_PROCESSED_SQL))
        ensure_processed_files_columns(engine)
        logger.info(f"📋 Tablas aseguradas: public.{table_name}, public.etl_processed_files")
    except SQLAlchemyError as e:
        error_msg = f"Error creando tablas: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result
    except Exception:
        error_msg = f"Error inesperado creando tablas: {traceback.format_exc()}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    # 2️⃣ Skip: si ya fue procesado con éxito y no requiere reprocesar (no es force)
    if not force:
        try:
            with engine.connect() as conn:
                existing_status = conn.execute(
                    text("SELECT status FROM public.etl_processed_files WHERE json_filename = :fn"),
                    {"fn": os.path.basename(json_path)}
                ).scalar()
                if existing_status == "success":
                    logger.info(f"⏭️ {json_path} ya procesado con éxito, sin cambios.")
                    return {**result, "status": "success", "error": None}
        except Exception:
            logger.warning("⚠️ No se pudo comprobar etl_processed_files, procesando de todas formas.")

    # 3️⃣ Inspección de picos
    try:
        peaks_df, key_matches = inspect_peaks(json_path, plot=False, **find_peaks_kwargs)
    except Exception as e:
        error_msg = f"❌ Error inspeccionando picos: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        return result

    if peaks_df is None or peaks_df.empty:
        logger.warning(f"⚠️ No se detectaron picos en {json_path}")
        return {**result, "status": "no_peaks"}

    # Normalizar columnas
    if "shift_cm-1" in peaks_df.columns:
        peaks_df = peaks_df.rename(columns={"shift_cm-1": "shift_cm1"})
    peaks_df["json_filename"] = os.path.basename(json_path)
    if "sensor_id" not in peaks_df.columns:
        peaks_df["sensor_id"] = -1
    if "sample_id" not in peaks_df.columns:
        peaks_df["sample_id"] = None
    if "technique" not in peaks_df.columns:
        peaks_df["technique"] = None
    if "peak_type" not in peaks_df.columns:
        peaks_df["peak_type"] = "Other"

    # Parsear IDs desde filename
    sensor_val, sample_val = parse_ids_from_filename(json_path)
    if sensor_val is not None:
        peaks_df["sensor_id"] = int(sensor_val)
    if sample_val is not None:
        peaks_df["sample_id"] = int(sample_val)

    # 4️⃣ Upsert determinista
    staging_table = f"{table_name}_staging"
    rows_to_process = len(peaks_df)
    result["rows_attempted"] = rows_to_process

    try:
        with engine.begin() as conn:
            pre_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            logger.info(f"📊 Total antes: {pre_total}")

            peaks_df.to_sql(staging_table, conn, if_exists="replace", index=False, chunksize=500)

            inserted_new = conn.execute(text(f"""
                WITH new_rows AS (
                  INSERT INTO public.{table_name} 
                  (json_filename, shift_cm1, intensity, peak_type, sample_id, sensor_id, technique, detected_at)
                  SELECT s.json_filename, s.shift_cm1, s.intensity, s.peak_type, s.sample_id, s.sensor_id, s.technique, now()
                  FROM {staging_table} s
                  LEFT JOIN public.{table_name} r
                    ON r.json_filename = s.json_filename
                   AND r.shift_cm1 = s.shift_cm1
                   AND r.sensor_id = s.sensor_id
                  WHERE r.json_filename IS NULL
                  RETURNING 1
                )
                SELECT COUNT(*) FROM new_rows;
            """)).scalar()

            # UPDATE pero contando realmente cuántas filas cambiaron (auditable)
            updated_count = conn.execute(text(f"""
                WITH updated AS (
                  UPDATE public.{table_name} t
                  SET intensity = s.intensity,
                      peak_type = s.peak_type,
                      sample_id = s.sample_id,
                      detected_at = now()
                  FROM {staging_table} s
                  WHERE t.json_filename = s.json_filename
                    AND t.shift_cm1 = s.shift_cm1
                    AND t.sensor_id = s.sensor_id
                    AND (
                      t.intensity IS DISTINCT FROM s.intensity
                      OR t.peak_type IS DISTINCT FROM s.peak_type
                      OR t.sample_id IS DISTINCT FROM s.sample_id
                    )
                  RETURNING 1
                )
                SELECT COUNT(*) FROM updated;
            """)).scalar()

            post_total = conn.execute(text(f"SELECT COUNT(*) FROM public.{table_name}")).scalar()
            conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))

        delta = post_total - pre_total
        logger.info(f"📈 Total después: {post_total} (Δ {delta})")
        result["rows_inserted"] = int(inserted_new or 0)
        result["rows_updated"] = int(updated_count or 0)
        result["status"] = "success"

    except Exception as e:
        result["error"] = f"Error en upsert: {e}"
        logger.exception(result["error"])
        return result

    # 5️⃣ Registrar archivo procesado
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO public.etl_processed_files (json_filename, processed_at, rows_inserted, rows_attempted, rows_updated, forced, status)
                VALUES (:fn, now(), :rows_inserted, :rows_attempted, :rows_updated, :forced, :st)
                ON CONFLICT (json_filename) DO UPDATE
                SET processed_at = now(),
                    rows_inserted = EXCLUDED.rows_inserted,
                    rows_attempted = EXCLUDED.rows_attempted,
                    rows_updated = EXCLUDED.rows_updated,
                    forced = EXCLUDED.forced,
                    status = EXCLUDED.status;
            """), {
                "fn": os.path.basename(json_path),
                "rows_inserted": result["rows_inserted"],
                "rows_attempted": result["rows_attempted"],
                "rows_updated": result.get("rows_updated", 0),
                "forced": bool(force),
                "st": result["status"]
            })
    except Exception:
        logger.exception("⚠️ No se pudo registrar en etl_processed_files")

    return result
```

### Pasos recomendados inmediatamente después de reemplazar el archivo
1. Reemplaza el archivo y haz commit:
```bash
git add ETL/Gold/save_peaks.py
git commit -m "feat(raman): añadir rows_updated y forced; pool_pre_ping; asegurar columnas en etl_processed_files"
```
2. Reinicia Airflow para que use el nuevo código:
```bash
docker-compose restart airflow
```
3. Verifica ejecutando un test rápido (CLI):
```bash
docker-compose exec airflow bash -c "python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
PY"
```
4. Comprueba en Postgres la fila en `etl_processed_files`:
```bash
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, rows_inserted, rows_attempted, rows_updated, forced, status FROM etl_processed_files WHERE json_filename = 'WE-PI-CHINA-1.json';"
```

Si quieres, aplico también el cambio equivalente en el DAG para que registre en logs los valores `rows_updated` y `forced` (opcional). ¿Lo hago ahora?

### Assistant
Perfecto — gracias por las salidas, son muy útiles. Resumen, diagnóstico y siguientes pasos concretos (todo claro y accionable).

---

# 1) Resumen breve de lo que pasó (estado actual)
- La tarea `peaks_raman_test` se ejecutó correctamente desde Airflow y **marcó SUCCESS**.  
- Logs clave:
  - Procesó **1 archivo** (por diseño: `RAMAN_TEST_MAX_FILES=1`).
  - `inspect_peaks` detectó **85 picos** en `/opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json`.
  - Antes en la tabla `raman_peaks` había **2284** filas en total; después seguía **2284** (Δ 0).
  - En la vista por archivo: `WE-PI-CHINA-1.json` aparece con **514** filas en DB.
  - En `etl_processed_files` el registro quedó con `rows_attempted = 85`, `rows_inserted = 0`, `status = success`.

---

# 2) Diagnóstico — por qué `attempted=85` vs `514` en la tabla
Hay **dos causas posibles (y compatibles)** para la diferencia entre 85 y 514:

1. **Archivo / origen distinto**  
   - En la ejecución previa que insertó 429 (y mostró 514 rows para ese archivo) probaste con el JSON desde `data/Raman_files/json/WE-PI-CHINA-1.json` (probablemente *raw*). Ahora el DAG está procesando el archivo en `ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json` (archivo *cleaned*). Es muy plausible que el *cleaning* cambie la forma del espectro y reduzca el número de picos detectados (514 → 85).

2. **Parámetros de detección distintos**  
   - En el DAG llamaste `save_peaks_to_db(..., prominence=10)` (y `tolerance=15`), lo cual afecta la detección; la ejecución previa que dio 514 picos **no** usó `prominence=10` (o usó otros parámetros). Diferentes `find_peaks_kwargs` producen distinto `rows_attempted`.

La razón por la que `rows_inserted = 0` y `Δ = 0` es porque los 85 picos detectados ya existían en la tabla con la clave única `(json_filename, shift_cm1, sensor_id)` — por eso no se insertaron nuevas filas. El `UPDATE` sí se ejecutó, pero no hubo nuevas filas que añadir (y el código actual **no** devuelve cuántas filas se actualizaron).

---

# 3) Acciones recomendadas (elige una o varias — incluyo comandos exactos)

## Opción A — Reproducir exactamente lo que generó 514 (diagnóstico rápido)
Ejecuta `save_peaks_to_db` desde CLI dentro del contenedor Airflow usando **exactamente** el archivo y los parámetros que usaste antes. Esto confirmará cuál combinación produjo 514.

```bash
docker-compose exec airflow bash

# Ejecuta sobre el archivo en /opt/airflow/project/data (raw)
python - <<'PY'
from ETL.Gold.save_peaks import save_peaks_to_db
print(save_peaks_to_db('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', force=True))
PY
```

Si ese comando da `rows_attempted=514` entonces confirmamos que el origen (raw vs cleaned) es la causa.

---

## Opción B — Comparar detección entre raw y cleaned (rápida inspección)
Mira cuántos picos detecta `inspect_peaks` en ambos archivos:

```bash
docker-compose exec airflow bash

python - <<'PY'
from ETL.Silver.inspect_peaks import inspect_peaks
p_raw, _ = inspect_peaks('/opt/airflow/project/data/Raman_files/json/WE-PI-CHINA-1.json', plot=False)
p_clean, _ = inspect_peaks('/opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json', plot=False)
print("raw:", None if p_raw is None else len(p_raw))
print("clean:", None if p_clean is None else len(p_clean))
PY
```

Esto te mostrará si el *clean* redujo el conteo.

---

## Opción C — Ejecutar la tarea de prueba sobre el archivo raw desde el DAG
Si quieres probar la ruta Airflow → save_peaks sobre el archivo *raw* (sin modificar código), puedes temporalmente cambiar `peaks_raman_test` para leer de `data/Raman_files/json` en lugar del folder `ETL/Silver/...` o ejecutar la función `save_peaks_to_db` directamente con ese path (similar a Opción A).

---

## Opción D — Si quieres que la prueba reescriba/actualice todo (forzar re-calculo y ver diferencias)
Aumenta `RAMAN_TEST_MAX_FILES` para procesar más o todos los archivos (cuidado con recursos):

```bash
# en host o .env para docker-compose
export RAMAN_TEST_MAX_FILES=0   # si implementas 0 -> significa "todos"; ahora el DAG toma int(), decidirás convención
# reinicia airflow para que vea la var
docker-compose restart airflow
```

(o modifica `op_kwargs` en DAG para `max_files = <n>`).

---

# 4) Mejoras sugeridas al código (recomendadas — puedo aplicarlas si confirmas)
Para observabilidad y trazabilidad es conveniente:

1. **Registrar cuántas filas se *actualizaron*** (ahora solo recoges `rows_inserted`).  
   - Propongo capturar `rows_updated` y devolverlo en `result`. También almacenar `rows_updated` en `etl_processed_files`.

2. **Registrar si la ejecución fue `force`** en `etl_processed_files` (columna `forced BOOLEAN`), para histórico.

3. **Hacer el staging table temporal o usar schema con prefijo para evitar colisiones** cuando haya concurrencia.

4. **Añadir `pool_pre_ping=True` al `create_engine`** para mayor robustez de conexión.

### Ejemplo de cambio mínimo (insert + update counts)
Puedo darte el patch exacto, pero aquí te dejo la idea del SQL para contar actualizaciones:

```sql
-- inserted_new (ya lo haces con RETURNING)
WITH new_rows AS (
  INSERT INTO public.raman_peaks (...)
  SELECT ... FROM staging s
  LEFT JOIN public.raman_peaks r ...
  WHERE r.json_filename IS NULL
  RETURNING 1
)
SELECT COUNT(*) FROM new_rows;
```

```sql
-- updated_count
WITH updated AS (
  UPDATE public.raman_peaks t
  SET intensity = s.intensity,
      peak_type = s.peak_type,
      sample_id = s.sample_id,
      detected_at = now()
  FROM staging s
  WHERE t.json_filename = s.json_filename
    AND t.shift_cm1 = s.shift_cm1
    AND t.sensor_id = s.sensor_id
    AND (
      t.intensity IS DISTINCT FROM s.intensity
      OR t.peak_type IS DISTINCT FROM s.peak_type
      OR t.sample_id IS DISTINCT FROM s.sample_id
    )
  RETURNING 1
)
SELECT COUNT(*) FROM updated;
```

Y luego en Python:

```python
result["rows_inserted"] = inserted_new or 0
result["rows_updated"] = updated_count or 0
```

Además habría que `ALTER TABLE etl_processed_files ADD COLUMN rows_updated INTEGER;` (y opcionalmente `forced BOOLEAN`).

Si quieres, preparo el **patch completo** (diff) para `save_peaks.py` que:
- Añade `rows_updated`.
- Asegura la columna en `ensure_processed_files_columns`.
- Añade `pool_pre_ping=True` en `create_engine`.
- (Opcional) añade `forced` boolean en `etl_processed_files`.

Dime si lo aplico y te doy el diff y el comando `git apply`.

---

# 5) Recomendación inmediata y paso siguiente que yo haría ahora
1. Ejecutar la **Opción B** (comparar `inspect_peaks` en raw vs clean) para confirmar por qué hay 514 vs 85.  
2. Si confirmamos que el cleaned redujo la detección y eso no es deseado, revisar la función `clean_data` y parámetros de `inspect_peaks` (`prominence`, `tolerance`, `height`, etc.).  
3. Implementar la mejora para **contar rows_updated** — así las ejecuciones `force=True` quedarán totalmente auditables.

¿Quieres que:
- A) Te prepare el **patch automático** para `save_peaks.py` (añadir `rows_updated`, `forced` y `pool_pre_ping`) listo para `git apply`?  
- B) Primero corro yo (te doy los comandos) la comparación raw vs clean para confirmarlo y luego procedemos al patch?  

Elige A o B (o ambas), y procedo inmediatamente con el diff o los comandos listos.

### Human
Estas fueron las salidas

docker-compose exec airflow bash
airflow@a47347198099:/opt/airflow$ airflow dags list | grep raman_pipeline
/opt/airflow/logs/scheduler/latest already exists as a dir/file. Skip creating symlink.
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
raman_pipeline  | /opt/airflow/dags/raman_pipeline.py  | omicas  | False    
airflow@a47347198099:/opt/airflow$ 
airflow@a47347198099:/opt/airflow$ 
airflow@a47347198099:/opt/airflow$ airflow tasks list raman_pipeline
/opt/airflow/logs/scheduler/latest already exists as a dir/file. Skip creating symlink.
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
✅ Pipeline ETL Omicas configurado correctamente
🚀 ¡Listo para ejecutar el pipeline Omicas!
bronze_raman
gold_raman
peaks_raman
peaks_raman_test
silver_raman
airflow@a47347198099:/opt/airflow$ 
airflow@a47347198099:/opt/airflow$ 
airflow@a47347198099:/opt/airflow$ airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00
/opt/airflow/logs/scheduler/latest already exists as a dir/file. Skip creating symlink.
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
[2025-08-15T02:46:35.756+0000] {dagbag.py:588} INFO - Filling up the DagBag from /opt/airflow/dags
✅ Pipeline ETL Omicas configurado correctamente
🚀 ¡Listo para ejecutar el pipeline Omicas!
[2025-08-15T02:46:37.251+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=non-requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman_test __airflow_temporary_run_2025-08-15T02:46:37.213202+00:00__ [None]>
[2025-08-15T02:46:37.258+0000] {taskinstance.py:2613} INFO - Dependencies all met for dep_context=requeueable deps ti=<TaskInstance: raman_pipeline.peaks_raman_test __airflow_temporary_run_2025-08-15T02:46:37.213202+00:00__ [None]>
[2025-08-15T02:46:37.259+0000] {taskinstance.py:2866} INFO - Starting attempt 0 of 2
[2025-08-15T02:46:37.259+0000] {taskinstance.py:2947} WARNING - cannot record queued_duration for task peaks_raman_test because previous state change time has not been saved
[2025-08-15T02:46:37.261+0000] {taskinstance.py:2889} INFO - Executing <Task(PythonOperator): peaks_raman_test> on 2025-08-15 00:00:00+00:00
[2025-08-15T02:46:37.452+0000] {taskinstance.py:3132} INFO - Exporting env vars: AIRFLOW_CTX_DAG_OWNER='omicas' AIRFLOW_CTX_DAG_ID='raman_pipeline' AIRFLOW_CTX_TASK_ID='peaks_raman_test' AIRFLOW_CTX_EXECUTION_DATE='2025-08-15T00:00:00+00:00' AIRFLOW_CTX_DAG_RUN_ID='__airflow_temporary_run_2025-08-15T02:46:37.213202+00:00__'
[2025-08-15T02:46:37.457+0000] {taskinstance.py:731} INFO - ::endgroup::
2025-08-15 02:46:37,497 [INFO] [TEST FORCE] Procesando 1 archivo(s) (max_files=1)
[2025-08-15T02:46:37.497+0000] {raman_pipeline.py:150} INFO - [TEST FORCE] Procesando 1 archivo(s) (max_files=1)
2025-08-15 02:46:37,498 [INFO] 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
[2025-08-15T02:46:37.498+0000] {save_peaks.py:87} INFO - 🔄 Procesando picos de: /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
2025-08-15 02:46:37,520 [INFO] 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
[2025-08-15T02:46:37.520+0000] {save_peaks.py:107} INFO - 📋 Tablas aseguradas: public.raman_peaks, public.etl_processed_files
🔎 Detectados 85 picos en /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json
[2025-08-15T02:46:37.545+0000] {utils.py:50} INFO - Parsed sensor_id=None sample_id=1 from filename 'WE-PI-CHINA-1.json'
2025-08-15 02:46:37,549 [INFO] 📊 Total antes: 2284
[2025-08-15T02:46:37.549+0000] {save_peaks.py:176} INFO - 📊 Total antes: 2284
2025-08-15 02:46:37,580 [INFO] 📈 Total después: 2284 (Δ 0)
[2025-08-15T02:46:37.580+0000] {save_peaks.py:212} INFO - 📈 Total después: 2284 (Δ 0)
2025-08-15 02:46:37,583 [INFO] [TEST FORCE] save_peaks success for /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json: inserted=0 attempted=85
[2025-08-15T02:46:37.583+0000] {raman_pipeline.py:162} INFO - [TEST FORCE] save_peaks success for /opt/airflow/project/ETL/Silver/raman_jsons_clean/WE-PI-CHINA-1.json: inserted=0 attempted=85
[2025-08-15T02:46:37.584+0000] {python.py:240} INFO - Done. Returned value was: [{'file': 'WE-PI-CHINA-1.json', 'rows_inserted': 0, 'rows_attempted': 85, 'status': 'success', 'error': None}]
[2025-08-15T02:46:37.592+0000] {taskinstance.py:340} INFO - ::group::Post task execution logs
[2025-08-15T02:46:37.593+0000] {taskinstance.py:352} INFO - Marking task as SUCCESS. dag_id=raman_pipeline, task_id=peaks_raman_test, run_id=__airflow_temporary_run_2025-08-15T02:46:37.213202+00:00__, execution_date=20250815T000000, start_date=, end_date=20250815T024637

docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, COUNT(*) FROM raman_peaks GROUP BY json_filename ORDER BY json_filename LIMIT 10;"
        json_filename        | count 
-----------------------------+-------
 WE-PI-CHINA-1.json          |   514
 WE-PI-China-1-sensor 2.json |    96
 WE-PI-China-1-sensor 3.json |    89
 WE-PI-CHINA-2.json          |   102
 WE-PI-China-2-sensor 2.json |    98
 WE-PI-China-2-sensor 3.json |    83
 WE-PI-CHINA-3.json          |    96
 WE-PI-China-3-sensor 2.json |   106
 WE-PI-China-3-sensor 3.json |    86
 WE-PI-CHINA-4.json          |    88
(10 rows)

docker-compose exec postgres psql -U omicas -d omicas -c "SELECT * FROM etl_processed_files WHERE json_filename = 'WE-PI-CHINA-1.json';"
 id |   json_filename    |         processed_at          | rows_inserted | status  | rows_attempted 
----+--------------------+-------------------------------+---------------+---------+----------------
  3 | WE-PI-CHINA-1.json | 2025-08-15 02:46:37.581672+00 |             0 | success |             85
(1 row)

### Assistant
Perfecto — gracias por el código. Procedo y te entrego **la versión lista para reemplazar** de `Airflow/Dags/raman_pipeline.py` que:

- Mantiene tu flujo de producción (bronze → silver → gold → peaks_raman).
- Añade una **tarea temporal de prueba** `peaks_raman_test` que **forza** `save_peaks_to_db(..., force=True)`.
- Por seguridad, la tarea de prueba procesa **por defecto solamente 1 archivo** (puedes ajustar esto con la variable de entorno `RAMAN_TEST_MAX_FILES` o con `op_kwargs` en el DAG).
- Incluye logging consistente, manejo de errores y retorno de resultados para XCom.

Copia/pegá el archivo siguiente en `Airflow/Dags/raman_pipeline.py` (reemplaza el actual). Luego te doy los comandos exactos para ejecutar la prueba y cómo revertir.

---

# Nuevo `Airflow/Dags/raman_pipeline.py` (reemplazar archivo actual)

```python
# Airflow/Dags/raman_pipeline.py
import sys
import os
import glob
import logging
from datetime import datetime, timedelta

# Asegurar PATH del proyecto para imports relativos
PROJECT_ROOT = "/opt/airflow/project"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from airflow import DAG
from airflow.operators.python import PythonOperator

# ETL functions (as en tu repo)
from ETL.Bronze.extract_raman import extract_raman
from ETL.Silver.clean_data import clean_data
from ETL.Gold.load_to_postgres import load_to_postgres
from ETL.Gold.save_peaks import save_peaks_to_db

# ===== Configuración de logging del DAG =====
log_file_path = "/opt/airflow/logs/raman_pipeline.log"
error_log_path = "/opt/airflow/logs/raman_pipeline_errors.log"

logger = logging.getLogger("raman_pipeline")
logger.setLevel(logging.INFO)

# Evitar duplicar handlers al recargar el DAG
if not logger.handlers:
    # File handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # Stream handler (capturado por Airflow)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)

def log_error(msg: str):
    try:
        with open(error_log_path, "a") as f:
            f.write(f"{datetime.now()} - {msg}\n")
    except Exception:
        logger.exception("No se pudo escribir en error_log_path")
    logger.error(msg)

# ===== Default args =====
default_args = {
    "owner": "omicas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Variable de entorno que controla cuantos archivos procesar en la prueba (por defecto 1)
TEST_MAX_FILES = int(os.getenv("RAMAN_TEST_MAX_FILES", "1"))

with DAG(
    dag_id="raman_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    # -------------------------
    # 1) BRONZE
    # -------------------------
    t_bronze = PythonOperator(
        task_id="bronze_raman",
        python_callable=extract_raman,
        op_kwargs={"raw_dir": "/opt/airflow/project/data/Raman_files"},
    )

    # -------------------------
    # 2) SILVER
    # -------------------------
    def silver_task(**_):
        bronze_dir = "/opt/airflow/project/data/Raman_files/json"
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        os.makedirs(silver_dir, exist_ok=True)
        for js in glob.glob(f"{bronze_dir}/*.json"):
            out = os.path.join(silver_dir, os.path.basename(js))
            clean_data(js, out)

    t_silver = PythonOperator(
        task_id="silver_raman",
        python_callable=silver_task,
    )

    # -------------------------
    # 3) GOLD: Espectros completos (producción)
    # -------------------------
    def gold_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        for js in glob.glob(f"{silver_dir}/*.json"):
            load_to_postgres(js, table_name="raman")

    t_gold = PythonOperator(
        task_id="gold_raman",
        python_callable=gold_task,
    )

    # -------------------------
    # 4) GOLD: Picos detectados (producción)
    # -------------------------
    def peaks_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        results = []
        for js in glob.glob(f"{silver_dir}/*.json"):
            res = save_peaks_to_db(js, tolerance=15, prominence=10)
            results.append(res)
            status = res.get("status")
            if status == "failed":
                err = res.get("error") or "status=failed"
                log_error(f"save_peaks failed for {js}: {err}")
                raise RuntimeError(f"save_peaks failed for {js}: {err}")
            elif status == "no_peaks":
                logger.info(f"save_peaks no_peaks for {js}.")
            elif status == "success":
                logger.info(f"save_peaks success for {js}: inserted={res.get('rows_inserted')}, attempted={res.get('rows_attempted')}")
            else:
                logger.info(f"save_peaks status for {js}: {status}")
        return results

    t_peaks = PythonOperator(
        task_id="peaks_raman",
        python_callable=peaks_task,
    )

    # -------------------------
    # 5) TAREA TEMPORAL DE PRUEBA (FORCE = True)
    #     Por seguridad, procesa por defecto solo TEST_MAX_FILES (env var)
    # -------------------------
    def peaks_test_task(max_files: int = TEST_MAX_FILES, **_):
        """
        Ejecuta save_peaks_to_db(..., force=True) para hasta `max_files`.
        """
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        files = sorted(glob.glob(f"{silver_dir}/*.json"))
        if not files:
            logger.warning("No hay archivos .json en silver_dir para la prueba.")
            return []

        files_to_run = files[:max_files]
        logger.info(f"[TEST FORCE] Procesando {len(files_to_run)} archivo(s) (max_files={max_files})")

        results = []
        for js in files_to_run:
            res = save_peaks_to_db(js, tolerance=15, prominence=10, force=True)
            results.append(res)
            status = res.get("status")
            if status != "success":
                err = res.get("error") or f"status={status}"
                log_error(f"[TEST FORCE] save_peaks failed for {js}: {err}")
                # Queremos que falle la tarea si algo no es 'success' para validar retries/manejo
                raise RuntimeError(f"[TEST FORCE] save_peaks failed for {js}: {err}")
            logger.info(f"[TEST FORCE] save_peaks success for {js}: inserted={res.get('rows_inserted')} attempted={res.get('rows_attempted')}")
        return results

    t_peaks_test = PythonOperator(
        task_id="peaks_raman_test",
        python_callable=peaks_test_task,
        op_kwargs={"max_files": TEST_MAX_FILES},
    )

    # -------------------------
    # Flujo (por defecto): Bronze -> Silver -> Gold -> Peaks (producción)
    # Ruta de prueba: Bronze -> Silver -> Gold -> peaks_raman_test
    # -------------------------
    t_bronze >> t_silver >> t_gold >> t_peaks
    t_bronze >> t_silver >> t_gold >> t_peaks_test
```

---

# Comandos exactos para desplegar y ejecutar la prueba (CLI — recomendado)

1. **Reemplaza el archivo** localmente y haz commit (opcional):
```bash
git add Airflow/Dags/raman_pipeline.py
git commit -m "test: add peaks_raman_test task (force=True) with safe default 1 file"
```

2. **Reinicia Airflow / recarga DAGs** (depende de tu `docker-compose`):
```bash
# desde la raíz del proyecto (donde está docker-compose.yml)
docker-compose down
docker-compose up -d
# o al menos reinicia servicio airflow
docker-compose restart airflow
```

3. **Verifica que Airflow vea el DAG** (dentro del contenedor airflow):
```bash
docker-compose exec airflow bash
airflow dags list | grep raman_pipeline
# ver tasks
airflow tasks list raman_pipeline
```

4. **Ejecución de prueba (sin scheduler, ver logs en terminal)**  
Usa `airflow tasks test` para ejecutar la tarea aislada — esta ejecuta la función en el contexto de Airflow y volcará logs en la terminal:

```bash
# desde dentro del contenedor airflow
# usa una run_date cualquiera (no afecta DB)
airflow tasks test raman_pipeline peaks_raman_test 2025-08-15T00:00:00
```

`airflow tasks test` ejecutará `peaks_raman_test` y deberías ver los logs de `save_peaks_to_db`. Si quieres procesar más archivos en la prueba, exporta `RAMAN_TEST_MAX_FILES` en el entorno del contenedor antes de reiniciar Airflow, por ejemplo:

```bash
# en el host, si docker-compose define variables desde .env, añade:
export RAMAN_TEST_MAX_FILES=3
# Luego reinicia el contenedor para que la variable sea visible dentro:
docker-compose restart airflow
```

Alternativamente, edita `op_kwargs` en el DAG para pasar `max_files=3` temporalmente.

5. **Validación en la DB** (desde el contenedor postgres o usando psql cliente):
```bash
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT json_filename, COUNT(*) FROM raman_peaks GROUP BY json_filename ORDER BY json_filename LIMIT 10;"
docker-compose exec postgres psql -U omicas -d omicas -c "SELECT * FROM etl_processed_files WHERE json_filename = 'WE-PI-CHINA-1.json';"
```

---

# Cómo revertir (después de la prueba)
- Si confirmas que todo está correcto, simplemente elimina la tarea `t_peaks_test` del DAG (o comenta las dos líneas que enlazan la ruta de prueba).
- Commit y restart del servicio Airflow (o recarga de DAGs).
- Si prefieres dejarla en el código, no hará nada a menos que la ejecutes manualmente.

---

# Revisión rápida de `save_peaks.py` (pendientes / recomendaciones)
Tu `save_peaks.py` está bien estructurado y el comportamiento que mostraste en el test CLI concuerda con las métricas que esperas. Solo sugiero, si quieres, pequeñas mejoras para robustez y observabilidad (no obligatorias para la prueba):

1. **Timeout / pool de conexiones**: al crear `engine = create_engine(conn_str)` podrías añadir `pool_pre_ping=True` para recuperación automática si la conexión Postgres se recicla:
   ```python
   engine = create_engine(conn_str, pool_pre_ping=True)
   ```

2. **Logging más detallado en `ensure_processed_files_columns`**: ahora asume la tabla `etl_processed_files` existe (se crea antes) — está bien, pero podrías capturar y loggear si la consulta a `information_schema` falla.

3. **Evitar tablas temporales fuera de public**: si quieres asegurar limpieza, usar `CREATE TEMP TABLE` para staging evita colisiones en concurrencia, pero `to_sql` con conexión de SQLAlchemy a veces no soporta `CREATE TEMP TABLE` de forma directa — lo actual que tenés (staging table y DROP TABLE IF EXISTS) está bien pero ten en cuenta condiciones de concurrencia si ejecutas múltiples instancias paralelas.

4. **Tamaño XCom**: si retornas listas grandes desde tasks a XCom, Airflow puede inflar la base de metadatos. Actualmente `peaks_task` y `peaks_test_task` retornan `results` (listas pequeñas por archivo) — ok, pero si tienes muchos archivos evita retornar todo; mejor guardar en DB y devolver un resumen (counts).

Si quieres, aplico alguna de estas mejoras ahora mismo en `save_peaks.py`.

---

Dime **si quieres que reemplace el DAG tal cual** (te lo doy listo para pegar), o si prefieres que **procese 1 archivo exacto** (p. ej. `WE-PI-CHINA-1.json`) en la prueba — en ese caso te entrego la versión que fuerza ese único archivo para máxima seguridad. También puedo preparar el **patch (diff)** si prefieres aplicar con `git apply`.

### Human
Pues rey, es que me quitaste mucha parte del codigo que ya existia, mira o no se si esto este relacionado. Miralo a ver:

# Airflow/Dags/raman_pipeline.py
import sys
import os
import glob
import logging
from datetime import datetime, timedelta

# Asegurar PATH del proyecto para imports relativos
PROJECT_ROOT = "/opt/airflow/project"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from airflow import DAG
from airflow.operators.python import PythonOperator

# ETL functions (as en tu repo)
from ETL.Bronze.extract_raman import extract_raman
from ETL.Silver.clean_data import clean_data
from ETL.Gold.load_to_postgres import load_to_postgres
from ETL.Gold.save_peaks import save_peaks_to_db

# ===== Configuración de logging del DAG =====
log_file_path = "/opt/airflow/logs/raman_pipeline.log"
error_log_path = "/opt/airflow/logs/raman_pipeline_errors.log"

logger = logging.getLogger("raman_pipeline")
logger.setLevel(logging.INFO)

# Evitar duplicar handlers al recargar el DAG
if not logger.handlers:
    # File handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # Stream handler (capturado por Airflow)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(sh)

def log_error(msg: str):
    try:
        with open(error_log_path, "a") as f:
            f.write(f"{datetime.now()} - {msg}\n")
    except Exception:
        logger.exception("No se pudo escribir en error_log_path")
    logger.error(msg)

# ===== Default args =====
default_args = {
    "owner": "omicas",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Variable de entorno que controla cuantos archivos procesar en la prueba (por defecto 1)
TEST_MAX_FILES = int(os.getenv("RAMAN_TEST_MAX_FILES", "1"))

with DAG(
    dag_id="raman_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    # -------------------------
    # 1) BRONZE
    # -------------------------
    t_bronze = PythonOperator(
        task_id="bronze_raman",
        python_callable=extract_raman,
        op_kwargs={"raw_dir": "/opt/airflow/project/data/Raman_files"},
    )

    # -------------------------
    # 2) SILVER
    # -------------------------
    def silver_task(**_):
        bronze_dir = "/opt/airflow/project/data/Raman_files/json"
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        os.makedirs(silver_dir, exist_ok=True)
        for js in glob.glob(f"{bronze_dir}/*.json"):
            out = os.path.join(silver_dir, os.path.basename(js))
            clean_data(js, out)

    t_silver = PythonOperator(
        task_id="silver_raman",
        python_callable=silver_task,
    )

    # -------------------------
    # 3) GOLD: Espectros completos (producción)
    # -------------------------
    def gold_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        for js in glob.glob(f"{silver_dir}/*.json"):
            load_to_postgres(js, table_name="raman")

    t_gold = PythonOperator(
        task_id="gold_raman",
        python_callable=gold_task,
    )

    # -------------------------
    # 4) GOLD: Picos detectados (producción)
    # -------------------------
    def peaks_task(**_):
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        results = []
        for js in glob.glob(f"{silver_dir}/*.json"):
            res = save_peaks_to_db(js, tolerance=15, prominence=10)
            results.append(res)
            status = res.get("status")
            if status == "failed":
                err = res.get("error") or "status=failed"
                log_error(f"save_peaks failed for {js}: {err}")
                raise RuntimeError(f"save_peaks failed for {js}: {err}")
            elif status == "no_peaks":
                logger.info(f"save_peaks no_peaks for {js}.")
            elif status == "success":
                logger.info(f"save_peaks success for {js}: inserted={res.get('rows_inserted')}, attempted={res.get('rows_attempted')}")
            else:
                logger.info(f"save_peaks status for {js}: {status}")
        return results

    t_peaks = PythonOperator(
        task_id="peaks_raman",
        python_callable=peaks_task,
    )

    # -------------------------
    # 5) TAREA TEMPORAL DE PRUEBA (FORCE = True)
    #     Por seguridad, procesa por defecto solo TEST_MAX_FILES (env var)
    # -------------------------
    def peaks_test_task(max_files: int = TEST_MAX_FILES, **_):
        """
        Ejecuta save_peaks_to_db(..., force=True) para hasta `max_files`.
        """
        silver_dir = "/opt/airflow/project/ETL/Silver/raman_jsons_clean"
        files = sorted(glob.glob(f"{silver_dir}/*.json"))
        if not files:
            logger.warning("No hay archivos .json en silver_dir para la prueba.")
            return []

        files_to_run = files[:max_files]
        logger.info(f"[TEST FORCE] Procesando {len(files_to_run)} archivo(s) (max_files={max_files})")

        results = []
        for js in files_to_run:
            res = save_peaks_to_db(js, tolerance=15, prominence=10, force=True)
            results.append(res)
            status = res.get("status")
            if status != "success":
                err = res.get("error") or f"status={status}"
                log_error(f"[TEST FORCE] save_peaks failed for {js}: {err}")
                # Queremos que falle la tarea si algo no es 'success' para validar retries/manejo
                raise RuntimeError(f"[TEST FORCE] save_peaks failed for {js}: {err}")
            logger.info(f"[TEST FORCE] save_peaks success for {js}: inserted={res.get('rows_inserted')} attempted={res.get('rows_attempted')}")
        return results

    t_peaks_test = PythonOperator(
        task_id="peaks_raman_test",
        python_callable=peaks_test_task,
        op_kwargs={"max_files": TEST_MAX_FILES},
    )

    # -------------------------
    # Flujo (por defecto): Bronze -> Silver -> Gold -> Peaks (producción)
    # Ruta de prueba: Bronze -> Silver -> Gold -> peaks_raman_test
    # -------------------------
    t_bronze >> t_silver >> t_gold >> t_peaks
    t_bronze >> t_silver >> t_gold >> t_peaks_test

