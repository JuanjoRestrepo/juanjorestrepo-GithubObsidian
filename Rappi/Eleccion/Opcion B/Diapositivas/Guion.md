


## 🗣️ **ARQUITECTURA**

Aquí vemos la arquitectura general del sistema.”

“Todo parte de un archivo de direcciones, que alimenta el orquestador principal, desarrollado en **Python con Playwright**.”

“El sistema resuelve automáticamente las URLs de los restaurantes y ejecuta scrapers específicos para **Rappi, UberEats y DiDi Food**.”

“Cada scraper obtiene los precios de productos clave, las tarifas de envío y los cargos por servicio.”

“Los resultados se almacenan en **JSON estandarizados**, junto con **capturas y logs**, lo que permite trazabilidad total.”

“Finalmente, los datos son procesados en los módulos de análisis y visualización, donde generamos **indicadores competitivos, comparativos de precios y dashboards ejecutivos**.”

“En resumen, el flujo completo va de la entrada de direcciones hasta la generación automática de insights competitivos.”

“Es una arquitectura modular, escalable y auditable, diseñada para integrar múltiples plataformas de forma automática y confiable.”


### 🧱 **Modular**

> “Porque cada componente cumple una función específica y desacoplada: resolución de URLs, scraping por plataforma, utilidades y análisis.  
> Esto permite mantener o reemplazar cualquier módulo sin afectar al resto.”


### ⚙️ **Escalable**

> “Porque el sistema puede ampliarse horizontalmente —agregando más plataformas, más direcciones o más productos— sin modificar la arquitectura base.  
> El flujo y los formatos de salida permanecen constantes.”

**👉 Ejemplo:** puedo ejecutar varias instancias en paralelo o escalar el scraping a distintos países simplemente cambiando el CSV de entrada.


### 🔍 **Auditable**

> “Porque cada ejecución deja evidencia trazable: logs, capturas de pantalla, metadatos y archivos JSON que documentan cada decisión y resultado.”

**👉 Ejemplo:** si un dato es inconsistente, puedo revisar el _screenshot_ y el JSON de depuración (`debug_responses/`) para entender exactamente qué ocurrió.

---

## **Diapositiva: Estrategias de Scraping**

> “La estrategia de scraping se diseñó con el objetivo de **obtener métricas comparables entre plataformas** de delivery —principalmente Rappi, UberEats y DiDi Food.  
> El alcance inicial se enfocó en **Rappi como prueba de concepto**, pero la arquitectura ya soporta múltiples plataformas de forma unificada.”

> “El sistema extrae **métricas cuantitativas clave** como el precio de los productos, tarifas de envío y servicio, descuentos aplicados y disponibilidad.  
> Esto permite construir una **base de datos estandarizada** para análisis competitivo, pricing y experiencia de usuario.”

> “En términos técnicos, cada scraper emplea **Playwright para la navegación dinámica**, y combina tres estrategias:  
> 1️⃣ extracción directa del _DOM_,  
> 2️⃣ lectura de respuestas _XHR / JSON_, y  
> 3️⃣ simulación de interacción (_add to cart_) para obtener tarifas ocultas.”



1️⃣ **DOM Parsing:** lectura directa del contenido visible.  
2️⃣ **XHR/JSON:** captura de datos en respuestas de red.  
3️⃣ **Simulación de interacción:** detección de tarifas ocultas.

> “El sistema aplica tres estrategias complementarias de scraping para asegurar que se capture toda la información, incluso la que no está directamente visible.”

> “Primero, se hace **DOM parsing**, que lee los elementos visibles en la interfaz.”  
> “Segundo, se analiza el tráfico de red, con el enfoque **XHR/JSON parsing**, donde se interceptan las respuestas que contienen datos estructurados del backend.”  
> “Y por último, usamos **simulación de interacción**, por ejemplo, agregando un producto al carrito, para detectar tarifas o precios que sólo aparecen después de una acción del usuario.”

> “Estas tres capas se integran para construir un dataset **completo, verificable y estandarizado**, base de todo el análisis  posterior.”


---

## 🧠 **Diapositiva: Mejora — Simulación Add-to-Cart**
#### **Texto breve en diapositiva (3–4 bullets):**

- Último fallback cuando no se encuentran tarifas visibles.
- Simula clics reales en “Agregar al carrito”.
- Extrae tarifas directamente del resumen del pedido.
- Aumenta la cobertura y confiabilidad del scraping.


---
### 🗣️ **Explicación oral (qué decir tú):**

> “Esta mejora permite obtener las tarifas incluso cuando no están visibles en el HTML.  
> El sistema identifica botones como _Agregar_ o _Añadir_, ejecuta un clic simulado y analiza el contenido del carrito, donde aparecen valores como el costo de envío o la tarifa de servicio.  
> Esto hace que el scraper se comporte como un usuario real y actúe como capa de respaldo cuando los métodos tradicionales (como XHR o DOM parsing) no encuentran la información.  
> Está implementado dentro del módulo _rappi_scraper.py_, en la función privada __try_simulate_add_to_cart_, y fue clave para aumentar la precisión del modelo de scraping.”



---

## Título: **Procesamiento y validación de datos**

- Datos estandarizados: `results.json` y `mapping.csv`
- Limpieza automática con `sanitize_number()` y reglas de negocio
- Extracción y validación de _delivery fee_ y _service fee_ (4 estrategias)
- Evidencias y trazabilidad: _screenshots_ + JSON de depuración


“En esta fase procesamos los datos crudos y los convertimos en información confiable y auditable.

Primero generamos los archivos **`results.json`** con los registros estandarizados y **`mapping.csv`** que mapea direcciones con los restaurantes.

Usamos funciones como **`sanitize_number()`** para limpiar formatos y reglas que validan los precios y tarifas. Las tarifas de envío y servicio se extraen mediante **cuatro estrategias combinadas**:  
1️⃣ inspección del objeto `window.__NEXT_DATA__`,  
2️⃣ análisis de respuestas XHR,  
3️⃣ búsqueda textual en el DOM, y  
4️⃣ simulación **Add-to-Cart** para forzar la visibilidad del resumen de pago.

Además, todos los pasos generan **evidencias**: capturas de pantalla y archivos JSON en carpetas de _debug_, lo que nos permite **rastrear, auditar y reproducir cualquier error**.

Finalmente, cada registro se valida frente a umbrales razonables y se clasifica como _success_, _not_found_ o _error_, lo que nos da un indicador de calidad por plataforma.















## 🧠 **Interpretación (para decir al presentar):**

### 1️⃣ Distribución de precios

![[Pasted image 20251017005929.png]]

- _“En general, los precios se concentran en dos rangos principales: uno bajo alrededor de $80–100 y otro alto cerca de $180–200 pesos. Esto refleja la segmentación entre bebidas y combos premium.”_
    
- _“La media es $128.93 y la mediana $144, lo que indica una ligera asimetría hacia productos de menor precio.”_
    

### 2️⃣ Precios por plataforma

![[Pasted image 20251017010051.png]]

- _“Aquí vemos claramente que Rappi tiende a tener precios más altos que UberEats.”_
    
- _“El rango de Rappi es más amplio, lo que refleja variación por zonas o promociones. UberEats muestra valores más compactos y económicos.”_
    

### 3️⃣ Distribución por categoría de producto

![[Pasted image 20251017010141.png]]
- _“La muestra está equilibrada: tenemos 5 productos premium, 5 combos y 4 bebidas.”_
    
- _“Esto asegura comparabilidad entre tipos de ítems en ambas plataformas.”_
    

### 4️⃣ Precios promedio por zona



- _“Los precios son consistentes en las zonas de mayor poder adquisitivo: Polanco, Condesa y Tlalpan Centro rondan los $142 pesos.”_
    
- _“El Centro Histórico es significativamente más barato ($79), lo que confirma una diferenciación geográfica de precios.”_


## 🗣️ **Cómo presentarlo oralmente (resumen de 20–25 segundos):**

> “Aquí vemos el análisis exploratorio de precios.  
> En la esquina superior izquierda observamos que la distribución es bimodal —productos económicos y combos premium—.  
> En la comparación de plataformas, Rappi muestra precios más altos.  
> En la parte inferior izquierda, vemos que las categorías están balanceadas, y a la derecha, las zonas premium mantienen precios alrededor de 140 pesos, mientras que el Centro Histórico es el más económico.”


**![](data:image/png;base64,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)**
**Bullets (para la diapositiva):**

- Polanco y Condesa concentran los valores totales más altos (≈$950–$1000 MXN).
- Centro Histórico es 60–70% más económico.
- UberEats mantiene menor costo logístico (delivery) en todas las zonas.
- Evidencia de diferenciación por nivel socioeconómico y cobertura operativa.

**Qué decir al presentarlo (discurso oral):**

> “Cuando combinamos el precio del producto con el costo de delivery, vemos que Polanco y Condesa son las zonas más caras en ambas plataformas.  
> UberEats sigue siendo más competitivo en costos de envío, mientras que Rappi concentra mayor valor total por zona, lo que sugiere estrategias diferenciadas de pricing y segmentación.”





---


# 3) ¿Qué hace cada script / dónde se ejecutan las piezas clave?

- **main (multi_platform_scraper.py / playwright_poc.py)**
    
    - Lee `addresses.csv`, orquesta scrapers por plataforma, captura respuestas HTTP y screenshots, guarda todos los resultados en `results.json` y `mapping.csv`.
        
- **rappi_scraper.py**
    
    - Extrae productos y precios desde el DOM (bloques evaluados por JS).
        
    - Extrae fees con varias estrategias (funciones clave):
        
        - `_try_parse_next_data()` → busca `window.__NEXT_DATA__`.
            
        - `_scan_xhr_responses()` → analiza XHR/JSON capturados.
            
        - `_extract_text_fees_from_dom()` → búsqueda por regex en el DOM.
            
        - `_try_simulate_add_to_cart()` → simula añadir producto para exponer tarifas ocultas.
            
    - Arma registros finales con `priceValue`, `deliveryFeeValue`, `serviceFeeValue`, `finalPriceValue`, `feeSource`.
        
- **utils.py**
    
    - `sanitize_number()` normaliza cadenas numéricas.
        
    - `dump_json_to()` escribe debug files.
        
    - `MAX_REASONABLE_FEE` define umbral para detectar valores anómalos.
        
- **resolver.py**
    
    - Resuelve la URL del restaurante desde la búsqueda (genera `resolutionMeta` usado luego en mapping y debugging).
        
- **Outputs de evidencia**
    
    - `data/debug_responses/*` (NEXT_DATA, XHR summaries) para auditar por porqué un fee fue / no fue detectado.
        
    - `data/screenshots/*` para revisar visualmente.





---


### 🕐 **20:00 – 30:00 | Sesión de preguntas**

**Posibles preguntas y cómo responder:**

|Pregunta|Respuesta sugerida|
|---|---|
|¿Por qué usar Playwright y no Selenium?|Playwright es más moderno, rápido y soporta interceptación de red y múltiples contextos.|
|¿Qué hace que la arquitectura sea escalable?|Está separada por módulos — se puede añadir otra plataforma con solo crear un nuevo scraper e integrarlo al orquestador.|
|¿Cómo manejaste los bloqueos o detección anti-bot?|Con rotación de user-agents, demoras aleatorias y tiempos variables de navegación.|
|¿Qué tipo de validaciones implementaste?|Validación numérica, límites máximos razonables y registros JSON de cada respuesta capturada.|
|¿Cómo planeas extender el sistema?|Integrando DiDi Food, automatizando ejecución diaria y generando dashboards dinámicos.|