
## Justificación técnica para usar PostgreSQL

|Criterio|Justificación|
|---|---|
|🔒 Seguridad|Permite control de usuarios, roles y privilegios para acceso y edición.|
|📦 Estructura relacional|Ideal para representar de forma estructurada artículos, autores, palabras clave, etc.|
|🔄 Compatibilidad con Airflow/dbt|Integración directa para orquestación (Airflow) y transformación analítica (dbt).|
|🧪 Soporte para tests y validación|Puedes aplicar constraints (NOT NULL, UNIQUE, CHECK) y pruebas con dbt|
|🚀 Rendimiento|Capaz de soportar miles de registros y múltiples consultas para dashboards o notebooks.|
|📐 Escalabilidad|Puede escalar horizontalmente en la nube o replicarse si se decide hacer producción.|
|🛠️ Integración con Python|Soporte maduro vía `psycopg2`, `SQLAlchemy`, `pandas.to_sql`, etc.|


## 📋 Propuesta de tabla: `scopus_articles`

|Campo|Tipo SQL|Descripción|
|---|---|---|
|id|SERIAL PRIMARY KEY|Identificador interno único|
|title|TEXT NOT NULL|Título del artículo|
|authors|TEXT NOT NULL|Autores (string plano por ahora)|
|abstract|TEXT|Resumen|
|journal|TEXT NOT NULL|Nombre de la revista|
|year|INTEGER|Año de publicación|
|doi|TEXT UNIQUE|Identificador DOI|
|link|TEXT|URL a Scopus|
|source_query|TEXT|Término de búsqueda original|
|retrieved_date|DATE|Fecha de extracción del dato|
|exported_at|TIMESTAMP|Fecha de carga en PostgreSQL|