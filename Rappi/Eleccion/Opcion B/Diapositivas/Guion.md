## 🕐 0:00 – 1:30 | Introducción general

**Diapositiva (texto corto):**

- PoC: Competitive Intelligence para plataformas de delivery
    
- Plataformas: Rappi, Uber Eats
    
- Métricas: precio, delivery fee, service fee, disponibilidad
    

**Qué decir (texto literal):**  
“Buenos días, mi nombre es Juan José. El proyecto que presento hoy es un sistema de **Competitive Intelligence** para plataformas de delivery — centrado en **Rappi** y **Uber Eats**. Su propósito es recolectar, procesar y analizar métricas clave como precios, tarifas y disponibilidad de productos, de forma automática y auditada.”

**Bullets oralmente (rápido):**

- “Es un Proof of Concept funcional.”
    
- “Automatiza la captura y análisis de datos de mercado.”
    
- “Permite comparar comportamiento competitivo entre plataformas.”
    

---

## 🕐 1:30 – 4:00 | Motivación y problema

**Diapositiva (texto corto):**

- Problema: no hay APIs públicas comparables
    
- Variabilidad: zona, hora, demanda
    
- Solución: scraping controlado y auditable
    

**Qué decir (texto literal):**  
“El reto: no hay APIs públicas comparables; los precios varían por zona, hora y demanda. Nuestro objetivo fue construir un sistema robusto y reproducible para obtener datos comparables entre plataformas.”

**Puntos orales (breves):**

- “Problema: falta de acceso oficial a datos.”
    
- “Enfoque: Playwright para navegación dinámica y captura de red.”
    
- “Valor: datos comparables, reproducibles y auditables.”
    

---

## 🕐 4:00 – 8:30 | Arquitectura del sistema — explicación ampliada

**Diapositiva (texto corto + diagrama):**

- Arquitectura modular, escalable y auditable
    
- Flujos: CSV → orquestador → scrapers → JSON + evidencias → análisis
    

**Qué decir (introducción):**  
“La arquitectura que diseñé es modular, escalable y auditable. Todo parte de un archivo de direcciones y termina en reportes ejecutivos y dashboards visuales.”

**Explicación módulo a módulo (línea por línea, decirlo tal cual):**

- **multi_platform_scraper.py — orquestador:**  
    “Es el núcleo. Lee el `addresses.csv`, itera direcciones y plataformas, captura respuestas HTTP y screenshots, compila `results.json` y `mapping.csv`.”
    
- **resolver.py — resolución de URL:**  
    “Localiza la URL del restaurante usando una **lógica de selección** (reglas de decisión) que puntúa candidatos y devuelve `resolutionMeta` con la confianza.”
    
- **rappi_scraper.py / ubereats_scraper.py — scrapers por plataforma:**  
    “Extraen nombre, precio, disponibilidad y tarifas. Implementan múltiples técnicas para obtener fees: `window.__NEXT_DATA__`, XHR/JSON, parsing del DOM y simulación Add-to-Cart.”
    
- **utils.py — utilidades:**  
    “Contiene funciones transversales: `sanitize_number()` para limpiar números, `dump_json_to()` para guardar debug, delays aleatorios y umbrales (`MAX_REASONABLE_FEE`).”
    
- **Notebook / scripts de análisis:**  
    “Aunque hay scripts en `analysis/`, el trabajo de análisis y visualización final se realizó en `Rappi_Engineering_2025.ipynb`.”
    

**Cierre (decirlo exactamente):**  
“La separación por módulos facilita mantenimiento o extensión — por eso es _modular_; se puede paralelizar o ejecutar en más direcciones/plataformas sin cambiar la arquitectura — por eso es _escalable_; y cada ejecución deja capturas y JSON para auditoría — por eso es _auditable_.”

---

## 🕐 8:30 – 11:00 | Estrategias de scraping

**Diapositiva (3 bullets):**

- DOM parsing
    
- XHR / JSON parsing
    
- Simulación Add-to-Cart
    

**Qué decir (texto literal):**  
“Combinamos tres estrategias complementarias para maximizar cobertura y exactitud: DOM parsing para lo visible, XHR/JSON parsing para respuestas estructuradas del backend, y simulación Add-to-Cart como respaldo cuando las tarifas solo aparecen tras interacción del usuario.”

---

## 🕐 11:00 – 13:30 | Mejora — Simulación Add-to-Cart

**Diapositiva (4 bullets):**

- Fallback último si no hay fees visibles
    
- Simula clics en 'Agregar'
    
- Extrae tarifas del resumen de pedido
    
- Implementado en `rappi_scraper.py` → `_try_simulate_add_to_cart`
    

**Qué decir (texto literal):**  
“Si no encontramos fees por otras vías, simulamos añadir un producto al carrito. El scraper busca botones como 'Agregar' o 'Añadir', ejecuta un clic simulado y analiza el contenido del carrito donde aparecen el delivery y la service fee. Esto actúa como comportamiento de usuario real y fue clave para aumentar la precisión.”

---

## 🕐 13:30 – 16:30 | Procesamiento y validación de datos

**Diapositiva (bullets):**

- Outputs: `results.json`, `mapping.csv`, `data/debug_responses/`, `data/screenshots/`
    
- Limpieza: `sanitize_number()`
    
- Reglas: `MAX_REASONABLE_FEE`
    
- Clasificación: `success` / `not_found` / `error`
    

**Qué decir (texto literal):**  
“Los datos crudos se normalizan y validan: `sanitize_number()` limpia distintos formatos numéricos; rechazamos fees fuera de un umbral razonable; y cada registro incluye metadata de la resolución y origen del fee (`feeSource`). Además guardamos evidencia: JSONs de `window.__NEXT_DATA__`, resúmenes XHR y screenshots para auditoría y debugging.”

---

## 🕐 16:30 – 19:00 | Análisis exploratorio & hallazgos — Rappi vs Uber Eats

> **Instrucción:** muestra los gráficos del notebook en el mismo orden. Aquí tienes exactamente qué decir por cada gráfico.

### Gráfico 1 — Distribución de precios (histograma)

**Qué decir (20–25s):**  
“Aquí vemos una visualización con una **distribución bimodal**, es decir, que los precios se agrupan en **dos modas o picos distintos**. Esto revela la existencia de **dos subpoblaciones de productos**: un grupo **económico** concentrado alrededor de **$80–100 MXN** y un grupo **premium** cerca de **$180–200 MXN**.

Las estadísticas centrales confirman esta polarización: la **media** se sitúa en **$129 MXN**, mientras que la **mediana** es notablemente más alta, en **$144 MXN**. El hecho de que la mediana ($144 MXN) sea superior a la media ($129 MXN) indica una **ligera asimetría hacia la izquierda (sesgo negativo)**, lo que es causado principalmente por la influencia del grupo más numeroso de productos en el rango de precios más alto (premium).”

### Gráfico 2 — Precios por plataforma (boxplots Rappi vs UberEats)

**Qué decir (20s):**  
“En la comparación, Rappi muestra medianas más altas y un rango más amplio; Uber Eats aparece más compacto y con valores generalmente menores. Esto indica que Rappi tiende a tener precios base más altos o mayor variabilidad por zona o promoción.”

### Gráfico 3 — Distribución por categoría (bebidas / combos / premium)

**Qué decir (15–20s):**  
“La muestra está equilibrada entre categorías, lo que nos permite comparar manzanas con manzanas entre plataformas: bebidas, combos y productos premium están representados.”

### Gráfico 4 — Precios promedio por zona (barras o mapa)

**Qué decir (20s):**  
“Polanco, Condesa y Tlalpan presentan precios promedio altos (~142 MXN), mientras que el Centro Histórico es mucho más barato (~79 MXN). Esto confirma segmentación geográfica: zonas premium vs zonas más económicas.”

### Gráfico 5 — Precio final combinado (producto + delivery + service)

**Qué decir (20s):**  
“Al sumar delivery y service fees, Polanco y Condesa muestran los totales más altos. Uber Eats suele mantener delivery más bajo, y Rappi concentra mayor valor total en varias zonas. Esto sugiere estrategias de pricing y cobertura distintas.”

---

## 🕐 19:00 – 20:00 | Conclusiones finales

**Diapositiva (bullets):**

- PoC exitoso y reproducible
    
- Add-to-Cart aumentó cobertura de fees
    
- Rappi: precios base más altos; Uber Eats: delivery más competitivo
    
- Próximos pasos: incluir DiDi Food, automatizar corridas, dashboards interactivos
    

**Qué decir (texto literal, 25s):**  
“El proyecto demuestra que es posible construir una capa de inteligencia competitiva confiable sobre plataformas sin API. La simulación Add-to-Cart fue crítica para capturar tarifas ocultas. Como hallazgo: Rappi muestra precios base más altos, Uber Eats tiende a ser más competitivo en delivery. Siguientes pasos: ampliar plataformas, programar ejecuciones periódicas y exponer dashboards para la toma de decisiones.”

---

## 🕐 20:00 – 30:00 | Preguntas — respuestas preparadas

**Preguntas frecuentes y respuestas (corta y lista):**

- **¿Por qué Playwright y no Selenium?**  
    “Playwright ofrece mejor control de múltiples contextos, interceptación de red y estabilidad moderna para páginas dinámicas.”
    
- **¿Qué es la ‘lógica de selección’ en el resolver?**  
    “Son reglas de decisión que puntúan candidatos (por ejemplo: +50 si el href o texto contiene 'mcdonald'); la URL con mayor puntaje se devuelve junto con un `confidence` (high/medium/low).”
    
- **¿Cómo se minimiza la detección anti-bot?**  
    “Rotación de user-agents, delays aleatorios, y límites de frecuencia. Además, guardamos capturas y JSON para analizar bloqueos si ocurren.”
    
- **¿Qué grado de confianza tienen los fees extraídos?**  
    “Elevada cuando provienen de JSON/XHR o `window.__NEXT_DATA__`. Si vienen solo de parsing textual del DOM, la confianza es menor; Add-to-Cart eleva la confianza cuando lo logra.”
    
- **¿Dónde corren las tareas? ¿Se pueden paralelizar?**  
    “Se ejecutan desde `multi_platform_scraper.py` (o `playwright_poc.py`) con Playwright; la arquitectura permite ejecutar múltiples instancias en paralelo para escalar.”
    

---

## Notas rápidas (para tus apuntes personales)

- Cuando muestres un gráfico, apunta siempre a 3 mensajes: _qué es el gráfico_, _qué se observa_, _qué implica para negocio_.
    
- Si te piden detalles técnicos, menciona funciones clave: `_try_parse_next_data`, `_scan_xhr_responses`, `_try_simulate_add_to_cart`, `sanitize_number`.
    
- Si te preguntan por limitaciones: menciona dependencia de estructura HTML, posible bloqueo anti-bot, y tamaño de la muestra (n addresses).