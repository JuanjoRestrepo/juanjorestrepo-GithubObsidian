# Plan de Trabajo y Seguimiento

## 1. Definición del esquema de metadatos y salida
- [x] **Crear JSON Schema**  
  - Descripción: Definir `scopus_schema.json` con todos los campos necesarios (`title`, `authors`, `year`, `doi`, `keywords`, `related_protocol_id`, etc.)  
- [ ] **Revisar y validar el esquema**  
  - Descripción: Corroborar tipos, longitudes y explicaciones de cada campo; asegurar que cubra todos los requerimientos.  

## 2. Pipeline ETL ligero para ingestión en tu repositorio
- [ ] **Escribir DAG/Skript de Airflow**  
  - Descripción: Orquestar tareas de extracción (`fetch_scopus_articles()`), transformación y carga.  
- [ ] **Implementar validación con JSON Schema**  
  - Descripción: Integrar paso que valide cada JSON contra `scopus_schema.json`.  
- [ ] **Mapear y limpiar campos**  
  - Descripción:  
    - Renombrar campos (p.ej. `dc:title` → `title`).  
    - Limpiar texto y extraer keywords.  
- [ ] **Carga a MinIO/Nextcloud**  
  - Descripción:  
    - Subir los JSON finales al bucket S3/MinIO.  
    - Registrar metadatos vía API en tu base documental.  

## 3. Generación automática de notas Markdown para Obsidian
- [ ] **Crear función `export_to_obsidian()`**  
  - Descripción: Iterar sobre el DataFrame y generar un `.md` por artículo con frontmatter YAML.  
- [ ] **Estructurar carpetas en Obsidian**  
  - Descripción: Organizar bajo `Bibliografía/Raman`, `Bibliografía/FTIR`, `Bibliografía/UVVis`, etc.  
- [ ] **Integrar paso en el pipeline**  
  - Descripción: Añadir al DAG el “export_to_obsidian()” tras la transformación.  

## 4. Diseño del repositorio central e integración
- [ ] **Configurar almacenamiento (MinIO o bucket en la nube)**  
  - Descripción: Crear el bucket y definir estructura de rutas.  
- [ ] **Definir roles y políticas de acceso**  
  - Descripción: Establecer quién puede leer, escribir y aprobar.  
- [ ] **Desarrollar microservicio (Flask/FastAPI)**  
  - Descripción:  
    - Endpoints de búsqueda (año, técnica, autor).  
    - Endpoint para descarga de registros.  
- [ ] **Desplegar en local para pruebas**  

## 5. Construcción de casos de uso analíticos
- [ ] **Crear Jupyter Notebook piloto**  
  - Descripción: Análisis de conteo de artículos por año y técnica.  
- [ ] **Desarrollar dashboard simple**  
  - Descripción: Usar Grafana o Streamlit conectado a tu API para mostrar:  
    - Series temporales de publicaciones.  
    - Redes de coautoría.  
- [ ] **Presentar resultados en taller interno**  

## 6. Programación y monitorización
- [ ] **Programar ejecución periódica**  
  - Descripción: Configurar en Airflow (o cron) para que corra mensual/trimestralmente.  
- [ ] **Configurar alertas**  
  - Descripción: Notificaciones por correo o Slack ante fallos o cambios significativos.  
- [ ] **Documentar el flujo completo**  
  - Descripción: Añadir diagrama, README y manual de operación al repositorio.  

---

## Próximo paso inmediato
- [ ] Seleccionar bloque para comenzar:  
  - “Definir JSON Schema y validaciones”  
  - “Generar notas Markdown automáticamente”  
  - Otro: ______________________

