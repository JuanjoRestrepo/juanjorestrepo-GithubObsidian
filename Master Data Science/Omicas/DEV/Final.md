

# Informe de Avances del Proyecto Ómicas

**Fecha:** 31 de julio de 2025  
**Autor(es):** Juan José Restrepo Rosero.  
**Contexto:** Proyecto de sistematización y gestión de datos multiómicos en el semillero iÓMICAS

---

## 1. Introducción

El objetivo de este proyecto es construir un pipeline ETL reproducible y escalable, capaz de capturar datos de diversas técnicas ómicas (Scopus, Raman, FTIR, UV-Vis), limpiarlos, normalizarlos y cargarlos en un data warehouse (PostgreSQL), de modo que puedan consumirse fácilmente para análisis posteriores y modelado.

---

## 2. Arquitectura General


![[Diagram_Omicas.png|centered]]


**Descripción de capas**:  
- **Bronze Layer**: Extracción de datos crudos desde APIs (Scopus) o archivos locales (Raman, FTIR, UV-Vis), almacenándolos en JSON/CSV en MinIO o volumen local.  
- **Silver Layer**: Proceso de limpieza y normalización genérica (`clean_data`), que transforma los crudos en CSV listos para análisis.  
- **Gold Layer**: Carga de los CSV limpios en tablas en PostgreSQL mediante `load_to_postgres`, creando la zona de consumo del data warehouse.

**Orquestación**: Airflow gestiona la ejecución diaria de las tareas del DAG `omicas_pipeline`, con dependencias claras extract → clean → load.

---

## 3. Estado Actual

1. **Extracción**  
   - Scopus y Raman se extraen correctamente (tareas `extract_scopus`, `extract_raman` en verde).  
   - FTIR y UV-Vis presentan errores de formato; estamos adaptando los scripts `extract_ftir.py` y `extract_uvvis.py`.

2. **Limpieza**  
   - La función genérica `clean_data` unifica el proceso de normalización.  
   - Ajustes pendientes para leer JSON de Scopus y CSV de espectros con sus columnas específicas.

3. **Carga**  
   - El módulo `load_to_postgres` se encuentra operativo; las tablas `scopus` y `raman` están creadas y pobladas.  
   - Verificación de integridad de datos y definición de índices por hacer.

---

## 4. Próximos Pasos

1. **Corregir extractores FTIR/UV-Vis** para que generen CSV con columnas estandarizadas.  
2. **Incorporar MinIO** como almacenamiento de capa Bronze y Silver; actualizar tareas Airflow para cargar/descargar desde buckets S3.  
3. **Integrar dbt** post-carga:  
   - Modelar transformaciones de negocio (vistas, agregaciones).  
   - Añadir tests y documentación automática.  
4. **Desarrollo de pruebas unitarias** y CI/CD para el pipeline.  
5. **Dashboard de monitoreo**: desplegar una interfaz (Looker Studio o similar) que consuma directamente las tablas Gold.

---

## 5. Conclusión

Se ha establecido la base de un pipeline modular y reproducible usando Python, Airflow, Docker, MinIO y PostgreSQL. La arquitectura en capas facilita la trazabilidad y la calidad de los datos. Con las correcciones de los extractores faltantes y la incorporación de dbt, el sistema estará preparado para soportar análisis avanzados multiómicos y flujos de trabajo de machine learning.

---

**Anexos**  
- Snippets de código relevantes  
- Logs de ejecución  
- Estructura de ficheros  
- Mapa de dependencias Airflow  
