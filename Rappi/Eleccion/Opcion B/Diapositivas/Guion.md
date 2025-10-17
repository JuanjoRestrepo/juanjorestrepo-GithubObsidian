
# Guion completo — palabra por palabra (por diapositiva)

**Slide 1 — Portada (0:00 – 0:40)**  
"Buenos días. Soy Juan José Restrepo Rosero. Gracias por el tiempo. Hoy voy a presentar el caso técnico: ‘Sistema de Competitive Intelligence para Rappi’. En los próximos minutos les mostraré el objetivo del PoC, la arquitectura técnica, la estrategia de scraping, los principales hallazgos comparativos frente a Uber Eats y las recomendaciones accionables."

**Slide 2 — Contexto y Objetivo (1:00 – 1:30)**  
"Contexto breve: las plataformas de delivery compiten en tiempo real con promociones, tarifas dinámicas y disponibilidad variable. El objetivo de este PoC fue obtener métricas comparativas entre plataformas —en particular Rappi y Uber Eats— para entender competitividad por producto y por zona, y proponer acciones tácticas y técnicas. Importante: DiDi no estuvo disponible en este muestreo inicial; lo documentamos como limitación y proponemos integrarlo en la siguiente fase."

**Slide 4 — Arquitectura (1:30 – 2:30)**  
"partimos de un archivo de direcciones representativas, un orquestador ejecuta scrapers modulares por plataforma y consolida los resultados en JSON y CSV. El stack técnico clave fue Playwright para scraping y Python/pandas para análisis; los outputs son reproducibles en notebooks para auditoría y demo. Esta arquitectura permite re-ejecución automática y trazabilidad mediante screenshots y logs."

**Slide 5 — Estrategia de Scraping (2:30 – 3:30)**  
"La estrategia técnica combinó tres métodos: DOM parsing para leer contenido visible; XHR/JSON scraping para capturar datos de las respuestas de red cuando están disponibles; y simulación de interacción, incluyendo un fallback de Add-to-Cart para extraer tarifas ocultas en el resumen del pedido. Aplicamos rate limiting, retries y guardado de capturas como evidencia para mantener ética y reproducibilidad."

**Slide 6 — Procesamiento y Validación de Datos (3:30 – 4:30)**  
"En el pipeline los datos se estandarizaron con funciones como `sanitize_number()` y mappings de producto. Validamos campos críticos: `finalPriceValue` y `deliveryFeeValue`, y marcamos flags para ofertas. Para control de calidad medimos el ratio `success` versus `not_found` y guardamos JSONs y screenshots por evento. Esto permite cuantificar y explicar sesgos de muestreo."



### INSIGHT #1: La Ventaja Inicial (Fast Food Individual)

**Slide 7 — Mean final price — Big Mac (4:30 – 5:40)**

Intro frase:  
"Iniciamos el análisis comparando el producto más estandarizado: la Big Mac."

"Aquí, Rappi tiene una clara ventaja de precio, siendo $154.40 versus $181.87 de Uber Eats. Rappi es 15.1% más económico en este ítem individual."

"Finding: Rappi tiene un mejor posicionamiento de precio en el ítem individual. Impacto: Esta ventaja es un punto de marketing clave. Recomendación: Usar esta ventaja en campañas publicitarias con un mensaje claro, por ejemplo 'El producto es más barato en Rappi' para reforzar percepción de valor en compras individuales."

"Esta ventaja es relevante, pero no cuenta toda la historia cuando consideramos la canasta completa."

### INSIGHT #2 & #3: El Contra-Ataque Competitivo (La Canasta)

**Slide 8 — Mean final price — Combo Mediano (5:40 – 6:40)**

"Sin embargo, la ventaja inicial se revierte cuando miramos la canasta completa."

"Para el Combo, Rappi es 24.7% más caro que Uber Eats."

"Esto sugiere que Uber Eats está usando descuentos y promociones en combos para capturar ticket medio."


**Slide 9 — Mean final price — Coca-Cola 500ml (6:40 – 7:20)**

"En el retail, que impacta la frecuencia de uso, vemos la misma dinámica."
  
"En el ítem de retail —la Coca-Cola 500ml— Rappi es 20.1% más caro."

"Uber Eats está subsidiando agresivamente el pedido de mayor valor (Combo) y el pedido de mayor frecuencia (Retail). Impacto: Estamos perdiendo competitividad en el Average Order Value y en la frecuencia de uso. Recomendación: Introducir una lógica de subsidios de fees más granular para neutralizar la ventaja de Uber Eats en pedidos con combos y categorías retail."

"Para entender por qué sucede esto, necesitamos mirar la estructura de fees."


### INSIGHT #4: La Anomalía y la Corrección Técnica (Estructura de Fees)

**Slide 10 — Delivery fee distribution by platform (7:20 – 8:20)**
 
"Analizamos la distribución de delivery fees para explicar la reversión observada."

"En la muestra aparece un Delivery Fee en Uber Eats de $137.00 que sobresale como anomalía. Esto puede ser el precio full sin subsidio o una agregación de tarifas. Debo destacar que nuestro scraper encontró un edge técnico: hay casos con bloqueo de autenticación o datos cargados por API que no siempre se capturan perfectamente."


"El Delivery Fee reportado es anómalo y puede invalidar la comparación directa si no lo corregimos. Impacto: Sin la métrica correcta, las decisiones de pricing permanecen 'a ciegas'. Recomendación: Corregir la métrica con validaciones adicionales —usar Add-to-Cart, capturas y verificación en sesiones autenticadas— y comparar siempre con el Costo Total por Entrega (Delivery Fee + Service Fee)."

"Con esa corrección en mente, veamos el análisis de valor total por zona."



### INSIGHT #5: La Raíz del Problema (El Ataque Estratégico)

**Slide 11 — Análisis de Valor Total por Zona (8:20 – 10:00)**

Apertura:  
"Ahora aplicamos la corrección y analizamos el valor total —producto más delivery— por zona."

Texto que dices al mostrar el gráfico:  
"El gráfico muestra que el precio del producto entre plataformas es casi idéntico, pero la diferencia en el precio final está enteramente en el Delivery Fee: la franja superior es la que marca la distancia en la altura total."

Finding / Impact / Recomendación (preciso):  
"Finding: Uber Eats subsidi­a casi el 100% del Delivery Fee en zonas estratégicas —Zona 1 y Zona 2— con el objetivo de igualar o bajar el precio final. Impacto: La entrega se convierte en la palanca competitiva principal. Recomendación: Mover el foco de Rappi del precio del producto al precio final total; implementar un Delivery Fee dinámico a nivel de zona y subsidiar automáticamente en zonas donde detectemos subsidios agresivos por parte de la competencia."

Breve ejemplo operacional:  
"Operativamente proponemos un piloto que subsidie el delivery al 100% en tres zonas donde Uber Eats lidera, midiendo variación en share y AOV en 4 semanas."


### INSIGHT #6: Estrategia Bimodal y Riesgo Geográfico

**Slide 12 — Cheapest platform code by address — Heatmap (10:00 – 11:30)**

Apertura:  
"Finalmente, miremos la variabilidad geográfica sintetizada en el heatmap."

Texto que dices al mostrar el heatmap:  
"El posicionamiento de precio es binario y depende de la zona: Rappi es más barato en zonas wealthier —Condesa y Polanco— mientras que Uber Eats es más barato en zonas de expansión como Tlalpan Centro."

Finding / Impact / Recomendación estratégica:  
"Finding: El ataque competitivo de Uber Eats está focalizado en ganar penetración en zonas de expansión, que son fuentes de crecimiento. Impacto: Si no actuamos, podemos perder la base de usuarios de crecimiento. Recomendación de estrategia bimodal: en zonas wealthier competir en calidad operacional y tiempos de entrega; en zonas de expansión neutralizar el precio con subsidios direccionados para blindar el mercado en crecimiento."

Transición hacia conclusiones:  
"Con estos hallazgos, paso a un resumen ejecutivo y las recomendaciones priorizadas."








---

![[Pasted image 20251017150504.png]]

**INSIGHT CLAVE #1: POSICIONAMIENTO DE PRECIOS****Rappi es 15.1% más económico que Uber Eats en productos de referencia.**"Nuestro análisis se centró en métricas de _commodities_ (como la Big Mac) para garantizar una comparación **apples-to-apples**. El dato revela que Rappi tiene una **ventaja de precio final** significativa, siendo **15.1% más barato** que Uber Eats."**Finding**: Rappi Price: $154.40. Uber Eats Price: $181.87."Esto indica una **estructura de costos más eficiente** o una **agresiva estrategia de subsidio de _fees_** que se traslada al usuario final. Es una ventaja que debemos **monetizar y publicitar**."**Recomendación**: Monetizar la ventaja de precio en campañas de Marketing y Pricing."La recomendación de negocio es simple: aprovechar esta ventaja. Los equipos de Marketing deben usar esto como eje central de la comunicación en los países clave. El equipo de Pricing debe asegurarse de que esta brecha se mantenga de forma estratégica."