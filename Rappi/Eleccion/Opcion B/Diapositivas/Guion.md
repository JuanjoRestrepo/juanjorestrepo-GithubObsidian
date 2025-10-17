# Guion final (30 min: 20 exposición + 10 preguntas)

## 🕐 0:00 – 1:30 | **Introducción general** (Slide: 1)

**Slide (texto mínimo):**

- Proyecto: Competitive Intelligence — Rappi vs. Uber Eats
    
- Objetivo: recolectar y comparar precios, delivery fee, service fee y disponibilidad
    
- Estado: PoC funcional
    

**Lo que dices (30–45s):**  
“Buenos días, soy Juan José. Presento un PoC de Competitive Intelligence para plataformas de delivery —principalmente Rappi y Uber Eats— que automatiza la recolección, validación y análisis de métricas clave como precio de producto, tarifas de envío y cargos de servicio. El resultado son datasets estandarizados listos para generar reportes ejecutivos.”

---

## 🕐 1:30 – 4:00 | **Motivación y problema** (Slide: 2)

**Slide (texto mínimo):**

- Problema: no hay APIs públicas → datos no comparables
    
- Meta: sistema robusto, auditable y reproducible
    

**Lo que dices (45–60s):**  
“El problema es simple: no tenemos APIs oficiales para comparar precios. Los valores cambian por zona, hora y demanda. Necesitamos datos comparables y trazables: por eso construimos este pipeline con Playwright que captura evidencia (screenshots y JSON) para auditoría.”

---

## 🕐 4:00 – 8:30 | **Arquitectura del sistema** (Slide: 3 — muestra el diagrama mermaid que ya tienes)

**Slide (texto mínimo):**  
“Arquitectura modular, escalable y auditable — entrada: CSV → salida: reportes y dashboards”

**Explicación (lo que dices, 3–4 frases):**  
“La arquitectura es modular: cada componente tiene responsabilidad única y queda bien desacoplado. El orquestador `multi_platform_scraper.py` controla el flujo; `resolver.py` localiza la URL correcta del restaurante; los scrapers `rappi_scraper.py` y `ubereats_scraper.py` extraen precios y fees; `utils.py` contiene validaciones, delays y persistencia; y el análisis final se realizó en `Rappi_Engineering_2025.ipynb`.”

**Mini-descripciones (una frase cada una — para explicar rápida):**

- `multi_platform_scraper.py`: orquesta todo (lectura CSV, instancias Playwright, escritura `results.json`).
    
- `resolver.py`: resuelve y selecciona la URL de restaurante más probable usando reglas de decisión.
    
- `rappi_scraper.py` / `ubereats_scraper.py`: extraen DOM, XHR y simulan add-to-cart para tarifas.
    
- `utils.py`: limpieza, retries, delays y dumps de debug.
    
- Notebook: análisis exploratorio, gráficos y conclusiones (fuente de los dashboards).
    

**Si te preguntan “¿por qué modular y escalable?”** (respuesta corta):  
“Modular porque cada pieza hace una tarea única (fácil de mantener/reemplazar). Escalable porque el orquestador acepta nuevas plataformas añadiendo un scraper y mantiene el formato de salida — se pueden ejecutar instancias en paralelo o cambiar el CSV para otros países.”

---

## 🕐 8:30 – 11:00 | **Estrategias de scraping** (Slide: 4)

**Slide (bullets cortos):**

- DOM parsing
    
- XHR / JSON parsing
    
- Simulación Add-to-Cart
    

**Lo que dices (30–40s):**  
“Combinamos tres capas para aumentar cobertura: lectura del DOM (lo visible), captura de respuestas XHR/JSON (datos de backend) y la simulación de interacción (add-to-cart) para exponer tarifas ocultas. Juntas forman un dataset completo y verificable.”

**Nota corta (qué script):**  
“La simulación Add-to-Cart está en `rappi_scraper.py` → `_try_simulate_add_to_cart()`.”

---

## 🕐 11:00 – 13:30 | **Mejora: Simulación Add-to-Cart** (Slide: 5)

**Slide (3–4 bullets):**

- Fallback para tarifas ocultas
    
- Simula clic en “Agregar”
    
- Extrae resumen del pedido (delivery/service)
    
- Implementado en `rappi_scraper.py`
    

**Lo que dices (30–40s):**  
“Al añadir el producto al carrito, aparecen valores que no están en el menú: tarifas dinámicas, comisiones o cargos por promociones. Eso aumentó nuestra tasa de detección y la exactitud del `finalPriceValue`.”

---

## 🕐 13:30 – 16:30 | **Procesamiento y validación de datos** (Slide: 6)

**Slide (bullets):**

- `results.json` (estandarizado) + `mapping.csv`
    
- `sanitize_number()` y `MAX_REASONABLE_FEE`
    
- 4 vías para fees: NEXT_DATA, XHR, DOM, Add-to-Cart
    
- Evidencia: screenshots + `debug_responses`
    

**Lo que dices (40–45s):**  
“Limpiamos y normalizamos los datos: convertimos cadenas a números con `sanitize_number()`, aplicamos umbrales (`MAX_REASONABLE_FEE`) y registramos cada decisión con `debug_responses` y screenshots para poder auditar fácilmente. Las rutas para extraer fees son: 1) `window.__NEXT_DATA__`, 2) XHR/JSON, 3) regex en DOM y 4) simulación de carrito.”

---

## 🕐 16:30 – 19:00 | **Análisis exploratorio — Rappi vs Uber Eats** (Slides 7–11: gráficos)

> **Instrucción:** cada slide con gráfico pone 2 líneas de bullets; tú hablas ~20–30s por gráfico.

### Slide 7 — **Distribución de precios (bimodal)**

**Slide (bullets):**

- Distribución bimodal: rango bajo (≈80–100) y alto (≈180–200)
    
- Media ≈ 129, Mediana ≈ 144
    

**Lo que dices (20–30s):**  
“Observamos una distribución bimodal: productos individuales y combos premium. La media y la mediana muestran ligera asimetría hacia productos más baratos, lo que indica mezcla de ítems y promociones.”

---

### Slide 8 — **Precios por plataforma (Rappi vs UberEats)**

**Slide (bullets):**

- Rappi muestra valores más altos y mayor variabilidad
    
- UberEats presenta rango más compacto y económico
    

**Lo que dices (20–30s):**  
“En esta comparación Rappi tiende a precios base más altos y con mayor dispersión, mientras UberEats es más consistente y algo más barato en promedio. Esto sugiere diferencias en pricing y promociones por plataforma.”

---

### Slide 9 — **Distribución por categoría de producto**

**Slide (bullets):**

- Categorías balanceadas: premium, combos, bebidas
    
- Muestra comparativa clara entre plataformas
    

**Lo que dices (20–30s):**  
“La muestra incluye categorías balanceadas (premium, combos, bebidas), lo que ayuda a comparar de forma justa entre plataformas y evitar sesgos por tipo de producto.”

---

### Slide 10 — **Precios promedio por zona**

**Slide (bullets):**

- Polanco/Condesa ≈ $140 promedio
    
- Centro Histórico ≈ $79 (mucho más barato)
    

**Lo que dices (25–30s):**  
“Geográficamente, zonas de mayor poder adquisitivo (Polanco, Condesa) tienen precios promedio ~140; Centro Histórico es significativamente más barato — esto confirma segmentación geográfica y estrategia de cobertura.”

---

### Slide 11 — **Precio final por zona (producto + delivery + fees)**

**Slide (bullets):**

- Polanco/Condesa: totales más altos (≈ $950–$1000 MXN por pedidos simulados)
    
- UberEats: menor costo logístico (delivery) en general
    

**Lo que dices (25–30s):**  
“Combinando producto + delivery + service, Polanco/Condesa dominan el costo total. UberEats suele tener menor delivery fee, mientras Rappi presenta mayor valor total por zona — posible enfoque en conveniencia o tarifas dinámicas.”

---

## 🕐 19:00 – 20:00 | **Conclusiones** (Slide: 12)

**Slide (bullets cortos):**

- Sistema modular, auditable y escalable (PoC listo)
    
- Add-to-Cart aumentó precisión
    
- Rappi vs UberEats: diferencias en pricing y fees
    
- Siguiente paso: automatizar ejecución y dashboards en tiempo real
    

**Lo que dices (30–40s):**  
“Resumiendo: el PoC es funcional y trazable. La simulación de carrito mejoró la calidad del dato. Las plataformas aplican estrategias diferentes —Rappi con precios base más altos y UberEats con menores costos de envío—. Próximo paso: automatizar ejecuciones periódicas y exponer dashboards ejecutivos.”

---

## 🕐 20:00 – 30:00 | **Preguntas (10 min)**

**Preguntas esperadas y respuestas breves:**

- **¿Por qué Playwright y no Selenium?**  
    “Playwright maneja múltiples contextos, intercepta XHR/JSON más fácilmente y suele ser más robusto para SPAs modernas.”
    
- **¿Qué significa `score += 50` en resolver?**  
    “Es una regla de decisión: ganar 50 puntos cuando el candidato contiene ‘mcdonald’ —prioriza coincidencias fuertes para elegir la URL.”
    
- **¿Cómo se evita ser bloqueado?**  
    “Rotación de user-agents, delays aleatorios, y límites de requests; además guardamos evidencia para revisar fallos.”
    
- **¿Cómo validar que el fee es correcto?**  
    “Comparamos múltiples fuentes: `__NEXT_DATA__`, XHR, DOM y carrito; si coinciden, confianza alta; todo auditado con JSON y screenshots.”
    
- **¿Qué tan escalable es para otros países o cadenas?**  
    “Se añade un scraper específico por plataforma o cadena; formato de salida y orquestador se mantienen, por lo que la ampliación es directa.”
    

---

## Apéndice para tus notas (resumen técnico rápido — copy/paste)

**Dónde está cada cosa:**

- Orquestador: `multi_platform_scraper.py` (main)
    
- Resolver: `resolver.py` → `resolve_restaurant_url(page, query)` (reglas de decisión)
    
- Rappi scraper: `rappi_scraper.py` → scraping DOM /