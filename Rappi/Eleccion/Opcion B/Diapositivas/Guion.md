
# Guion completo — palabra por palabra (por diapositiva)

**Slide 1 — Portada (0:00 – 0:40)**  
"Buenos días. Soy Juan José Restrepo Rosero. Gracias por el tiempo. Hoy voy a presentar el caso técnico: ‘Sistema de Competitive Intelligence para Rappi’. En los próximos minutos les mostraré el objetivo del PoC, la arquitectura técnica, la estrategia de scraping, los principales hallazgos comparativos frente a Uber Eats y las recomendaciones accionables."

**Slide 2 — Contexto y Objetivo (1:00 – 1:30)**  
"Contexto breve: las plataformas de delivery compiten en tiempo real con promociones, tarifas dinámicas y disponibilidad variable. El objetivo de este PoC fue obtener métricas comparativas entre plataformas —en particular Rappi y Uber Eats— para entender competitividad por producto y por zona, y proponer acciones tácticas y técnicas. Importante: DiDi no estuvo disponible en este muestreo inicial; lo documentamos como limitación y proponemos integrarlo en la siguiente fase."

**Slide 4 — Arquitectura (1:30 – 2:30)**  
"Arquitectura de alto nivel: partimos de un archivo de direcciones representativas, un orquestador ejecuta scrapers modulares por plataforma y consolida los resultados en JSON y CSV. El stack técnico clave fue Playwright para scraping y Python/pandas para análisis; los outputs son reproducibles en notebooks para auditoría y demo. Esta arquitectura permite re-ejecución automática y trazabilidad mediante screenshots y logs."









![[Pasted image 20251017150504.png]]

**INSIGHT CLAVE #1: POSICIONAMIENTO DE PRECIOS****Rappi es 15.1% más económico que Uber Eats en productos de referencia.**"Nuestro análisis se centró en métricas de _commodities_ (como la Big Mac) para garantizar una comparación **apples-to-apples**. El dato revela que Rappi tiene una **ventaja de precio final** significativa, siendo **15.1% más barato** que Uber Eats."**Finding**: Rappi Price: $154.40. Uber Eats Price: $181.87."Esto indica una **estructura de costos más eficiente** o una **agresiva estrategia de subsidio de _fees_** que se traslada al usuario final. Es una ventaja que debemos **monetizar y publicitar**."**Recomendación**: Monetizar la ventaja de precio en campañas de Marketing y Pricing."La recomendación de negocio es simple: aprovechar esta ventaja. Los equipos de Marketing deben usar esto como eje central de la comunicación en los países clave. El equipo de Pricing debe asegurarse de que esta brecha se mantenga de forma estratégica."