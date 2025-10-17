


## 🗣️ **GUION ORAL (qué debes decir tú al presentar la diapositiva)**

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