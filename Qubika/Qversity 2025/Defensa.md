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

#### 1. Configuration and Setup

- **`URL`** points to the public S3 JSON dataset.
- **`RAW_JSON_PATH`** is the local path inside our Airflow container where we write the JSON file.
- **`DB_CONN_INFO`** reads connection parameters from environment variables (`.env`) , ensuring portability across environments.
- **`default_args`** include owner, start date, retry policy, and notification settings for robust execution.”
	- In Python, `**` before a dictionary unpacks its key–value pairs into **named function arguments**. It’s equivalent to: 
			conn = psycopg2.connect(
			    host=DB_CONN_INFO['host'],
			    port=DB_CONN_INFO['port'],
			    dbname=DB_CONN_INFO['dbname'],
			    user=DB_CONN_INFO['user'],
			password=DB_CONN_INFO['password'],
			)

#### 2. Task 1 – Download JSON

```python
def download_json():
	os.makedirs(os.path.dirname(RAW_JSON_PATH), exist_ok=True)
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    data = response.json()
    with open(RAW_JSON_PATH, 'w', encoding='utf-8') as f:
        for rec in data:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    logging.info("✅ JSON downloaded with %d records", len(data))

```

In the **`download_json`** function, we:
- **Ensure the target directory exists** (`os.makedirs` with `exist_ok=True`).
- **Fetch the entire JSON** from S3 using `requests.get(...)` with a 60‑second timeout.
- **Validate the response** by calling `raise_for_status()` to fail fast on HTTP errors.
- **Parse the JSON into a Python list**, then open our local file in write mode.
- **Write each record as one line of JSON** (NDJSON format), which simplifies downstream streaming and bulk loading.
- **Log the number of records** for observability.”


#### 3. Task 2 – Load to PostgreSQL

```python
def load_to_postgres():
    conn = psycopg2.connect(**DB_CONN_INFO)
    cur = conn.cursor()

    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS bronze;
    DROP TABLE IF EXISTS bronze.customers_raw;
    CREATE TABLE bronze.customers_raw (
        id SERIAL PRIMARY KEY,
        raw_json JSONB,
        ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    with open(RAW_JSON_PATH, 'r', encoding='utf-8') as f:
        records = [(json.dumps(json.loads(line)),) for line in f]
    execute_values(
        cur,
        "INSERT INTO bronze.customers_raw (raw_json) VALUES %s",
        records
    )

    conn.commit()
    cur.close()
    conn.close()
    logging.info("✅ Loaded %d records into bronze.customers_raw", len(records))

```

“In the **`load_to_postgres`** function, we:

- **Open a connection** to PostgreSQL via `psycopg2.connect` using our `DB_CONN_INFO`.
- **Obtain a cursor** to execute SQL statements.
- **Ensure idempotency** by dropping and recreating the target table:
	- `CREATE SCHEMA IF NOT EXISTS bronze;`
	- `DROP TABLE IF EXISTS bronze.customers_raw;`
	- `CREATE TABLE bronze.customers_raw (...)` defines three columns:
	    - `id SERIAL PRIMARY KEY` for a unique surrogate key,
	    - `raw_json JSONB` to store the original JSON record,
	    - `ingestion_timestamp` to track when it was loaded.

- **Read the JSON file line by line**, parse each line back into JSON (to ensure valid JSON), then wrap it in a one‑element tuple for bulk insertion.
- **Use `psycopg2.extras.execute_values`** to perform a **single bulk INSERT** of all records. This is far more efficient than row‑by‑row inserts.
- **Commit the transaction**, close cursor and connection to free resources.
- **Log the total number of rows** inserted for monitoring.”


---
## Silver layer

**Goal:** Transform raw JSON into clean, normalized, and queryable relational tables.

- In the Silver layer, I transformed the unstructured JSON data from the Bronze layer into structured tables following **Third Normal Form (3NF)**.  

I created three core models using dbt:


##### - `silver_customers`

This is the central model in Silver. It parses customer profiles and attributes from the JSON structure. I implemented:"

- ✅ Field extraction from nested JSON (`->>` operators).
- ✅ **Custom cleaning rules** for:
    - First and last names (`initcap`, `regexp_replace`, `fallbacks`)
    - Email validation using regex
    - Phone number normalization (only valid 10-digit numbers)
    - Normalized cities (`Bogotá`, `Cali`, `Lima`, etc.)
    - Standardized countries (COLOMBIA, MEXICO, PERU, etc.)
    - Plan types: `PREPAGO`, `POSPAGO`, `CONTROL`
    - Operators: `CLARO`, `TIGO`, `WOM`, `MOVISTAR`
    
- ✅ Validation and segmentation of `credit_score`
- ✅ Date parsing in multiple formats (ISO and DD/MM/YYYY)
- ✅ Type casting for numerical fields (bill, data usage, coordinates)
- ✅ Final **deduplication** using `row_number()` over `customer_id`, keeping the most recent record.


This model ensures that all personal, geographic, and financial attributes are validated and consistent.


##### - `silver_services`

**This model flattens the array of contracted services for each customer.**

- ✅ Extracts the `contracted_services` JSON array
- ✅ Uses `jsonb_array_elements()` to explode each service
- ✅ Normalizes names with `replace()`, `upper()`, `trim()`
- ✅ Maps common variants to a controlled list: `VOICE`, `SMS`, `DATA`, `ROAMING`, `INTERNATIONAL`

 "The output is one row per service per customer, linked via `raw_id`."


##### - `silver_payments`

**This model explodes the `payment_history` array per customer into separate payment records.**

- ✅ Validates structure: only arrays are processed
- ✅ Extracts:
    - `payment_date`
    - `amount` (validated using regex)
    - `amount_validity` (tagged as VALID or INVALID)
    - `status` (e.g., PAID, FAILED)

It generates a payment timeline per customer, enabling all Gold models related to revenue and payment behavior.


### 🧩 Relationships & ERD

All models are connected via `raw_id` (from the Bronze source).  
The Silver layer feeds into more than 20 Gold models.  

For example:

- `silver_customers` → demographics, operators, plans, geography
- `silver_services` → combinations, popularity, ARPU
- `silver_payments` → payment issues, revenue metrics

This modular design lets us reuse clean, validated data in multiple business contexts.

##### Análisis detallado – `silver_customers.sql`

![[Pasted image 20250702195142.png]]

![[Pasted image 20250702195151.png]]

![[Pasted image 20250702195208.png]]
![[Pasted image 20250702202426.png]]





![[Pasted image 20250702195242.png]]
![[Pasted image 20250702195249.png]]
![[Pasted image 20250702195415.png]]

![[Pasted image 20250702195423.png]]

![[Pasted image 20250702195523.png]]

![[Pasted image 20250702195531.png]]


![[Pasted image 20250702195553.png]]

![[Pasted image 20250702195616.png]]

![[Pasted image 20250702201509.png]]


![[Pasted image 20250702201525.png]]

![[Pasted image 20250702201559.png]]

![[Pasted image 20250702201609.png]]


![[Pasted image 20250702202551.png]]


##### 🧩 Análisis detallado — `silver_services.sql`

![[Pasted image 20250702201745.png]]

![[Pasted image 20250702201753.png]]
![[Pasted image 20250702201803.png]]


![[Pasted image 20250702201813.png]]
![[Pasted image 20250702201846.png]]
![[Pasted image 20250702201900.png]]

![[Pasted image 20250702201912.png]]


##### 🧾 Análisis detallado — `silver_payments.sql`


![[Pasted image 20250702202014.png]]
![[Pasted image 20250702202020.png]]

![[Pasted image 20250702202029.png]]

![[Pasted image 20250702202200.png]]
![[Pasted image 20250702202204.png]]
![[Pasted image 20250702202210.png]]
![[Pasted image 20250702202217.png]]






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


