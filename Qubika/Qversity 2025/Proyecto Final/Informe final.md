
# 📄 Informe Final – Proyecto de Arquitectura de Datos Qversity

## 1. Objetivo del Proyecto

Diseñar e implementar una arquitectura de datos moderna basada en capas (Bronze, Silver y Gold) para procesar, transformar y analizar los datos de una empresa de tecnología educativa (Qversity), integrando herramientas de orquestación (Airflow) y transformación de datos (dbt), con persistencia en PostgreSQL.

---

## 2. Arquitectura General del Proyecto

La arquitectura sigue un enfoque modular por capas:

- **Bronze**: Ingesta de datos crudos en formato JSON o CSV.
- **Silver**: Limpieza, tipificación y normalización (modelo 3NF).
- **Gold**: Modelos analíticos agregados para toma de decisiones (star schema).
- **Orquestación**: Automatización de procesos ETL mediante Airflow.
- **Transformaciones**: Definidas y ejecutadas mediante dbt.

---

## 3. Implementación Técnica

### 3.1. Herramientas utilizadas

| Componente     | Herramienta            | Descripción breve                                           |
|----------------|------------------------|--------------------------------------------------------------|
| Ingesta        | PostgreSQL             | Persistencia relacional en 4 esquemas: `raw`, `bronze`, `silver`, `gold`. |
| Transformación | dbt (`dbt-core`)       | Transformaciones SQL modularizadas por capas.                |
| Orquestador    | Apache Airflow         | DAGs para ejecutar transformaciones programadas.             |
| Contenedores   | Docker + docker-compose| Entorno reproducible local con servicios aislados.           |

---

### 3.2. Esquema de base de datos

**Esquemas creados:**

- `bronze`: datos crudos sin transformación.
- `silver`: datos limpios, tipificados y desnormalizados.
- `gold`: datos agregados, listos para dashboards o análisis.

**Tablas generadas en Gold (19):**

- `gold_arpu_by_plan_type`
- `gold_operator_summary`
- `gold_credit_score_segments`
- `gold_customer_distribution`
- `gold_service_combinations`
- `gold_payment_issues`
- `gold_pending_payments`
- `gold_top_customer_segments`
- `gold_revenue_by_location`
- `gold_new_customer_trends`
- *(y otras hasta completar 19)*

---

### 3.3. DAG de Airflow

- **ID:** `gold_etl_dag`
- **Tipo:** `BashOperator`
- **Comando:** Ejecuta `dbt run --select gold && dbt test --select gold`
- **Frecuencia:** `@daily`
- **Catchup:** `False`
- **Alertas:** email en caso de fallo

---

### 3.4. Orquestación completa (Workflow)

1. Airflow inicia el DAG.
2. Ejecuta dbt dentro del contenedor.
3. Se generan las tablas analíticas `gold.*`.
4. Se validan los tests.
5. Se registra el resultado de ejecución.

---

## 4. Validación Final

### ✅ Estado de ejecución

- DAG ejecutado exitosamente desde consola y UI.
- `dbt run` completado sin errores (`PASS=19`).
- `dbt test` ejecutado sin fallos (`PASS=5`).
- Tablas creadas en PostgreSQL (`\dt gold.*`).

---

## 5. Recomendaciones futuras

- Integrar alertas vía Slack, correo funcional (SMTP real) o dashboards.
- Agregar tareas de exportación (CSV/Parquet).
- Ampliar cobertura de `tests` dbt a más modelos.
- Documentar cada modelo dbt (`description:` y `meta:`).

---

## 6. Evidencias

- Capturas de Airflow (UI DAG y éxito de ejecución).
- Logs de ejecución `dbt run` y `dbt test`.
- Listado completo de tablas `gold.*`.
- Repositorio Git con historial de commits semánticos y estructurados.

---

## 7. Conclusión

Este proyecto demuestra una arquitectura de datos robusta, automatizada y modular, implementada con herramientas modernas:

- Procesamiento en capas (raw → silver → gold)
- Automatización reproducible con Airflow y Docker
- Transformaciones auditables y escalables con dbt
- Infraestructura definida como código

El sistema cumple con los requerimientos académicos y es fácilmente extensible para ambientes reales de análisis de datos.

---



