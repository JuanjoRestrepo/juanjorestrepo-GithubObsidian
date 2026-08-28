---
title: "MOC - Caso de Estudio Rappi: Estrategias Técnicas y Arquitectura"
date: 2026-08-27
tags:
  - caso-estudio
  - arquitectura
  - moc
  - rpa
  - llm
  - data-science
status: evergreen
---

# 🗺️ Map of Content (MOC) — Caso de Estudio Técnico Rappi

Bienvenido a la base de conocimiento central para la preparación, desarrollo y defensa del **Caso Técnico Rappi**. Este espacio consolida la evaluación técnica, diseño de arquitectura, planes de trabajo y guiones de sustentación divididos en dos vías estratégicas principales: **Opción A** (Análisis Estadístico + RAG/LLM) y **Opción B** (Competitive Intelligence vía RPA/Playwright).

---

## 🧭 Índice de Navegación Rápida

```mermaid
mindmap
  root((Caso Rappi))
    MOC Central
      [[Caso de Estudio Rappi - MOC]]
    Opción A: Analytics & RAG
      [[1. MVP|MVP & Entregables]]
      [[2. Resumen rápido del dataset|Perfilado Dataset]]
      [[3. Plan de Trabajo|Estrategia & Defensa]]
      [[5. Tech Stack|Tech Stack Opción A]]
      [[6. Riesgos|Matriz de Riesgos]]
      [[7. Cronograma|Cronograma Ejecución]]
      [[Diagrama Arquitectura|Arquitectura RAG]]
      [[Objetivo|Bloque 1: EDA]]
      [[Plan de Trabajo|Bloque 2: Insights]]
    Opción B: RPA & Competitive Intelligence
      [[1. Comparación Opciones|Matriz Comparativa]]
      [[2. Alcance|Alcance & MVP]]
      [[3. Tech Stack|Tech Stack Opción B]]
      [[4. Métricas y Criterios|Métricas de Calidad]]
      [[5. Presentacion|Estructura Defensa]]
      [[7. Riesgos y Complicaciones|Gestión de Riesgos]]
      [[Arquitectura|Arquitectura Scraping]]
      [[Plan de Trabajo|Cronograma Opción B]]
      Diapositivas y Guiones
        [[Guion|Guion Oficial Diapositivas]]
        [[GUION BORADDOR|Borrador Detallado & Q&A]]
      Documentación de Scripts
        [[RUN|Guía de Ejecución CLI]]
        [[multi_platform_scraper|Orquestador Multi-Plataforma]]
        [[resolver.py|Heurística de Resolución]]
        [[rappi_scrapper.py|Módulo Heurística Rappi]]
        [[playwright main.py|Extracción & DOM]]
        [[utils.py|Módulo de Utilidades]]
```

---

## ⚖️ Matriz de Decisión Arquitectónica: Opción A vs. Opción B

| Criterio de Evaluación | Opción A: LLM & Business Insights (RAG) | Opción B: Competitive Intelligence (RPA) |
| :--- | :--- | :--- |
| **Núcleo Técnico** | Modelado tabular, detección de anomalías, embeddings, Vector DB (FAISS), RAG estructurado (JSON). | Web scraping dinámico con Playwright, ingeniería inversa de API/XHR, normalización de entidades (`RapidFuzz`). |
| **Entradas de Datos** | Dataset transaccional cerrado (`RAW_INPUT_METRICS`, `RAW_ORDERS`, `RAW_SUMMARY`). | Muestreo geoespacial en vivo (`addresses.csv`), captura de DOM dinámico e interceptación de red. |
| **Auditabilidad** | Evaluación heurística/humana ($N=30$), métricas de cobertura y precisión factual contra alucinaciones. | Evidencias deterministas: Capturas de pantalla (`data/screenshots/`), dumps JSON (`__NEXT_DATA__`, XHR). |
| **Facilidad de Defensa** | Requiere justificar mitigación de alucinaciones, diseño de prompts y costo/latencia de inferencia. | Altamente defendible: Métricas duras (éxito de parsing, cobertura, comparativas directas de precios y fees). |
| **Recomendación** | Estrategia de alto impacto conceptual; ideal si el rol está orientado a IA generativa y producto. | **Estrategia recomendada para sustentación técnica**: Demuestra solidez en Data Engineering, scraping e insights de negocio inmediatos. |

---

## 📂 Estructura Detallada de la Bóveda

### 🅰️ Opción A: Inteligencia Aumentada & RAG
Enfocada en el análisis avanzado de datos temporales/tabulares de órdenes y métricas operativas de Rappi, complementado con una capa generativa para responder preguntas de negocio con respaldo factual.

1. **Definición y Alcance:**
   - [[1. MVP|1. MVP]]: Requerimientos mínimos y entregables defensibles.
   - [[2. Resumen rápido del dataset|2. Resumen rápido del dataset]]: Análisis estructural de las hojas de datos.
   - [[4. MVP Entregable|4. MVP Entregable]]: Checklist de aceptación de entregables.
2. **Estrategia y Planificación:**
   - [[3. Plan de Trabajo|3. Plan de Trabajo]]: Estrategia de grounding, salida JSON estructurada y métricas de evaluación.
   - [[5. Tech Stack|5. Tech Stack]]: Selección tecnológica justificada (Python, Pandas, FAISS, Streamlit, Docker).
   - [[6. Riesgos|6. Riesgos]]: Mitigación de alucinaciones, cuotas de API y gestión del tiempo.
   - [[7. Cronograma|7. Cronograma]]: Plan de ejecución de 4 días.
3. **Desarrollo Técnico:**
   - [[Diagrama Arquitectura|Diagrama de Arquitectura RAG]]: Pipeline de 4 fases (Data Pipeline → Insights Engine → RAG → App Demo).
   - [[Objetivo|Bloque 1 - Objetivo EDA]]: Exploración de datos y artefactos visuales.
   - [[Plan de Trabajo|Bloque 2 - Plan de Trabajo]]: Flujo analítico y generación de los Top 5 insights.

---

### 🅱️ Opción B: Competitive Intelligence & Extracción RPA
Diseño e implementación de un pipeline de inteligencia competitiva para comparar precios, tarifas de entrega (*delivery fee*) y tarifas de servicio (*service fee*) entre Rappi, Uber Eats y DiDi Food.

1. **Definición y Comparativa:**
   - [[1. Comparación Opciones|1. Comparación Opciones]]: Análisis de ventajas, riesgos y justificación de selección.
   - [[2. Alcance|2. Alcance]]: Definición del MVP (3 competidores $\times$ 3 dimensiones).
   - [[3. Tech Stack|3. Tech Stack]]: Justificación técnica (Playwright, Pandas, RapidFuzz, Docker).
   - [[4. Métricas y Criterios|4. Métricas y Criterios]]: KPIs de evaluación (Coverage, Parsing Accuracy, Freshness).
   - [[7. Riesgos y Complicaciones|7. Riesgos y Complicaciones]]: Mitigación de bloqueos anti-bot y consideraciones legales (`robots.txt`).
   - [[Arquitectura|Arquitectura General Opción B]]: Diagrama de flujo de datos completo y descripción módulo a módulo.
   - [[Plan de Trabajo|Plan de Trabajo Opción B]]: Cronograma de desarrollo.

2. **Guiones de Presentación y Sustentación:**
   - [[Guion|Guion Oficial por Diapositivas]]: Script paso a paso para la defensa técnica (10–12 minutos).
   - [[GUION BORADDOR|Guion Extendido y Preguntas Frecuentes]]: Guion detallado con análisis de gráficos y banco de respuestas para Q&A técnico.

3. **Documentación Conceptual de Scripts:**
   - [[RUN|Guía de Ejecución CLI]]: Comando de terminal y flags de ejecución.
   - [[multi_platform_scraper|Orquestador Multi-Plataforma]]: Explicación arquitectónica del script `multi_platform_scraper.py`.
   - [[resolver.py|Resolver de URLs]]: Algoritmo de puntuación y resolución heurística de restaurantes.
   - [[rappi_scrapper.py|Heurística de Consultas Rappi]]: Módulo tipado para construcción de queries de búsqueda.
   - [[playwright main.py|Estrategias de Extracción DOM/XHR]]: Desglose de extracción por DOM, XHR y `__NEXT_DATA__`.
   - [[utils.py|Módulo de Utilidades]]: Funciones auxiliares (`sanitize_number`, `retry`, `random_delay`, logging).

---

## 🎯 Puntos Clave para la Defensa del Caso

1. **Dominio de la Cadena de Extracción (Cascada de Fallbacks):**
   $$\text{window.\_\_NEXT\_DATA\_\_} \longrightarrow \text{Interceptación XHR} \longrightarrow \text{Parsing DOM} \longrightarrow \text{Simulación Add-to-Cart}$$
2. **Hallazgo Estratégico Principal (Efecto Canasta & Subsidio):**
   - Rappi lidera en precio base de productos individuales (ej. Big Mac: $-15.1\%$).
   - Uber Eats subsidia agresivamente combos ($-24.7\%$) y delivery fees en zonas de expansión (estrategia bimodal).
3. **Reproducibilidad y Ética:**
   - Trazabilidad total mediante `selector_hash`, metadata de confianza y capturas en `data/screenshots/`.
   - Respeto a límites de tasa (*rate limiting*) y delays estocásticos.
