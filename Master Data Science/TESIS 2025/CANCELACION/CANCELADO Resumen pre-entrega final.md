---
date: 2025-06-08
tags:
  - Tesis
  - Master
  - Maestria
---


## ✅ Resumen del Notebook Actual

### Sección 0: Dependencias y Configuración

- Instalación de librerías (`rapidfuzz`, `networkx`, `plotly`, `umap-learn`, `pymannkendall`, entre otras).
    
- Montaje de Google Drive y carga del CSV (`Analisis Documentos Tesis BD.csv`).
    

### Sección 1: Inspección Inicial (EDA)

- Visualización de dimensiones, tipos, valores nulos.
- Gráficos de distribución por año, por número de autores.

### Sección 2: Limpieza y Preprocesamiento Avanzado

- Desambiguación de nombres de autores e instituciones con `rapidfuzz`.
- Imputación de valores faltantes (numéricos y categóricos).
- Normalización de texto (keywords, barriers).

### Sección 3: Análisis Bibliométrico

- Evolución temporal + prueba de tendencia Mann–Kendall.
- Construcción y análisis de la red de coautoría (métricas: degree, betweenness, eigenvector; detección de comunidades).
- Análisis de revistas y quartiles.
- Análisis de palabras clave con UMAP.
- Modelos temáticos: LDA vs NMF + términos destacados.


### Sección 4: Barreras

- Extracción y frecuencia de las principales barreras.
- Gráfico y análisis interpretativo basado en tus aportes.

### Sección 5: Visualizaciones Interactivas

- Gráficos dinámicos con Plotly (línea temporal, mapa de países/facultades).
- Exportación de resultados (ej.: grafo a GraphML).


---

## 🧭 Próximos Pasos / ¿Qué Revisar?

1. **¿En qué sección te gustaría retomar?**
    - EDA: ¿Grafiquemos nuevo indicador, variable o cruce de datos?
    - Modelado: ¿Creamos el dashboard interactivo o refinamos LDA/NMF?
    - Red de coautoría: ¿Visualización interactiva o detección de comunidades avanzada?

2. **¿Qué necesitas ahora?**
    - ¿Quieres que ejecute una celda específica para recordarla?
    - ¿Prefieres acceder a un diagrama general del notebook actualizado?
    
3. **¿Visualizaciones o informes?**
    - ¿Generamos una versión PDF/Dash o mejoramos los markdown con detalles?


