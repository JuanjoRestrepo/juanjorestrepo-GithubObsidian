

Para almacenar y gestionar de manera óptima los distintos tipos de datos de nuestro flujo Medallion, te propongo la siguiente combinación de bases de datos y almacenes:

1. **InfluxDB** (Series temporales – Bronze layer)  
    ─ **Por qué**: las salidas de los equipos de espectroscopía (Raman, FTIR, UV-Vis) son esencialmente series de intensidad vs. número de onda/longitud de onda. InfluxDB está pensado para series temporales y permite consultas muy ágiles sobre rangos, downsampling, retención automática de datos y etiquetas (tags) para metadatos básicos (técnica, muestra, fecha).  
    ─ **Qué guardar**:  
    • Todos los espectros “raw” justo como los exporta el instrumento (con timestamp, sample_id, técnica).  
    • Columnas de metadata ligeras (técnica, ID de experimento, operador).
    
2. **MinIO** (Objetos S3-compatibles – Bronze/Gold layers)  
    ─ **Por qué**: para archivos más pesados o no estructurados (por ejemplo, archivos binarios SPC/JDX, reportes completos, imágenes de espectros), MinIO te da un bucket S3 local, fácil de versionar y con políticas de retención.  
    ─ **Qué guardar**:  
    • Copias de seguridad de los CSV/JSON “raw” (bronze/raw_scopus.json).  
    • Ficheros de errores y reportes intermedios.
    
3. **PostgreSQL** (Relacional – Silver/Gold layers)  
    ─ **Por qué**: para los datos ya validados, limpios y enriquecidos (metadatos de artículos, parámetros de muestras, resultados de pipelines ML), una base relacional permite consultas complejas (joins entre tablas de protocolos, artículos, experimentos). Además, PostgreSQL con TimescaleDB puede actuar igualmente como base de series temporales si lo prefieres.  
    ─ **Qué guardar**:  
    • La tabla `scopus_articles` con los campos que definiste en el schema (título, autores, resumen, año, doi, link, fuente, fecha).  
    • Tablas de “protocolos”, “experimentos”, “muestras” y relaciones entre ellas.  
    • Vistas/materialized views para casos de uso analítico (Gold layer).





### Flujo de almacenamiento

1. **Bronze**
    - `extract_scopus.py` → escribe raw JSON en MinIO/FS y serie de espectros en InfluxDB.
        
2. **Silver**
    - `clean_scopus.py` → lee raw JSON de MinIO, parsea y valida, luego write a PostgreSQL (`scopus_articles`), y opcionalmente series ya etiquetadas en InfluxDB.
        
3. **Gold**
    - `export_scopus.py` → genera CSV finales o construye vistas en PostgreSQL, exporta dashboards, notebooks, etc.
        

Con esta arquitectura atenderás:
- **Agilidad** en ingestión de series (InfluxDB).
- **Almacenamiento seguro de objetos** (MinIO)
- **Potencia relacional y analítica** (PostgreSQL).


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