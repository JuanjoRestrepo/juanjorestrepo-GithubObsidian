# 🎯 PASO 1 — Executive Pitch

I designed and implemented a complete ELT data pipeline using Apache Airflow, dbt, and PostgreSQL, following the Medallion architecture (Bronze, Silver, Gold).


![[Pasted image 20250702163048.png]]
Fuente: Databricks
## Bronze Layer

- The source was a complex JSON dataset containing mobile customer data.
- I extracted it from a public S3 bucket and ingested it into PostgreSQL using orchestrated DAGs in Airflow.

## Silver layer

- I cleaned and normalized the data—parsing nested fields, flattening arrays, and enforcing relational integrity. 

## Gold layer

- In the Gold layer, I used dbt to model business-ready tables and KPIs aligned with 21 predefined business questions.
- These insights covered customer behavior, service preferences, revenue patterns, and risk indicators like payment failures.


# 🧠 PASO 2 — Estructura de presentación por bloques



![[Pasted image 20250702163041.png]]

We implemented a full ELT architecture based on the Medallion design pattern: Bronze, Silver, and Gold layers.

- We used **Apache Airflow for orchestration**
- **dbt for SQL-based modeling**
- **PostgreSQL as our data warehouse.**



# 📊 PASO 3 — Selección de 3 a 5 Insights clave (defensa de resultados)


No necesitas explicar los 21 insights: **elige los más impactantes y dominados**, por ejemplo:

|Insight #|Tema|Por qué elegirlo|
|---|---|---|
|1|% fallos de pago|Riesgo financiero → decisiones inmediatas|
|5|Combinaciones más frecuentes|Segmentación de producto y marketing|
|6|Combinaciones más rentables|Maximización de ingresos|
|11|Resumen general de uso y ARPU|Muestra síntesis de análisis cruzado|
|7|Salud por operador (si tienes los datos)|Muestra contexto geográfico|

# 🎤 PASO 4 — Posibles preguntas del jurado (Q&A)

Te anticipo las 5–7 preguntas más comunes y te doy respuestas modelo:

- Why did you choose dbt instead of SQL scripts or Python?
- What’s the business value of your insights?
- What would you improve if you had more time?


