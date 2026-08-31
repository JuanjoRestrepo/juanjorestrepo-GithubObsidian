---
title: "Opción B - Cronograma de Ejecución y Plan de Trabajo"
date: 2026-08-27
tags:
  - caso-estudio
  - plan-trabajo
  - cronograma
  - rpa
status: evergreen
---

# 📅 Plan de Trabajo y Cronograma de Ejecución — Opción B

Plan de trabajo estructurado para la implementación, extracción, procesamiento y defensa del sistema de Competitive Intelligence.

---

## 🗓️ Desglose Diario de Actividades

| Jornada | Enfoque Principal | Tareas Críticas de Ingeniería | Entregable del Día |
| :--- | :--- | :--- | :--- |
| **Día 0 (9 Oct)** | **Definición & Scaffolding** | Configurar el alcance (3 plataformas, 3 KPIs), estructurar el entorno virtual con `uv`, redactar `Dockerfile` y crear el archivo `addresses.csv`. | Repositorio base y entorno listo para ejecución. |
| **Día 1 (10 Oct)** | **Desarrollo de Scrapers & Ingesta** | Implementar `resolver.py` y los módulos de extracción de Rappi y Uber Eats con Playwright; ejecutar primera corrida de captura. | Dataset crudo inicial en `results.json` con capturas. |
| **Día 2 (11 Oct)** | **ETL & Normalización** | Desarrollar funciones de limpieza (`sanitize_number`), matching de productos y primeros análisis exploratorios en Jupyter Notebook. | Notebook con EDA y métricas de completitud. |
| **Día 3 (12 Oct)** | **Análisis Estadístico & Calidad** | Calcular distribuciones de precios, boxplots comparativos, heatmaps geográficos y auditoría de métricas de calidad de parsing. | Gráficos ejecutivos y reporte cuantitativo finalizado. |
| **Día 4 (13 Oct)** | **Presentación & Ensayo** | Diseñar diapositivas de sustentación en PDF, documentar el `README.md` final, estructurar `demo_script.md` y realizar simulacros de defensa. | Entrega final y preparación completa para el panel. |