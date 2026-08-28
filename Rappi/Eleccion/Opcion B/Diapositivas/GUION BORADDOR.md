---
title: "Opción B - Guion Extendido de Sustentación y Banco de Q&A"
date: 2026-08-27
tags:
  - caso-estudio
  - presentacion
  - guion
  - oratoria
  - q-and-a
status: evergreen
---

# 🎙️ Guion Extendido de Sustentación y Preparación de Q&A

Guion detallado de exposición con minutaje estricto, texto literal sugerido, análisis estadístico profundo de gráficos y banco de respuestas técnicas a preguntas frecuentes.

---

## ⏱️ Minuto a Minuto de la Presentación

### 🕐 0:00 – 1:30 | Introducción General y Contexto
- **Apoyo Visual en Diapositiva:**
  - Proyecto: Proof of Concept (PoC) de *Competitive Intelligence* para delivery.
  - Plataformas: Rappi vs. Uber Eats.
  - Dimensiones: Precio del producto, *delivery fee*, *service fee* y disponibilidad.
- **Discurso Sugerido (Literal):**
  > *"Buenos días. Mi nombre es Juan José Restrepo. El proyecto que presento hoy es un sistema de **Competitive Intelligence** para plataformas de delivery, centrado en comparar la dinámica de precios y tarifas entre **Rappi** y **Uber Eats**. Su propósito es recolectar, procesar y analizar métricas clave como precios base, tarifas de entrega y disponibilidad de productos de forma automática, estructurada y auditable."*

---

### 🕐 1:30 – 4:00 | Motivación y Planteamiento del Problema
- **Apoyo Visual en Diapositiva:**
  - Desafío: Ausencia de APIs públicas y asimetría de información de mercado.
  - Variabilidad: Precios dinámicos por zona geográfica, hora y demanda.
  - Solución: Pipeline automatizado con Playwright y auditoría visual.
- **Discurso Sugerido (Literal):**
  > *"El principal reto de negocio radica en que no existen APIs públicas comparables entre competidores. Los precios y tarifas varían en tiempo real según la ubicación geográfica, el momento del día y la presión de la demanda. Nuestro objetivo fue construir un sistema robusto y reproducible para extraer y estructurar datos homogéneos que permitan tomar decisiones estratégicas de pricing y subsidios."*

---

### 🕐 4:00 – 8:30 | Arquitectura del Sistema y Explicación de Módulos
- **Apoyo Visual en Diapositiva:** Diagrama de bloques (Entradas $\rightarrow$ Orquestador $\rightarrow$ Scrapers $\rightarrow$ Persistencia $\rightarrow$ Análisis).
- **Discurso Sugerido por Módulo:**
  - **`multi_platform_scraper.py` (Orquestador):** *"Es el núcleo coordinador. Lee el archivo `addresses.csv`, itera por cada ubicación y plataforma, gestiona la sesión de Playwright, intercepta el tráfico de red y compila los resultados en `results.json`."*
  - **`resolver.py` (Resolución de URLs):** *"Localiza automáticamente la URL de la sucursal del restaurante aplicando un algoritmo de puntuación (+50 por coincidencia de marca, +10 por coincidencia de zona) y calcula un nivel de confianza (`high`, `medium`, `low`)."*
  - **`rappi_scraper.py` / `ubereats_scraper.py` (Scrapers Modulares):** *"Implementan la extracción en cascada: lectura de `window.__NEXT_DATA__`, parseo de JSONs en respuestas XHR, análisis del DOM y simulación de usuario en el carrito."*
  - **`utils.py` (Módulo Transversal):** *"Centraliza utilidades críticas: `sanitize_number()` para normalización de formatos numéricos, pausas estocásticas anti-bloqueo y control de umbrales como `MAX_REASONABLE_FEE`."*
  - **Cierre Arquitectónico:** *"Esta arquitectura es **modular** (facilita añadir competidores), **escalable** (permite paralelización) y **auditable** (guarda capturas de pantalla y dumps JSON por cada evento)."*

---

### 🕐 8:30 – 13:30 | Estrategia de Scraping y Simulación Add-to-Cart
- **Apoyo Visual en Diapositiva:** Cascada de 4 niveles de extracción.
- **Discurso Sugerido (Literal):**
  > *"Para garantizar la máxima cobertura de datos, diseñamos una estrategia en cascada: primero extraemos datos estructurados desde el objeto `window.__NEXT_DATA__`; si no está disponible, interceptamos las respuestas de red XHR del backend; en tercer lugar, parseamos el texto del DOM. Si las tarifas de entrega están ocultas, activamos el fallback de **Simulación Add-to-Cart**, donde el scraper añade programáticamente el producto al carrito para leer el desglose final de delivery y service fee."*

---

### 🕐 13:30 – 19:00 | Análisis Exploratorio de Datos & Hallazgos Estratégicos

#### 📊 Gráfico 1 — Distribución de Precios (Histograma)
> *"Observamos una **distribución bimodal** en los precios: un segmento económico alrededor de los $\$80-\$100\text{ MXN}$ y un segmento premium cerca de $\$180-\$200\text{ MXN}$. Dado que la **Mediana ($\$144.00\text{ MXN}$)** es superior a la **Media ($\$128.93\text{ MXN}$)**, la distribución presenta una **asimetría negativa (sesgo hacia la izquierda)** causada por una cola de precios bajos que tracciona la media hacia abajo."*

#### 📦 Gráfico 2 — Comparativa por Plataforma (Boxplots)
> *"Rappi exhibe medianas de precio base ligeramente más altas y mayor dispersión; Uber Eats presenta un rango más compacto y precios base más ajustados, reflejando estrategias de pricing diferenciadas."*

#### 📍 Gráfico 4 — Precios Promedio por Zona Geográfica
> *"Zonas como Polanco, Condesa y Tlalpan presentan precios medios elevados ($\approx \$142\text{ MXN}$), mientras que el Centro Histórico se posiciona como una zona más accesible ($\approx \$79\text{ MXN}$), confirmando la segmentación geográfica."*

#### 🚚 Gráfico 5 — Desglose de Valor Total (Producto + Delivery + Service Fee)
> *"Al integrar las tarifas de entrega, descubrimos que Uber Eats subsidia casi el $100\%$ del Delivery Fee en zonas estratégicas de expansión para compensar precios de producto más altos o ganar cuota de mercado."*

---

### 🕐 19:00 – 20:00 | Conclusiones y Recomendaciones de Negocio
- **Discurso Sugerido (Literal):**
  > *"El PoC demuestra que es viable construir una capa de inteligencia de mercado altamente confiable. Como conclusión de negocio: Rappi lidera en precios de productos individuales, pero Uber Eats es más competitivo en la canasta completa y en subsidios de entrega en zonas de expansión. Recomendamos implementar una política de Delivery Fee dinámico para neutralizar el avance de la competencia en dichas zonas."*

---

## ❓ Banco de Preguntas y Respuestas Técnicas (Q&A)

| Pregunta Esperada | Respuesta Técnica Argumentada |
| :--- | :--- |
| **¿Por qué utilizaron Playwright en lugar de Selenium o Scrapy?** | Playwright ofrece control nativo y asincrónico sobre contextos de navegador Chromium, permite interceptar tráfico de red (XHR/Fetch) de forma transparente y maneja Single Page Applications (SPAs) modernas con mayor estabilidad y velocidad que Selenium. |
| **¿Cómo opera el algoritmo de scoring en `resolver.py`?** | Es un sistema heurístico de puntuación ponderada: evalúa los enlaces en la página de resultados y otorga $+50$ puntos por coincidencia de la marca de interés y $+10$ puntos por coincidencia de texto con la dirección. Si el puntaje es $\ge 35$, se clasifica como confianza `high`. |
| **¿Cómo se mitiga el riesgo de bloqueos por sistemas anti-bot?** | Se aplican tres técnicas combinadas: rotación de cabeceras `User-Agent`, retardos aleatorios estocásticos (`random_delay` entre 1.2s y 3.5s) y captura prioritaria de datos estáticos/XHR para minimizar la cantidad de interacciones en el DOM. |
| **¿Qué confiabilidad tienen las tarifas capturadas?** | La confiabilidad es máxima cuando provienen de `__NEXT_DATA__` o respuestas JSON de red, y se respalda visualmente mediante capturas de pantalla automáticas (`data/screenshots/`) y la simulación Add-to-Cart. |