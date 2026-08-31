
# Informe de Avance del Proyecto OMICAS

**Fecha:** 2025-07-31

---

## 1. Resumen Ejecutivo

- **Objetivo**: Montar un pipeline ETL en Airflow que extraiga datos de Scopus, espectros Raman, FTIR y UV-Vis, los limpie, y los cargue en PostgreSQL; además de preparar el entorno Docker con MinIO.
- **Estado actual**:  
  - ✅ Contenedores Docker levantados (Postgres, PgAdmin, MinIO, Airflow).  
  - ✅ `requirements.txt` actualizado con librerías adicionales (modelado, XAI, MinIO).  
  - ✅ DAG `omicas_pipeline` configurado y sin errores de importación.  
  - ⚠️ Tareas de limpieza (`clean_*`) y extracción de FTIR/UV-Vis fallan por ausencia de datos de muestra.  

---

## 2. Arquitectura y Herramientas

| Componente   | Imagen / Versión       | Puerto  | Volumen       |
|-------------:|:-----------------------|:--------|:--------------|
| PostgreSQL   | `postgres:15`          | 5432    | `pg_data`     |
| PgAdmin      | `dpage/pgadmin4`       | 80      | —             |
| MinIO Server | `minio/minio:latest`   | 9000    | `minio_data`  |
| Airflow      | custom `Dockerfile.airflow` (2.10.3) | 8081→8080 | Proyecto + DAGs + Logs |

**Stack de librerías principales**  
- ETL & DB: `requests`, `pandas`, `sqlalchemy`, `psycopg2`  
- Orquestación: `apache-airflow==2.10.3`, `apache-airflow-providers-postgres`  
- Modelado & XAI: `numpy`, `scikit-learn`, `xgboost`, `shap`, `lime`  
- Almacenamiento objetos: `minio`

---

## 3. Pipeline ETL en Airflow

```mermaid
flowchart LR
    subgraph BRONZE
      A1[extract_scopus] --> A2[raw_scopus.json]
      B1[extract_raman]  --> B2[raman.csv]
      C1[extract_ftir]   --> C2[ftir.csv]
      D1[extract_uvvis]  --> D2[uvvis.csv]
    end
    subgraph SILVER
      A2 --> A3[clean_scopus → scopus.csv]
      B2 --> B3[clean_raman → raman.csv]
      C2 --> C3[clean_ftir → ftir.csv]
      D2 --> D3[clean_uvvis → uvvis.csv]
    end
    subgraph GOLD
      A3 --> A4[load_scopus → table `scopus`]
      B3 --> B4[load_raman  → table `raman`]
      C3 --> C4[load_ftir   → table `ftir`]
      D3 --> D4[load_uvvis  → table `uvvis`]
    end

```



```mermaid
flowchart TB
  subgraph Airflow
    direction TB
    extract_scopus --> clean_scopus --> load_scopus
    extract_raman   --> clean_raman   --> load_raman
    extract_ftir    --> clean_ftir    --> load_ftir
    extract_uvvis   --> clean_uvvis   --> load_uvvis
  end

  subgraph ETL [ ETL Pipeline ]
    direction LR
    Airflow
  end

```
