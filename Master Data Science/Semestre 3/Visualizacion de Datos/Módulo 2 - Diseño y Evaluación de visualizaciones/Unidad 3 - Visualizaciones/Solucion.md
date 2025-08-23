

# Documento de Entrega – Esbozo de Visualización

## Actividad 1 – Planteamiento de problemática y boceto

**Problema propuesto:**  
El dataset de inventario de autos usados contiene información sobre precio, modelo, año, marca y otras características. Un reto común para el área de ventas es identificar el rango de precios en el que se concentra la mayor parte de la oferta disponible. Esto ayuda a:

- Definir estrategias de mercadeo (autos de gama baja, media o alta).
    
- Ajustar la comunicación hacia los segmentos de clientes más frecuentes.
    
- Detectar si la distribución está sesgada hacia autos de bajo costo o hacia autos premium.
    

**Esbozo de visualización:**  
La visualización propuesta es un **histograma** de precios de autos, complementado con una línea que muestre la densidad (KDE) para suavizar la distribución. Este diseño:

- Permite observar claramente la concentración de precios.
    
- Identifica los rangos más frecuentes y los outliers.
    
- Cumple con la regla de expresividad: precio es una variable cuantitativa → debe representarse en un eje continuo.
    

_(Aquí se incluirá la foto del boceto hecho a mano, con barras representando el histograma de precios y el eje Y mostrando la frecuencia de autos por rango de precio)._

---

## Actividad 2 – Respuesta y justificación

**Pregunta:** ¿Dónde se concentra el mayor rango de precio en este inventario?

**Respuesta:**  
La mayor concentración se encuentra en el rango de **autos de gama media** (ej. entre 5,000 y 15,000 USD, dependiendo de los datos exactos). Esto refleja que el mercado de autos usados tiende a ofrecer más vehículos en un rango accesible para la mayoría de los compradores, mientras que autos premium o muy económicos son minoría.

**Visualización usada:**  
Un **histograma de precios** (con opción de agrupar en bins de 1,000 USD o 2,000 USD).

**Justificación de selección:**

- Expresividad: el histograma respeta la naturaleza continua del precio.
    
- Efectividad: permite detectar de forma inmediata los intervalos más frecuentes.
    
- Simplicidad: evita sobrecargar con múltiples dimensiones.
    
- Posibilidad de extender: se podrían usar **small multiples** (ej. un histograma por marca o año) para segmentar aún más el análisis.
    

_(Aquí se adjunta nuevamente la foto del boceto, destacando con color el rango más denso de precios)._

---

## Conclusión

El uso de histogramas para representar precios permite a los stakeholders identificar de inmediato la concentración del inventario, facilitando decisiones de mercadeo y segmentación. Además, es una visualización coherente con los principios revisados en la unidad: clara, precisa y sin ruido visual.

---

👉 Lo único que faltaría es que me confirmes si quieres que **yo te genere un histograma de ejemplo con Python y matplotlib** usando datos ficticios (para que lo pegues como referencia junto al boceto manual), o si prefieres que solo dejemos la justificación y el boceto hecho a mano. ¿Quieres que prepare ese histograma de referencia?



![[Pasted image 20250822182409.png]]

He generado un histograma de ejemplo (con KDE superpuesto) y lo guardé como archivo PNG para que lo uses como referencia en tu esbozo y documento.

- Archivo creado: `/mnt/data/histograma_precios_ejemplo.png`  
    (Descárgalo desde el enlace que aparece en la interfaz o indica si quieres que lo convierta a otro formato.)
    
- Rango de concentración estimado (33–67 percentil) en la muestra simulada: **≈ $5,700 – $10,230 USD**.

### Qué incluye la figura

- Histograma de precios con bins de USD 1,000.
    
- KDE (suavizado) sobre la distribución, escalado a la frecuencia para permitir comparar forma y barras.
    
- Rango sombreado (33–67 percentiles) marcado como aproximación del intervalo de mayor concentración.
    
- Anotación con el N total de observaciones.
    

---

### Cómo usar esta figura en tu entrega

1. Inserta la imagen como **referencia** junto a tu boceto manual.
    
2. En el documento de entrega, menciona que la figura es **ejemplo** (generada con datos simulados) y sirve para validar el tipo de visualización propuesto.
    
3. Cuando uses los datos reales (`Car_Datasets_inventory.xlsx`), repite el proceso o pega los valores exactos para:
    
    - calcular percentiles (p. ej. 33–67 o 25–75),
        
    - ajustar bin width apropiado (por ejemplo, USD 500, 1,000 o 2,000 según dispersión),
        
    - identificar con precisión el rango de concentración de precios.
---

### Texto listo para pegar en tu PDF (sección "Visualización de referencia")

> **Visualización de referencia (generada con datos simulados):**  
> Se presenta un histograma de precios de autos usados con KDE superpuesto (archivo: `histograma_precios_ejemplo.png`). El histograma usa bins de USD 1,000 y el KDE está escalado a la frecuencia para facilitar la comparación entre la forma de la distribución y la altura de las barras. En la muestra simulada, el rango de mayor concentración (33º–67º percentil) se ubica aproximadamente entre **USD 5,700 y USD 10,230**, lo que sugiere que la mayor parte del inventario se encuentra en la gama media de precios. Este gráfico sirve como guía para construir el boceto y validar la elección del histograma como método apropiado para responder: _¿Dónde se concentra el mayor rango de precio en este inventario?_



How have you been? Whats up?