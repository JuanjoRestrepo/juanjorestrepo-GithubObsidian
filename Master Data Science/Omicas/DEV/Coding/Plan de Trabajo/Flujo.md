

### ✅ **1. Tipos de información a almacenar**

|Tipo de recurso|Ejemplos|
|---|---|
|**Documentos**|Protocolos, reportes, actas, planes de trabajo, PDFs, Word, etc.|
|**Código y modelos ML**|Scripts Python, notebooks Jupyter, modelos `.pkl` o `.h5`|
|**Datos experimentales crudos**|Archivos CSV de equipos FTIR, microscopía, espectroscopía, etc.|
|**Datos derivados o transformados**|Datasets limpios, normalizados, listos para análisis|
|**Material complementario**|Presentaciones, imágenes, videos, papers|

### ✅ **2. Requerimientos técnicos y operativos**

|Requisito|¿Por qué es importante?|
|---|---|
|Control de versiones|Para asegurar trazabilidad de cambios|
|Metadatos personalizados|Para permitir búsquedas, filtrado y vinculación entre recursos|
|Accesibilidad para el equipo|Que los investigadores y estudiantes puedan cargar y consultar|
|Permisos y seguridad|Protección según tipo de usuario (coordinador, colaborador, etc.)|
|Escalabilidad|Posibilidad de crecer conforme haya más datos|
|Integración con pipelines de ML|Para conectar fácilmente con modelos, scripts y datos|


### ✅ **3. Propuesta de arquitectura de almacenamiento híbrida para iÓmicas**

| Componente                                 | Herramienta propuesta                                | Ubicación sugerida                                  | Finalidad específica                                             |
| ------------------------------------------ | ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------- |
| 📁 **Gestión documental estructurada**     | **Nextcloud** o **Alfresco**                         | Servidor de la Javeriana / Omicas                   | Para almacenar documentos con estructura de carpetas y metadatos |
| 🧠 **Repositorio de código y modelos**     | **GitLab + Git LFS**                                 | Servidor privado o GitLab institucional             | Versionado de scripts, notebooks y modelos entrenados            |
| 📊 **Base de datos de datos crudos**       | **InfluxDB** (ya usado) o **PostgreSQL + Timescale** | Infraestructura de laboratorio o nube universitaria | Almacenamiento estructurado de datos de sensores y equipos       |
| 🧪 **Repositorio académico interoperable** | **DSpace** o **EPrints**                             | (opcional, si la universidad lo permite)            | Publicación formal de resultados y datos con DOI, acceso abierto |
| 📈 **Análisis y dashboards**               | Superset / Power BI (opcional)                       | Local o nube                                        | Visualización de tendencias derivadas de los modelos ML          |



### 📦 Ejemplo concreto de flujo

1. El investigador realiza un experimento y guarda el resultado como CSV → lo sube a **Nextcloud** en la carpeta “Datos Crudos → Técnica FTIR”.
    
2. El archivo se registra con metadatos: fecha, autor, técnica, equipo, estado.
    
3. Un script de preprocesamiento en **GitLab** se conecta al repositorio, limpia los datos y los deja en “Datos Tratados”.
    
4. El modelo ML entrenado también se versiona en **GitLab** y documenta su relación con los datos originales.
    
5. El informe generado se guarda en **Nextcloud** y vincula los IDs de datos y scripts usados.
    
6. (Opcional) Una versión final del informe y dataset se publica en **DSpace** con DOI para uso científico.


