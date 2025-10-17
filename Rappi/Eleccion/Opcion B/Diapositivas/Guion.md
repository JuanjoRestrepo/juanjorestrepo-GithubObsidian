


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


