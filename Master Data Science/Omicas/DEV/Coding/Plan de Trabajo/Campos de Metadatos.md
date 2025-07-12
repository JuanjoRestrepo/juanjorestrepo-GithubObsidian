
|Campo|Etiqueta DC/Extensión|Tipo de dato|Descripción / Valores permitidos|
|---|---|---|---|
|**Título**|dc:title|Texto libre|Nombre del recurso (p. ej. “Protocolo FTIR–45”).|
|**Autor / Creador**|dc:creator|Lista de textos|Investigador(es) responsable(s).|
|**Descripción**|dc:description|Texto largo|Resumen breve de contenido u objetivo.|
|**Fecha**|dc:date|Fecha (YYYY‑MM‑DD)|Fecha de creación o ejecución del experimento.|
|**Tipo de recurso**|dc:type|Lista desplegable|{“Protocolo”, “Dataset Crudo”, “Dataset Tratado”, “Informe ML”, “Publicación”, …}|
|**Técnica**|ext:technique|Lista desplegable|{“FTIR”, “Microscopía”, “Secuenciación”, “Espectroscopía Raman”, …}|
|**Equipo**|ext:equipment|Texto libre / lista|Nombre o modelo del equipo (p. ej. “Bruker Tensor II”).|
|**Formato**|dc:format|Lista desplegable|{“CSV”, “JSON”, “Jupyter Notebook”, “PDF”, “Word”, …}|
|**Identificador**|dc:identifier|Texto único|ID interno o URI (p. ej. “iOmicas–DS–20250701–001”).|
|**Palabras clave**|dc:subject|Lista de textos|Temas o palabras clave separadas por comas (“FTIR”, “análisis de tendencias”, …).|
|**Estado**|ext:status|Lista desplegable|{“Borrador”, “En revisión”, “Aprobado”}.|
|**Relaciones**|dc:relation|Referencia múltiple|IDs de recursos relacionados (protocolo → datasets → informe).|
|**Versión**|ext:version|Texto corto|Número o etiqueta de versión (“v1.0”, “v1.1”).|
|**Derechos / Acceso**|dc:rights|Lista desplegable|{“Acceso interno”, “Compartido Javeriana”, “Público”}.|
|**Proyecto / Fase**|ext:projectPhase|Lista desplegable|{“Concepción”, “Diseño”, “Implementación”, “Operación”}.|
|**Calidad de datos**|ext:dataQuality|Lista desplegable|{“Crudo”, “Depurado”, “Validado”}.|

