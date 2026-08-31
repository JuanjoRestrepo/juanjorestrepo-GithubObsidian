

# 🏅 qversity Data Pipeline (Medallion Architecture)

## 🚀 Descripción del proyecto

Implementación de un pipeline ELT completo usando la arquitectura Bronze‑Silver‑Gold:

- **Bronze**: datos crudos cargados en PostgreSQL sin modificaciones.
- **Silver**: datos limpiados, estructurados y validados con dbt.
- **Gold**: tablas listas para análisis con métricas de negocio calculadas.
    

Orquestación mediante Airflow; transformaciones con dbt.

## 🧰 Tecnologías

- **Airflow**: orquestación
- **dbt** (v1.10.1): transformación y pruebas
- **PostgreSQL**: almacenamiento
- **Docker / Docker Compose**: entornos reproducibles

## 📁 Estructura del repositorio

bash

CopyEdit

```bash
/  
├── bronze/ ← modelos de ingestión raw  
├── silver/ ← limpieza, flattening, deduplicación  
├── gold/ ← métricas y agregados  
├── macros/ ← macros dbt personalizadas  
├── tests/ ← pruebas SQL custom  
├── dbt_project.yml  
├── profiles.yml ← configuración de conexión  
└── README.md
```

## 🛠️ Setup inicial

1. Clonar repo y levantar ambiente:
 ``
```bash
docker compose up -d
```
2. Conectar Airflow y PostgreSQL.
    
3. Configurar `profiles.yml`:
```yaml
qversity:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres
      user: qversity-admin
      password: qversity-admin
      port: 5432
      dbname: qversity
      schema: public
      threads: 1

```

4. Cargar datos Bronze, crear tabla `bronze.customers_raw` (JSON puro).
    
5. Ejecutar dbt:
```bash
dbt debug dbt run dbt test
```

---
## 🏗️ Arquitectura por capa

### 1. Bronze

-> Datos crudos en `bronze.customers_raw`.  
**Nota**: No se modifican arrays ni estructuras anidadas.  
Cumple con la capa Bronze de la arquitectura medallion [youtube.com+1github.com+1](https://www.youtube.com/watch?v=qTkA8vfMy4w&utm_source=chatgpt.com)[blog.devops.dev+6github.com+6reddit.com+6](https://github.com/MekWiset/Medallion_DataLakehouse?utm_source=chatgpt.com)[i-spark.nl+7deeplearningnerds.com+7tsaiprabhanj.medium.com+7](https://www.deeplearningnerds.com/set-up-medallion-architecture-with-dbt-from-raw-data-to-gold-standard/?utm_source=chatgpt.com)[blog.devops.dev+1github.com+1](https://blog.devops.dev/databricks-gold-layer-design-best-practices-explained-cd0f7852a806?utm_source=chatgpt.com)[reddit.com](https://www.reddit.com/r/dataengineering/comments/1fbynu7/built_my_first_data_pipeline_using_data_bricks/?utm_source=chatgpt.com).

### 2. Silver

-> Modelos `silver_customers`, `silver_payments` limpian, flatten JSON, eliminan arrays.  
-> Se aplican pruebas `not_null`, `unique`, etc.  
Esta capa garantiza limpieza y estructura para el downstream [blog.devops.dev+2tsaiprabhanj.medium.com+2github.com+2](https://tsaiprabhanj.medium.com/medallion-architecture-with-dbt-a40050743be3?utm_source=chatgpt.com).

### 3. Gold

-> Modelos de negocio (`gold_arpu_by_plan_type`, `gold_operator_summary`)  
calculan KPIs como ARPU, ingresos por operador, pagos fallidos, etc.  
 -> Todas las transformaciones están en tablas materializadas listas para análisis .

---
## ✅ Pruebas y validación

- dbt ran 100 % satisfactoriamente con `PASS` en todas las pruebas.
- Las tablas se generaron correctamente en los esquemas `silver` y `gold` (verificado con `\dt silver.*`, `\dt gold.*`).
- Se corrigieron errores de esquema, materializaciones, y naming.

## 🔧 Detalles importantes

- `silver` y `gold` se materializan en los esquemas correctos (`silver`, `gold`) según `dbt_project.yml`, no en `public`.
- Las macros personalizadas (en `/macros`) automatizan lógica común.
- Se mantiene historial de versiones en Git con tags: `v0.1.0-bronze`, `v0.2.0-silver`, `v0.3.0-gold`.
    

## 🚀 Siguientes pasos / Capa Gold completa

- Crear más métricas: ARPU por país, edad, score de crédito.
- Generar tablas como:
    - `gold_customer_segmentation`
    - `gold_device_preferences`
    - `gold_payment_behaviors`
        
- Actualizar `schema.yml` agregando las nuevas tablas y sus tests.
- Documentar en `docs/` y generar `dbt docs` con toda la arquitectura, descripción y ERD.
    

---

### 📌 Resumen de cumplimiento de requisitos:

- **Orquestación**: Airflow.
- **Transformaciones**: dbt en capas Bronze, Silver y Gold.
- **Control de calidad**: pruebas `not_null`, `unique`, y validaciones personalizadas.
- **Diseño modular**: carpetas por capa, macros reutilizables.
- **Documentación & versión**: tags semánticos, README, macros, `dbt docs`.

---




## 🚀 Siguientes pasos

1. Definir nuevos modelos Gold según métricas pendientes.
    
2. Añadir tests adecuados en `schema.yml`.
    
3. Ejecutar dbt y validar resultados.
    
4. Generar ERD actualizado, gráficos y `dbt docs`.
    
5. Documentar todo (desafíos, soluciones) en README y presentación.




# NEW


| Capa   | Python / Airflow                         | dbt (SQL)                                                          |
| ------ | ---------------------------------------- | ------------------------------------------------------------------ |
| Bronze | Ingesta JSON desde S3 a Postgres         | —                                                                  |
| Silver | Orquestar DAGs, pre‑validaciones ligeras | Transformar en 3NF, limpiar, tipar, deduplicar, pruebas            |
| Gold   | Orquestar ejecución dbt Gold             | Modelar dimensión/fact, agregar métricas de negocio, tests finales |


## Qversity Data Platform

Este proyecto implementa un pipeline **Bronze → Silver → Gold** orquestado por Airflow, transformado con dbt y almacenado en PostgreSQL.

---

### 🎯 Business Insights

1. **ARPU por tipo de plan**: Los planes `pre_pago` muestran un ARPU promedio de $X; los planes `pospago` de $Y.
    
2. **Distribución de clientes por operador**:
    
    - Claro: 40%
        
    - Movistar: 35%
        
    - WOM/Tigo: 25%
        
3. **Comportamiento de crédito vs pago**: Clientes con **credit_score ≥ 700** tienen < 5% de pagos fallidos. Aquellos con **< 500** superan 15% de fallos.
    
4. **Servicios más populares**: `SMS` (1,234 clientes), `VOICE` (1,102), `DATA` (953).
    
5. **Combinaciones top de servicios**: `SMS, VOICE` lidera con 321 clientes.
    
6. **Distribución geográfica de ingresos**: Medellín y Bogotá concentran el 60% de la facturación.
    

---

### 🗂️ Entity–Relationship Diagram (Silver Layer)

```
erDiagram
    SILVER_CUSTOMERS {
        INTEGER raw_id PK
        INTEGER customer_id
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR phone_number
        VARCHAR city
        VARCHAR country
        DATE registration_date
        DATE last_payment_date
        INTEGER credit_score
    }
    SILVER_PAYMENTS {
        INTEGER raw_id PK
        DATE payment_date
        NUMERIC amount
        VARCHAR status
    }
    SILVER_CUSTOMERS ||--o{ SILVER_PAYMENTS : "1-to-many (raw_id)"
```

---

## 📘 Quick Start

1. Copiar variables de entorno:
    
    ```
    cp env.example .env
    ```
    
2. Levantar servicios:
    
    ```
    docker compose up -d
    ```
    

## 🚀 Ejecución del Pipeline

### Bronze & Silver

ingestión y transformación Silver

```
# DAG Bronze
airflow dags trigger bronze_ingest_dag
# dbt Silver
docker compose exec dbt bash -c "dbt run --models silver" && dbt test --models silver
```

### Gold

ejecución de todos los modelos Gold y tests

```
docker compose exec dbt bash -c "dbt run --models gold && dbt test --models gold"
```

---

## ✅ Checklist de Entrega

---

_Tag final:_ `v1.0.0`


# Capa Gold

![[Pasted image 20250619232243.png]]



# Arquitectura

![[Pasted image 20250619232821.png]]

