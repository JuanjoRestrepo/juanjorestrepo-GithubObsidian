
# ¿Qué es MinIO?  
MinIO es una implementación de almacenamiento de objetos compatible con la API de Amazon S3, pero que corre de manera _self-hosted_ y es completamente gratuita bajo licencia Apache 2.0. Con MinIO puedes tener tu propio “S3” en tu infraestructura (o incluso en tu laptop), sin coste de uso ni cuotas por volumen de datos.

# ¿Para qué sirve el cliente `minio` en Python?
La librería `minio` en `requirements.txt` te permite, desde tus scripts (ETL, validaciones, etc.), conectar, subir y descargar objetos (archivos crudos, resultados pesados, modelos serializados…) a tu servidor MinIO tal como lo harías a un bucket de S3. Ejemplo de uso:



- **¿Debo usarlo en el proyecto?**  
    Sí, Se recomiendA:
    1. **Guardar los datos “bronce”** (raw) en MinIO para no saturar la base de datos ni el contenedor de Airflow.
        
    2. **Versionar grandes outputs** (modelos entrenados, reportes, dashboards exportados).
        
    3. **Compartir artefactos** entre diferentes DAGS o incluso entre proyectos.
        
- **Costes y licencias**
    
    - MinIO es **gratuito**, no hay costes de uso ni tokens de AWS.
        
    - Solo se paga la infraestructura donde lo ejecutes (tu propio servidor o tu máquina local).

