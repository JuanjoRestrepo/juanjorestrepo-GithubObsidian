# 🎯 PASO 1 — Executive Pitch

I designed and implemented a complete ELT data pipeline using Apache Airflow, dbt, and PostgreSQL, following the Medallion architecture (Bronze, Silver, Gold).


![[Pasted image 20250702163048.png]]
Fuente: Databricks
## **Bronze Layer**

- The source was a complex JSON dataset containing mobile customer data.
- I extracted it from a public S3 bucket and ingested it into PostgreSQL using orchestrated DAGs in Airflow.


## ***Explanation🥉 Bronze Layer***

**Objective**: Ingest raw JSON into PostgreSQL.

1. Initial Prototype (`bronze_ingest.py`)
**What it does:**
- Creates the `bronze.customers_raw` table if missing.
- Fetches the entire JSON payload via HTTP.
- Inserts each record one by one into Postgres using the default Airflow Postgres hook.

```python
with DAG(
    dag_id='bronze_ingest_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql="""
            CREATE SCHEMA IF NOT EXISTS bronze;
            CREATE TABLE IF NOT EXISTS bronze.customers_raw (
                id SERIAL PRIMARY KEY,
                raw_json JSONB NOT NULL,
                ingestion_timestamp TIMESTAMP NOT NULL DEFAULT now()
            );
        """
    )

    load_data = PythonOperator(
        task_id='load_data_via_http',
        python_callable=load_via_http  # fetch & insert one record at a time
    )

    create_table >> load_data
```

This proved the concept but suffered from per‑record inserts (slower) and relied on `postgres_default` connection.


2. Production‑Ready DAG (`bronze_etl_dag.py`)

**Enhancements:**

- Bulk inserts via `psycopg2.extras.execute_values` for performance.
- Explicit DB connection parameters via environment variables.
- Writes JSON as newline‑delimited (NDJSON) file first for traceability.
- Drops & recreates the target table each run to ensure idempotency.


`complete_pipeline.py`

This DAG orchestrates all layers, but here we focus strictly on the Bronze ingestion steps.

```python
# dags/complete_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
import json
import os
import logging
import psycopg2
from psycopg2.extras import execute_values

# -----------------------------------------------

# CONFIGURACIÓN GENERAL

# -----------------------------------------------

URL = 'https://qversity-raw-public-data.s3.amazonaws.com/mobile_customers_messy_dataset.json'

RAW_JSON_PATH = '/opt/airflow/data/raw/raw_data.json'


DB_CONN_INFO = {
    'host': os.getenv('DB_HOST', 'postgres'),
    
    'port': os.getenv('DB_PORT', 5432),
    'dbname': os.getenv('POSTGRES_DB', 'qversity'),
    'user': os.getenv('POSTGRES_USER', 'qversity-admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'qversity-admin'),

}

  

default_args = {

    'owner': 'qversity',

    'start_date': days_ago(1),

    'depends_on_past': False,

    'email_on_failure': False,

    'email_on_retry': False,

    'retries': 1,

    'retry_delay': timedelta(minutes=2),

}

```




## Silver layer

- I cleaned and normalized the data—parsing nested fields, flattening arrays, and enforcing relational integrity. 

## Gold layer

- In the Gold layer, I used dbt to model business-ready tables and KPIs aligned with 21 predefined business questions.
- These insights covered customer behavior, service preferences, revenue patterns, and risk indicators like payment failures.


# 🧠 PASO 2 — Estructura de presentación por bloques


## 1. 🏗️ **Project Architecture**

![[Pasted image 20250702163041.png]]

We implemented a full ELT architecture based on the Medallion design pattern: Bronze, Silver, and Gold layers.

- We used **Apache Airflow for orchestration**
- **dbt for SQL-based modeling**
- **PostgreSQL as our data warehouse.**

All processes were containerized and managed using Docker and Docker Compose.


![[Pasted image 20250702172019.png]]

![[Pasted image 20250702172036.png]]

![[Pasted image 20250702172111.png]]

![[Pasted image 20250702172130.png]]

![[Pasted image 20250702172145.png]]


## 2. ⚙️ **Data Pipeline & Processing**

***“How did the data flow from raw to insight?”***

- The raw dataset was a JSON file stored in a public S3 bucket.
- In the Bronze layer, we ingested the raw data directly into PostgreSQL using a Python script and Airflow DAG.
- In the Silver layer, we parsed nested JSON fields, removed arrays, standardized field types, and normalized the data into 3NF.
- In the Gold layer, we created star-schema models with dbt to generate analytical tables that answer 21 specific business questions.

https://www.mermaidchart.com/app/projects/280dc706-7d77-41e9-b310-0a3a4def1f27/diagrams/a0e5d552-2c01-4784-8431-0fe642caca2e/version/v0.1/edit
















---
# 📊 PASO 3 — Selección de 3 a 5 Insights clave (defensa de resultados)


No necesitas explicar los 21 insights: **elige los más impactantes y dominados**, por ejemplo:

We derived 21 business insights. I will present a few that show the business value of this pipeline.

| Insight # | Tema                                     | Por qué elegirlo                          |
| --------- | ---------------------------------------- | ----------------------------------------- |
| 1         | % fallos de pago                         | Riesgo financiero → decisiones inmediatas |
| 5         | Combinaciones más frecuentes             | Segmentación de producto y marketing      |
| 6         | Combinaciones más rentables              | Maximización de ingresos                  |
| 11        | Resumen general de uso y ARPU            | Muestra síntesis de análisis cruzado      |
| 7         | Salud por operador (si tienes los datos) | Muestra contexto geográfico               |


1. % fallos de pago
![[Pasted image 20250702173313.png]]

we identified that 75% of customers have at least one failed payment, which represents a serious operational risk


# 4. 💡 **Business Impact & Recommendations**

_“What can the company do with these insights?”_

Based on these findings, we recommend:

1. Designing segmented service bundles (basic vs. premium).
2. Prioritizing collections and reminders for customer segments with failed or pending payments.
3. Creating campaigns targeted to the most valuable service combinations


# 🎤 PASO 5 — Posibles preguntas del jurado (Q&A)

Te anticipo las 5–7 preguntas más comunes y te doy respuestas modelo:

- Why did you choose dbt instead of SQL scripts or Python?
- What’s the business value of your insights?
- What would you improve if you had more time?


