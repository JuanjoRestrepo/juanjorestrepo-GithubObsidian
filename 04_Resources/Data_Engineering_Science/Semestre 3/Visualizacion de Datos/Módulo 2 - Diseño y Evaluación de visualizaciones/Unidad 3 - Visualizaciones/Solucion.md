---
title: "Solucion"
date: 2026-08-27
tags:
  - maestria
  - semestre-3
  - visualizacion-datos
  - apuntes
status: reference
---



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



---


# Histograma Final

![[Pasted image 20250822215905.png]]

## 1) Resultado principal (respuesta a la pregunta)

**¿Dónde se concentra el mayor rango de precio en este inventario?**

- Usando percentiles 33–67 como estimador del “rango de concentración” encontramos que **la mayor concentración de precios está entre ≈ 42,000 y 80,000 (moneda local).**
    
- Estadísticas clave del dataset (N = 1,617 registros):
    
    - Mínimo: **1** (valor atípico/documentación).
        
    - Máximo: **806,599**
        
    - Media: **≈ 65,652**
        
    - Mediana: **60,000**
        
    - Percentil 25: **32,686**
        
    - Percentil 33: **42,000**
        
    - Percentil 67: **80,000**
        
    - Percentil 75: **90,000**
        

**Interpretación breve:** la distribución es claramente sesgada a la derecha (cola larga hacia precios altos). La mayoría del inventario se agrupa en la gama baja-media/media (aprox. 42k–80k). Hay relativamente pocos autos premium que empujan la media hacia arriba; la mediana (60k) confirma que la “típica” oferta es de gama media.

---

## 2) Archivo generado (imagen)

He guardado la figura en tu espacio de trabajo:

- **Histograma (precio real con KDE y rango sombreado):**  
    `/mnt/data/histograma_precios_reales.png`
    

(En la interfaz del chat deberías poder descargar ese archivo. Si quieres lo convierto a SVG o a PDF también.)

La figura incluye:

- Histograma (bins de 50,000 en moneda local — elegido según la dispersión).
    
- Curva KDE escalada sobre la frecuencia.
    
- Rango sombreado (33–67 percentil) y líneas punteadas.
    
- Anotación con N y rango estimado.
    

---

## 3) Qué hice (breve metodología)

- Leí y limpié columnas del Excel (renombré columnas a `name, year, km_driven, price, fuel, seller_type, transmission, owner`).
    
- Convertí `price` a numérico (coerce).
    
- Calculé percentiles y estadísticas descriptivas.
    
- Elegí **bin_width = 50,000** (aprox.) por la escala de precios; generé histograma + KDE y sombreé el intervalo 33–67% para marcar la concentración.
    
- Guardé la imagen en `/mnt/data/histograma_precios_reales.png`.
    

Nota: el dataset contiene valores atípicos (ej. precio = 1). Recomiendo revisar y, si corresponde, filtrar registros con precios no plausibles antes de la versión final.

---

## 4) Texto listo para pegar en tu entrega (PDF). Copia y pega tal cual:

**Planteamiento del problema**  
Determinar en qué rango de precio se concentra la mayor parte del inventario de autos usados. Esta información es crítica para segmentación comercial, fijación de precios y estrategias de marketing.

**Visualización propuesta**  
Se utilizó un **histograma** de precios (bins = 50,000 unidades) con una curva de densidad (KDE) superpuesta. El histograma permite visualizar la frecuencia por intervalos de precio; la KDE suaviza la forma de la distribución y ayuda a ver picos de concentración.

**Resultado**  
La mayor concentración del inventario se encuentra aproximadamente entre **42,000 y 80,000** (moneda local). El histograma y la KDE muestran un pico en la parte baja-media del rango, confirmando que la oferta está concentrada en vehículos de gama media.

**Justificación de la elección visual**

- El precio es una variable cuantitativa continua → el histograma (o densidad) es la representación más expresiva y efectiva.
    
- Los bins permiten agrupar y simplificar la lectura (evitan saturación por valores individuales).
    
- La superposición de KDE ayuda a identificar el pico real de la distribución sin depender únicamente de la altura de barras.
    
- Para profundizar: se podrían crear _small multiples_ (histogramas por marca, por año o por tipo de transmisión) o un histograma apilado por categoría (por ejemplo, por `fuel` o `seller_type`) para comparar concentraciones entre subgrupos.
    

**Archivo demostrativo**  
Adjunto el histograma generado con los datos reales: `histograma_precios_reales.png`. (Inserta esta imagen en el PDF y, además, añade la foto del esbozo manual como evidencia del boceto).

---

## 5) Recomendaciones para tu PDF final (Actividad 2)

1. **Foto del boceto manual**: toma una foto nítida del dibujo a mano (buena iluminación, sin sombras).
    
2. **Incluir la figura real** (`histograma_precios_reales.png`) como referencia “computada”.
    
3. **Marcar en el boceto** el rango 42,000–80,000 con color destacado y añadir leyenda/nota explicativa.
    
4. **Anotar posibles anomalías** (e.g., registros con precio = 1; decidir si se excluyen en análisis final).
    
5. **Entregar tanto la foto del boceto como la imagen generada** y el texto (la sección “Resultado” + “Justificación”) en el PDF.
