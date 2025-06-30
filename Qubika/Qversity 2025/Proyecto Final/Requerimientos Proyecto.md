

# ✅ Data Pipeline Project Checklist

## 🐳 Docker & Environment
- [x] Repository follows naming convention `qversity-data-[year]-[city]-[your-name]`
- [x] Docker environment runs successfully: `docker-compose up -d`
- [x] Credentials stored in `.env` (never committed to Git)
- [ ] Full pipeline tested end-to-end via Docker

## 🚦 Airflow Execution
- [ ] Airflow DAG executes end-to-end without errors
- [ ] DAG includes clear task naming and documentation

## 🛠️ dbt Data Modeling
- [ ] dbt models create:
  - [ ] **Bronze layer** (raw data ingestion)
  - [ ] **Silver layer** (cleaned, transformed)
  - [ ] **Gold layer** (business-ready aggregates)
- [ ] All dbt tests pass: `dbt test`
- [ ] No array data types remain in final models
- [ ] All nested JSON objects flattened into columns

## 📊 Data Quality
- [ ] JSON data successfully loaded to database
- [ ] Verified >1000 records ingested
- [ ] dbt data quality tests implemented:
  - [ ] Not null checks
  - [ ] Unique keys
  - [ ] Accepted value validation
- [ ] Business questions answered with data




## 📝 Documentation
- [ ] `README.md` provides clear setup instructions:
  ```markdown
  ### Setup
  1. Clone repo: `git clone [url]`
  2. Create `.env` from `.env.example`
  3. Start services: `docker-compose up -d`
  4. Access Airflow at: http://localhost:8080
```


---

# NOTAS Procedimiento


# 1.✅ Revisión del archivo `.env`

|Variable|Valor|Estado|Comentario|
|---|---|---|---|
|`COMPOSE_PROJECT_NAME`|`qversity`|✅ Correcto|Define el prefijo del proyecto para Docker|
|`AIRFLOW_UID`|`50000`|✅ Correcto|UID genérico para permisos en el contenedor de Airflow|
|`AIRFLOW_PROJ_DIR`|`.`|✅ Correcto|Apunta al directorio del proyecto actual|
|`_AIRFLOW_WWW_USER_USERNAME`|`admin`|✅ Correcto|Usuario web para Airflow|
|`_AIRFLOW_WWW_USER_PASSWORD`|`admin`|✅ Correcto|Contraseña del UI de Airflow|
|`POSTGRES_USER`|`qversity-admin`|✅ Correcto|Usuario de la base de datos|
|`POSTGRES_PASSWORD`|`qversity-admin`|✅ Correcto|Contraseña de PostgreSQL|
|`POSTGRES_DB`|`qversity`|✅ Correcto|Nombre de la base de datos|
|`DBT_PROFILES_DIR`|`/dbt`|✅ Correcto|Ruta dentro del contenedor donde se espera el archivo `profiles.yml`|
|`DBT_PROJECT_DIR`|`/dbt`|✅ Correcto|Ruta del proyecto dbt en el contenedor|

El `.env` está **correctamente configurado** ✅

# 2. ▶️ Paso siguiente: Levantar servicios

```bash
docker compose up -d

## validar
docker compose ps
```

![[Pasted image 20250614204108.png]]

Confirma que aparezcan contenedores como:
- `qversity-airflow-*`
- `qversity-postgres`
- `qversity-dbt`
Y que todos estén con `state: running` o `healthy`.

![[Pasted image 20250614204116.png]]
##### Sobre la advertencia (`version is obsolete`)
- Docker Compose v2 ya no requiere la clave `version` en el fichero YAML.
- Puedes **eliminar** la línea `version: '3.8'` (o la que tengas) de tu `docker-compose.yml` para evitar confusiones futuras. No afectará al arranque.


### Verificaciones de salud
1. **Airflow UI**
    - Abre en el navegador: [http://localhost:8080](http://localhost:8080)
    - Inicia sesión con `admin` / `admin`.

![[Pasted image 20250614204236.png]]


2. **Conexión a PostgreSQL**  
Desde tu terminal:

```bash
docker compose exec postgres psql -U qversity-admin -d qversity
```

Para probar

```bash
\l    -- lista bases de datos
\dn   -- lista esquemas
```
Si estas consultas funcionan, la base está operativa.

![[Pasted image 20250614204415.png]]

1. `\l` — Bases de datos
```bash
postgres
qversity       ← ✅ tu base de datos de trabajo
template0
template1
```

Tienes correctamente creada la base `qversity`, que es donde se almacenarán las tablas de las capas **bronze**, **silver** y **gold**.

2. `\dn` — Schemas

```bash
public
```

Solo existe el schema `public` porque aún **no has ejecutado ningún modelo dbt** que cree los schemas `bronze`, `silver`, o `gold`. Esto es completamente normal si aún no has corrido:

```bash
dbt run
```

3. `\dt` — Tablas

Sin salida. Es correcto: **no hay ninguna tabla creada aún** porque:

- No se ha ejecutado ningún modelo dbt
- Tampoco se ha corrido ningún DAG de ingestión de datos desde Airflow


# 3. ## 🔜 Crear los esquemas Bronze, Silver y Gold en PostgreSQL

Para mantener el orden de tu arquitectura Medallion, te recomiendo crear tres esquemas vacíos antes de ingestar cualquier datos. En psql:

```sql
-- Conéctate a la BD qversity si no lo has hecho:
\c qversity

-- Crea los esquemas:
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Verifica:
\dn
```

Ahora al hacer `\dn` deberías ver:
```bash
bronze
public
silver
gold
```

![[Pasted image 20250614221016.png]]
















# 3. Creación del Bronze Dag

1. **download_from_s3**
    - Descarga el JSON `mobile_customers_dataset.json` desde el bucket `qversity-raw-public-data`
    - Lo guarda en `dags/data/raw/`
        
2. **create_bronze_table**
    - Crea el schema `bronze` y la tabla `bronze.mobile_customers_raw` con un campo `JSONB`
        
3. **load_raw_data**
    - Lee el JSON descargado
    - Inserta cada objeto como un registro en la tabla `bronze.mobile_customers_raw`
        
4. **cleanup_local_file**
    - Elimina el archivo local tras la carga

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import boto3
import json
import os

def download_from_s3(**kwargs):
    bucket = 'qversity-raw-public-data'
    key = 'mobile_customers_dataset.json'
    local_path = os.path.join(os.environ.get('AIRFLOW__CORE__DAGS_FOLDER', '/opt/airflow/dags'), 'data', 'raw', key)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    s3 = boto3.client('s3')
    s3.download_file(bucket, key, local_path)
    return local_path


def create_bronze_table(**kwargs):
    create_sql = """
    CREATE SCHEMA IF NOT EXISTS bronze;
    CREATE TABLE IF NOT EXISTS bronze.mobile_customers_raw (
        id SERIAL PRIMARY KEY,
        raw_data JSONB,
        ingestion_timestamp TIMESTAMP DEFAULT now()
    );
    """
    pg = PostgresHook(postgres_conn_id='postgres_default')
    pg.run(create_sql)


def load_raw_data(**kwargs):
    ti = kwargs['ti']
    local_path = ti.xcom_pull(task_ids='download_from_s3')
    pg = PostgresHook(postgres_conn_id='postgres_default')
    # Read JSON file and insert rows
    with open(local_path, 'r') as f:
        records = json.load(f)

    # Assuming records is a list of JSON objects
    insert_sql = "INSERT INTO bronze.mobile_customers_raw (raw_data) VALUES (%s);"
    for rec in records:
        pg.run(insert_sql, parameters=(json.dumps(rec),))


def cleanup(**kwargs):
    ti = kwargs['ti']
    local_path = ti.xcom_pull(task_ids='download_from_s3')
    try:
        os.remove(local_path)
    except Exception:
        pass


default_args = {
    'owner': 'qversity',
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='bronze_layer_ingestion',
    default_args=default_args,
    catchup=False,
    schedule_interval='@daily',
    tags=['bronze', 'qversity'],
) as dag:

    t1 = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        provide_context=True,
    )

    t2 = PythonOperator(
        task_id='create_bronze_table',
        python_callable=create_bronze_table,
        provide_context=True,
    )

    t3 = PythonOperator(
        task_id='load_raw_data',
        python_callable=load_raw_data,
        provide_context=True,
    )

    t4 = PythonOperator(
        task_id='cleanup_local_file',
        python_callable=cleanup,
        provide_context=True,
    )

    t1 >> t2 >> t3 >> t4

```

### Pasos para incorporar el DAG:

1. Copiar el contenido del canvas a `dags/bronze_dag.py`.
2. Asegurarse de tener en el `requirements.txt`: boto3
3. Reconstruir el entorno dbt/Airflow:
```bash
docker compose up -d --build airflow
```

4. Entrar a Airflow y activar el DAG `bronze_layer_ingestion`.
5. Ejecutar manualmente o esperar al primer schedule diario.


![[Pasted image 20250614210405.png]]


## 🧠 1. ¿Se debe ejecutar `bronze_dag.py` manualmente?

**No. Nunca debes darle “Run” manual en VSCode** como si fuera un script Python.
### Por qué:
Airflow **detecta automáticamente** los DAGs que estén dentro de la carpeta `dags/` configurada en tu entorno (por defecto, `./dags/` dentro del contenedor).

Entonces:
- Tú editas los archivos `.py` con DAGs desde VSCode.
- Pero **quien ejecuta el DAG es Airflow**, desde su UI o por su scheduler.


---
# Junio 17

## ✅ Guía en resúmen (Roadmap)

|Etapa|Acción|
|---|---|
|**Bronze**|✔️ Completo (ya tienes datos crudos cargados)|
|**Silver**|Corrige SQL y conversión numeric “unknown” → NULL|
||Ajusta nombres de campo (`ingestion_timestamp`)|
||Haz `dbt run` y `dbt test` para silver_customers, silver_payments|
|**Gold**|Define modelos de negocio y tests asociados|
|**Entrega final**|Esquema ER (Entity Relationship Diagram)|
||Documentación del pipeline y decisiones tomadas|
||Respuestas a preguntas de negocio en base al Gold|




![[Pasted image 20250617182208.png]]


docker compose exec postgres psql -U qversity-admin -d qversity -c "\dt bronze.*"
time="2025-06-17T18:21:29-05:00" level=warning msg="C:\\Users\\Juan Jose Restrepo\\Desktop\\Proyecto Final Qversity\\qversity-data-final-project-2025\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
                List of relations
 Schema |     Name      | Type  |     Owner
--------+---------------+-------+----------------
 bronze | customers_raw | table | qversity-admin
(1 row)

 docker compose exec postgres psql -U qversity-admin -d qversity -c "SELECT COUNT(*) FROM bronze.customers_raw;"
time="2025-06-17T18:21:36-05:00" level=warning msg="C:\\Users\\Juan Jose Restrepo\\Desktop\\Proyecto Final Qversity\\qversity-data-final-project-2025\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
 count
-------
 28151
(1 row)

![[Pasted image 20250617182219.png]]


## dbt silver payments and customers.sql


```bash
dbt clean --profiles-dir /dbt --project-dir /dbt
```

![[Pasted image 20250617194238.png]]


```bash
dbt debug
```

![[Pasted image 20250617194313.png]]


```bash
dbt test  --profiles-dir /dbt --project-dir /dbt --models silver_customers silver_payments
```

![[Pasted image 20250617194347.png]]


```bash
dbt test  --profiles-dir /dbt --project-dir /dbt --models silver_customers silver_payments
```

![[Pasted image 20250617194358.png]]


---

Al correr

```bash

```


public | dag_run                        | table | qversity-admin
 public | dag_run_note                   | table | qversity-admin
 public | dag_schedule_dataset_reference | table | qversity-admin
 public | dag_tag                        | table | qversity-admin
 public | dag_warning                    | table | qversity-admin
 public | dagrun_dataset_event           | table | qversity-admin
 public | dataset                        | table | qversity-admin
 public | dataset_dag_run_queue          | table | qversity-admin
 public | dataset_event                  | table | qversity-admin
 public | import_error                   | table | qversity-admin
 public | job                            | table | qversity-admin
 public | log                            | table | qversity-admin
 public | log_template                   | table | qversity-admin
 public | rendered_task_instance_fields  | table | qversity-admin
 public | serialized_dag                 | table | qversity-admin
 public | session                        | table | qversity-admin
 public | sla_miss                       | table | qversity-admin
 public | slot_pool                      | table | qversity-admin
 public | task_fail                      | table | qversity-admin
 public | task_instance                  | table | qversity-admin
 public | task_instance_note             | table | qversity-admin
 public | task_map                       | table | qversity-admin
 public | task_outlet_dataset_reference  | table | qversity-admin
 public | task_reschedule                | table | qversity-admin
 public | trigger                        | table | qversity-admin
 public | variable                       | table | qversity-admin
 public | xcom                           | table | qversity-admin
(42 rows)



--- 
raw data
```sql
SELECT
  (raw_json->>'customer_id')::int    AS customer_id,
  raw_json->>'first_name'             AS first_name,
  raw_json->>'email'                  AS email,
  (raw_json->>'phone_number')::text   AS phone_number
FROM bronze.customers_raw
LIMIT 10;
```


qversity=# SELECT (raw_json->>'customer_id')::int    AS customer_id, raw_json->>'first_name'             AS first_name,   raw_json->>'email'                  AS email,   (raw_json->>'phone_number')::text   AS phone_number  FROM bronze.customers_raw LIMIT 10;
 customer_id | first_name |            email            | phone_number
-------------+------------+-----------------------------+--------------
      604027 | Ana        | ana.gonzale@outlook.com     | 3144143064
      227667 |  Carme     | carme.rodriguez@email.com   | 3100626224
      324851 | Ana        | ana.rodrigue@outlook.com    | 3197349248
      505201 | Jun        | junmartínezcorreo.com       | 3154298487
      544725 | carlos     | carlos.fernande@outlook.com | 3197663808
      497219 | Sofi       | sofi.martnez@yahoo.com      | 3107682829
      855602 | miguel     | miguel.fernn@outlook.com    | 3137988968
      676908 | Mig        | mig.martin@outlook.com      | 319329141
      664874 | Mig        | mig.rodrguez@hotmail.com    | 3150860721
      240876 | Ana        | ana.rodrguez@email.com      | 3177217700
(10 rows)

qversity=#



---


## 📦 Exportar y utilizar datos raw en Obsidian

---

### 1. Exportar datos desde PostgreSQL con Docker Compose

1. **Dentro del contenedor** (bash):
    
    ```bash
    # JSON completo
    psql -U qversity-admin -d qversity \
      -c "COPY (SELECT raw_json FROM bronze.customers_raw) TO '/tmp/raw_data.json';"
    
    # CSV con columnas seleccionadas
    psql -U qversity-admin -d qversity \
      -c "COPY (SELECT \
        (raw_json->>'customer_id')::int    AS customer_id, \
        raw_json->>'first_name'             AS first_name, \
        raw_json->>'email'                  AS email, \
        raw_json->>'phone_number'           AS phone_number \
      FROM bronze.customers_raw) TO '/tmp/raw_data.csv' WITH CSV HEADER;"
    ```
    
2. **Copiar archivo a máquina local** (host):
    
    ```bash
    # JSON
    docker cp qversity-postgres-1:/tmp/raw_data.json ./raw_data.json
    
    # CSV
    docker cp qversity-postgres-1:/tmp/raw_data.csv ./raw_data.csv
    ```
    

---

### 2. Documentación en Markdown para Obsidian

````markdown
# Raw Data Extraction

## Resumen
En esta nota se documenta cómo extraer los datos crudos de la tabla `bronze.customers_raw` desde PostgreSQL dentro de Docker y cómo copiar los archivos resultantes a la máquina local.

---

## Comandos de exportación

### 1. Exportar a JSON
```bash
psql -U qversity-admin -d qversity \
  -c "COPY (SELECT raw_json FROM bronze.customers_raw) TO '/tmp/raw_data.json';"
````

### 2. Exportar a CSV

```bash
psql -U qversity-admin -d qversity \
  -c "COPY (SELECT (raw_json->>'customer_id')::int AS customer_id, raw_json->>'first_name' AS first_name, raw_json->>'email' AS email, raw_json->>'phone_number' AS phone_number FROM bronze.customers_raw) TO '/tmp/raw_data.csv' WITH CSV HEADER;"
```

### 3. Copiar a host

```bash
docker cp qversity-postgres-1:/tmp/raw_data.csv ./raw_data.csv
```

---

## Python Script de ejemplo

```python

# export_raw_data.py
# Script para extraer datos raw desde PostgreSQL en Docker a JSON y CSV

import os
import json
import csv
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

# Configuración de conexión (toma de variables de entorno o valores por defecto)
DB_USER = os.getenv('POSTGRES_USER', 'qversity-admin')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'qversity-admin')
DB_NAME = os.getenv('POSTGRES_DB', 'qversity')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Rutas de salida
OUTPUT_DIR = 'data/raw'
JSON_FILE = os.path.join(OUTPUT_DIR, 'raw_data.json')
CSV_FILE = os.path.join(OUTPUT_DIR, 'raw_data.csv')

# Asegurar que la carpeta exista
os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_json():
    """
    Extrae la columna raw_json desde bronze.customers_raw y la guarda como JSON lines.
    """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT raw_json FROM bronze.customers_raw;")
    rows = cur.fetchall()

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row['raw_json'], ensure_ascii=False))
            f.write('
')

    cur.close()
    conn.close()
    print(f"Exportado JSON a {JSON_FILE}, registros: {len(rows)}")


def export_csv():
    """
    Extrae un subconjunto de columnas para un CSV legible.
    """
	query = '''
		SELECT
		  (raw_json->>'customer_id')::float AS customer_id,
		  raw_json->>'first_name'           AS first_name,
		  raw_json->>'last_name'            AS last_name,
		  raw_json->>'email'                AS email,
		  raw_json->>'phone_number'         AS phone_number,
		  (raw_json->>'age')::float         AS age,
		  raw_json->>'country'              AS country,
		  raw_json->>'city'                 AS city,
		  raw_json->>'operator'             AS operator
		FROM bronze.customers_raw;
	'''

    # Usamos pandas para conveniencia
    conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    df = pd.read_sql(query, conn_str)
    df.to_csv(CSV_FILE, index=False, encoding='utf-8')
    print(f"Exportado CSV a {CSV_FILE}, filas: {len(df)}")


def main():
    export_json()
    export_csv()


if __name__ == '__main__':
    main()
```



}]}
```python
import pandas as pd

# Cargar CSV exportado
df = pd.read_csv('raw_data.csv')

# Vista previa
display(df.head(10))

# Inspect columns and types
print(df.info())

# Guardar en otro formato si es necesario
df.to_parquet('raw_data.parquet', index=False)
```

## CAPA SILVER RESULTS PSQL

![[Pasted image 20250618215839.png]]


## README
```markdown
# Silver Layer — Data Transformation

## 🧱 Contexto del Proyecto

Este proyecto forma parte del pipeline de datos para la plataforma local de análisis desarrollada como entregable final del curso de Qversity. La arquitectura sigue el enfoque *lakehouse* en capas: **Bronze → Silver → Gold**.

La **capa Silver** se encarga de transformar los datos brutos del JSON cargado en PostgreSQL (`bronze.customers_raw`) en tablas limpias, tipadas y deduplicadas para su posterior análisis.

---

## 📐 Estructura de Modelos

Los modelos transformados en esta capa son:

| Modelo                | Descripción breve                               |
|-----------------------|--------------------------------------------------|
| `silver_customers`    | Datos de clientes normalizados y deduplicados   |
| `silver_payments`     | Historial de pagos a nivel fila (exploded JSON) |

---

## 🧪 Validaciones realizadas

Se aplicaron pruebas automáticas de dbt para asegurar la calidad de los datos:

### `silver_customers`

- `customer_id`: `not_null`, `unique`
- `email`: `not_null`, `unique`

### `silver_payments`

- `raw_id`: `not_null`
- `payment_date`: `not_null`

Todas las pruebas fueron superadas con éxito ✅

---

## 🧹 Transformaciones clave

### ✔️ Limpieza
- Eliminación de espacios, símbolos y caracteres especiales (`regexp_replace`)
- Tipado correcto con casting: `int`, `numeric`, `float`, `date`
- Manejo de formatos de fecha múltiples (`to_date`, `::date`)
- Normalización de texto (`initcap`, `lower`, `upper`)

### ✔️ Deduplicación
- Clientes duplicados por `customer_id` → `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ingestion_ts DESC)`
- Corrección por `email` → se conserva solo el más reciente

### ✔️ Explosión del JSON
- `silver_payments` utiliza `jsonb_array_elements` para transformar `payment_history` en múltiples filas

---

## 📂 Esquema y materialización

Ambas tablas se materializan como `table` en el esquema **silver**:

```sql
{{
  config(
    materialized = 'table'
  )
}}

```


## ✅ Resultado final

Verificado con:

```bash
\dt silver.*
```

```sql
 Schema |       Name       | Type  |     Owner
--------+------------------+-------+----------------
 silver | silver_customers | table | qversity-admin
 silver | silver_payments  | table | qversity-admin
```



## ✅ ¿Qué prevalece?

dbt sigue esta prioridad:

1. El esquema definido en el modelo (`config(schema='...')`)
2. El esquema definido en el `dbt_project.yml` para esa carpeta
3. El esquema por defecto en `profiles.yml`



