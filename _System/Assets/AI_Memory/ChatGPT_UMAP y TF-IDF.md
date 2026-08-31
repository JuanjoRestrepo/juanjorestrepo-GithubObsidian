---
title: "UMAP y TF-IDF"
date: 1747705151.568306
tags: [ai_memory, claude_context]
summary: ""
---

### Assistant
Aquí tienes una versión condensada, profesional y clara para incluir en una diapositiva de presentación:

---

### 🗞️ Principales Revistas Publicadoras

- **Liderazgo claro:**  
  🔹 *Sustainability* encabeza con **11 artículos** publicados.

- **Grupo secundario:**  
  🔸 *Business Strategy and the Environment* (3 artículos)  
  🔸 Revistas con 2 artículos:  
  &nbsp;&nbsp;&nbsp;&nbsp;▪ *Cogent Business & Management*  
  &nbsp;&nbsp;&nbsp;&nbsp;▪ *Journal of Cleaner Production*  
  &nbsp;&nbsp;&nbsp;&nbsp;▪ *CSR & Environmental Management*  
  &nbsp;&nbsp;&nbsp;&nbsp;▪ *Cleaner and Responsible Consumption*

- **Alta dispersión:**  
  Otras revistas en el top 10 solo tienen 1 publicación.

---

**🔍 Implicaciones:**

- *Sustainability* es el **foro central** de publicación en el área.
- Las revistas del segundo grupo destacan el enfoque en **medioambiente y responsabilidad social**.
- La **diversidad editorial** refleja la **naturaleza interdisciplinaria** del tema y la necesidad de difusión especializada.

---

¿Quieres que también lo integre en formato gráfico o tabla para visualización en la presentación?

### Human
Combina estos dos analisis y vuelvelos lo mas conciso posible, algo resumidos pero que no pierda el detalle de la explicacion y sentido

Analisis 1:
El gráfico en la sección 3.4 Keywords y UMAP representa una visualización de los documentos de tu conjunto de datos basada en sus palabras clave, utilizando una técnica llamada UMAP (Uniform Manifold Approximation and Projection). Aquí te explico qué significa y representa cada parte:

¿Qué significa?

TF-IDF (Term Frequency-Inverse Document Frequency): Antes de crear el gráfico, el código calcula la representación TF-IDF de las palabras clave (Keywords) de cada documento. TF-IDF es una medida estadística que refleja la importancia de una palabra en un documento en relación con un corpus de documentos. Ayuda a identificar palabras clave que son más relevantes para un documento específico que para el corpus en general. En esencia, convierte el texto de las palabras clave en un formato numérico (un vector) que las computadoras pueden entender.
UMAP (Uniform Manifold Approximation and Projection): UMAP es un algoritmo de reducción de dimensionalidad no lineal. Esto significa que toma datos de alta dimensión (como los vectores TF-IDF de las palabras clave) y los reduce a un número menor de dimensiones (en este caso, 2 dimensiones: umap1 y umap2) mientras intenta preservar la estructura de "vecindad" de los datos originales. En términos sencillos, UMAP intenta colocar documentos con palabras clave similares cerca unos de otros en un espacio 2D.
Gráfico de dispersión (Scatter Plot): El gráfico en sí es un gráfico de dispersión donde cada punto representa un documento de tu base de datos.
Ejes UMAP (umap1 y umap2): Los ejes X (umap1) y Y (umap2) son las dos dimensiones creadas por el algoritmo UMAP. No tienen un significado intrínseco directo (no son "frecuencia" o "año"), sino que representan una proyección del espacio de palabras clave de alta dimensión a un espacio 2D. Documentos cercanos en este espacio 2D son aquellos que, según el análisis de palabras clave, son temáticamente similares.
Color (Hue='Year'): Cada punto en el gráfico está coloreado según el año de publicación del documento (Year). La paleta de colores (palette='viridis') asigna colores diferentes a los distintos años, típicamente con una gradación que muestra el paso del tiempo.
¿Qué representa el gráfico?

El gráfico "UMAP de Documentos según Keywords" te permite visualizar la distribución temática de tus documentos a lo largo del tiempo. Representa:

Agrupaciones Temáticas: Los grupos o clústeres de puntos que se forman en el gráfico sugieren que los documentos en esos grupos tienen conjuntos de palabras clave similares, lo que implica que abordan temas relacionados. Un clúster apretado indica un grupo de documentos temáticamente coherentes.
Evolución Temática a lo largo del Tiempo: El color de los puntos te muestra cómo se distribuyen los documentos de diferentes años en este espacio temático.
Si los puntos de años más recientes se agrupan en una región diferente a los puntos de años más antiguos, sugiere que han surgido nuevos temas o que los temas existentes han evolucionado.
Si los puntos de diferentes años están mezclados de manera uniforme en todo el gráfico, podría indicar que los temas principales han permanecido relativamente constantes a lo largo del tiempo en el corpus.
Si ves patrones de color que forman "caminos" o transiciones, puede sugerir cómo los temas han cambiado o se han desarrollado gradualmente.
Diversidad Temática: La dispersión general de los puntos en el gráfico te da una idea de la diversidad temática del conjunto de datos. Una gran dispersión con múltiples clústeres distintos indica una amplia gama de temas abordados. Un gráfico con un solo clúster grande y denso sugiere que la mayoría de los documentos giran en torno a un tema central muy similar.
En resumen, este gráfico es una herramienta visual poderosa para explorar cómo los temas de investigación representados por las palabras clave se relacionan entre sí y cómo esta estructura temática ha cambiado o permanecido estable a lo largo de los años de publicación en tu base de datos. Te ayuda a identificar temas predominantes, nichos de investigación y la trayectoria temporal del enfoque del corpus.

Analisis 2:
El gráfico que se genera con el código que proporcionaste es una visualización bidimensional de los documentos (artículos) de tu conjunto de datos, proyectados utilizando la técnica de reducción de dimensionalidad UMAP (Uniform Manifold Approximation and Projection), basada en la similitud de sus palabras clave (Keywords).

Aquí te explico qué representa cada parte:

Eje x (umap1) y Eje y (umap2): Estos ejes son las dos dimensiones resultantes de la reducción de dimensionalidad aplicada a las representaciones TF-IDF de las palabras clave de cada documento. En sí mismos, los valores numéricos de umap1 y umap2 no tienen una interpretación directa intuitiva. Lo importante es la posición relativa de los puntos en este espacio bidimensional.

Puntos: Cada punto en el gráfico representa un documento (artículo) en tu conjunto de datos.

Color de los puntos (hue='Year', palette='viridis'): El color de cada punto está determinado por el año de publicación ('Year') del documento. La paleta de colores 'viridis' se utiliza para mapear los valores del año a un espectro de colores. Esto permite visualizar si existen patrones temporales en la distribución de los documentos según sus palabras clave. Por ejemplo, si los documentos con palabras clave similares tienden a agruparse en ciertas regiones del gráfico y esos grupos tienen colores de año similares, podría sugerir una evolución en el uso de las palabras clave a lo largo del tiempo.

En resumen, el gráfico representa:

La similitud entre los documentos basada en sus palabras clave, proyectada en dos dimensiones mediante UMAP. Los documentos que están más cerca unos de otros en este gráfico se consideran más similares en términos de las palabras clave que contienen. Además, el color de cada punto codifica el año de publicación, permitiendo observar si hay alguna relación entre la similitud de las palabras clave y el tiempo.

¿Qué puedes inferir de este gráfico?

Agrupaciones: Si ves grupos de puntos cercanos, sugiere que esos documentos comparten palabras clave similares.
Patrones de color: Si observas tendencias en el color dentro de las agrupaciones (por ejemplo, una región con puntos predominantemente de un cierto rango de años), podría indicar una evolución temporal en las temáticas o el lenguaje utilizado en las palabras clave.
Dispersión: Si los puntos están muy dispersos sin agrupaciones claras, podría significar que los documentos tienen una gran diversidad en sus palabras clave.

### Human
{'asset_pointer': 'file-service://file-6F5Df5T8E8nRcVv9gnFX7Y', 'content_type': 'image_asset_pointer', 'fovea': None, 'height': 548, 'metadata': {'asset_pointer_link': None, 'container_pixel_height': None, 'container_pixel_width': None, 'dalle': None, 'emu_omit_glimpse_image': None, 'emu_patches_override': None, 'generation': None, 'gizmo': None, 'is_no_auth_placeholder': None, 'lpe_delta_encoding_channel': None, 'lpe_keep_patch_ijhw': None, 'sanitized': True, 'segmentation': None, 'watermarked_asset_pointer': None}, 'size_bytes': 40251, 'width': 678}

### Assistant
Aquí tienes una versión condensada, precisa y adecuada para una diapositiva de presentación:

---

### 👥 Patrones de Autoría

- **Predominio individual:**  
  La mayoría de artículos son de **autor único**, lo que destaca la **frecuencia de investigaciones individuales** en el campo.

- **Colaboraciones reducidas:**  
  Los artículos con **2–3 autores** son comunes, reflejando **equipos pequeños** (e.g., estudiante–tutor).

- **Equipos grandes, poco frecuentes:**  
  La producción **disminuye conforme aumenta el número de autores**, lo que indica que **colaboraciones extensas son excepcionales**.

- **Implicación clave:**  
  Se anticipa una **red de coautoría fragmentada**, dominada por nodos individuales o pequeños clústeres, en lugar de grandes comunidades colaborativas.

---

¿Te gustaría acompañar esto con un gráfico de barras o una visualización de red (co-author graph)?

### Human
Okay ahora damelo en formato markdown ordenado

Análisis de la gráfica “UMAP de Documentos según Keywords”

Ejes y distribución general

El eje X (umap1) y el eje Y (umap2) son proyecciones abstractas de la similitud temática basada en TF‑IDF de las keywords.

La nube de puntos acuñada entre ~[4.2, 8.5] en X y [1.8, 7.2] en Y indica una dispersión moderada: no hay un único cúmulo denso, sino varios grupos semifragmentados.

Clústeres temáticos

Se distinguen al menos tres regiones predominantes de densidad media–alta:

Zona inferior‑izquierda (umap1≈4.5–6.0, umap2≈2.0–3.5)

Zona central (umap1≈6.0–7.5, umap2≈4.0–5.5)

Zona superior‑derecha (umap1≈7.5–8.5, umap2≈5.0–7.0)

Cada región sugiere temas o subtemas distintos: los documentos en la misma zona comparten vocabulario clave.

Patrones temporales (color por Year)

La paleta viridis (azul→amarillo) codifica años antiguos (más oscuros) a recientes (más claros).

Mezcla difusa en casi todas las regiones: los puntos claros y oscuros se entrelazan, lo que sugiere que muchos temas han persistido a lo largo del tiempo.

Concentraciones ligeras de amarillos (años más recientes) aparecen en la región superior‑derecha, indicando posibles tópicos emergentes o en expansión.

Outliers y transiciones

Algunos puntos aislados (por ejemplo, en umap1≈5.0, umap2≈4.8) pueden corresponder a documentos muy atípicos o con keywords muy específicas.

Las transiciones de color dentro de los clústeres no forman trayectorias lineales nítidas, lo que apoya la idea de que la evolución temática no es un proceso único o lineal, sino multifacético.

Conclusiones clave

Hay variedad temática: múltiples grupos semidistintos reflejan diferentes líneas de investigación.

Estabilidad y novedad coexisten: la dispersión de colores indica tanto continuidad como la aparición de temas recientes en ciertas regiones.

Úsalo para identificar documentos representativos de cada clúster (centroides) y explorar su contenido como muestra de esos subtemas.

### Assistant
Aquí tienes un ejemplo de cómo estructurar tu análisis en estilo Google Colab, alternando celdas de código y celdas de texto Markdown. Está diseñado para que puedas copiarlo directamente en tu notebook y ejecutarlo paso a paso.

---

```markdown
## 3.4 Análisis de Keywords con TF‑IDF + UMAP

En esta sección calcularemos la representación TF‑IDF de las palabras clave de cada documento, reduciremos la dimensionalidad con UMAP y visualizarémos los resultados en un scatter plot coloreado por año. Esto nos permitirá explorar tanto la similitud temática como la evolución temporal de los documentos.
```

```python
# Celda 1: Imports y carga de datos
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import umap
import matplotlib.pyplot as plt

# Supongamos que ya tienes un DataFrame `df` con columnas 'Keywords' y 'Year'
# Por ejemplo:
# df = pd.read_csv('tu_dataset.csv')
# df.head()
```

```markdown
### Preparación TF‑IDF

Convertimos la columna de Keywords (lista o string) en una matriz TF‑IDF, que cuantifica la importancia de cada término en cada documento frente al corpus total.
```

```python
# Celda 2: Cálculo de TF‑IDF
vectorizer = TfidfVectorizer(
    tokenizer=lambda s: s.split(','),  # si tus keywords vienen separadas por comas
    lowercase=True,
    stop_words='english'
)
tfidfMatrix = vectorizer.fit_transform(df['Keywords'])
print("TF‑IDF matrix shape:", tfidfMatrix.shape)
```

```markdown
La matriz TF‑IDF resultante tiene forma `(n_documentos, n_vocabulario)`, donde cada fila es un documento y cada columna una palabra clave única.
```

```python
# Celda 3: Reducción de dimensionalidad con UMAP
reducer = umap.UMAP(n_components=2, random_state=42)
embedding = reducer.fit_transform(tfidfMatrix)
df_umap = pd.DataFrame(embedding, columns=['umap1', 'umap2'])
df_umap['Year'] = df['Year'].values

# Mostrar las primeras filas de la proyección
df_umap.head()
```

```markdown
|   |   umap1  |   umap2  | Year |
|---|---------:|---------:|-----:|
| 0 |  1.2345  | -0.6789  | 2018 |
| 1 | -0.5432  |  0.1234  | 2020 |
| 2 |  0.9876  | -1.2345  | 2019 |
| … |     …    |     …    |  …   |

Este fragmento muestra cómo cada documento se ha proyectado a dos dimensiones (`umap1`, `umap2`), junto con su año de publicación.
```

```python
# Celda 4: Gráfico de dispersión coloreado por año
plt.figure(figsize=(8,6))
scatter = plt.scatter(
    df_umap['umap1'],
    df_umap['umap2'],
    c=df_umap['Year'],
    cmap='viridis',
    alpha=0.7
)
cbar = plt.colorbar(scatter)
cbar.set_label('Year')
plt.title('UMAP de documentos según Keywords')
plt.xlabel('umap1')
plt.ylabel('umap2')
plt.tight_layout()
plt.show()
```

```markdown
### Interpretación de la salida gráfica

1. **Clústeres temáticos**  
   - Las agrupaciones de puntos indican subconjuntos de documentos que comparten palabras clave similares.  
2. **Evolución temporal**  
   - El degradado de colores (2010→2025 en viridis) revela si hay regiones dominadas por años recientes o antiguos.  
   - Zonas homogéneas en un mismo color sugieren temas que emergieron o evolucionaron en un período concreto.  
3. **Diversidad de tópicos**  
   - Una gran dispersión con varios clústeres apunta a una amplia variedad de temas.  
   - Un único cúmulo compacto indicaría un foco temático central.

---

Con este notebook tienes tanto el **código reproducible** como las **explicaciones intercaladas** en Markdown. Así logras un flujo claro: importación y carga de datos, transformación TF‑IDF, reducción con UMAP, visualización y análisis de resultados. Si necesitas profundizar en parámetros (p. ej. `n_neighbors`, `min_dist` de UMAP) o en preprocesamiento de texto, dime y lo integramos.

### Human
Temas dominantes: Las palabras clave más frecuentes (p. ej. “sustainability”, “small and medium enterprises”, “value creation”, etc.) reflejan el núcleo conceptual del estudio, centrado en prácticas sostenibles en PYMES y creación de valor compartido.
Diversidad temática: Aunque existe un pequeño conjunto de términos muy recurrentes, el “long tail” de keywords (más de 150 términos únicos) indica una amplia variedad de enfoques y subtemas, desde métodos específicos (“case study”, “survey”) hasta dimensiones geográficas (“emerging economies”).
Agrupamiento futuro: Para un análisis temático avanzado, conviene agrupar sinónimos y variantes (p. ej. “sme” vs. “small and medium enterprises”), y aplicar técnicas de reducción de dimensionalidad o clustering (p. ej. LDA, k‑means sobre TF-IDF) para descubrir tópicos emergentes.

### Assistant
```markdown
# Análisis de la gráfica “UMAP de Documentos según Keywords”

## 1. Ejes y distribución general
- **Eje X (umap1) y eje Y (umap2)**  
  Proyecciones abstractas de la similitud temática basada en TF‑IDF de las keywords.
- **Dispersión de puntos**  
  La nube se extiende aproximadamente entre X ≈ [4.2, 8.5] y Y ≈ [1.8, 7.2], mostrando varios grupos semifragmentados en lugar de un único cúmulo denso.

## 2. Clústeres temáticos
Se identifican tres regiones de densidad media–alta, cada una representando un subtema:

1. **Zona inferior‑izquierda**  
   - Coordenadas: umap1 ≈ 4.5–6.0, umap2 ≈ 2.0–3.5  
   - Interpretación: conjunto de documentos con keywords muy afines.

2. **Zona central**  
   - Coordenadas: umap1 ≈ 6.0–7.5, umap2 ≈ 4.0–5.5  
   - Interpretación: otro grupo temático consistente.

3. **Zona superior‑derecha**  
   - Coordenadas: umap1 ≈ 7.5–8.5, umap2 ≈ 5.0–7.0  
   - Interpretación: posible región de temas emergentes.

## 3. Patrones temporales (color por Year)
- **Paleta viridis** (azul→amarillo) codifica años antiguos (oscuros) a recientes (claros).  
- **Mezcla difusa**: puntos claros y oscuros se entrelazan en casi todas las regiones, indicando persistencia de muchos temas a lo largo del tiempo.  
- **Mayor presencia de amarillos** en la zona superior‑derecha, sugiriendo tópicos más recientes o en expansión.

## 4. Outliers y transiciones
- **Puntos aislados** (p. ej. umap1 ≈ 5.0, umap2 ≈ 4.8): documentos atípicos o con keywords muy específicas.  
- **Transiciones de color no lineales**: la evolución temática parece multifacética, sin un solo “camino” claro.

## 5. Conclusiones clave
- **Diversidad temática**: múltiples grupos semidistintos reflejan distintas líneas de investigación.  
- **Continuidad y novedad**: coexistencia de temas estables y emergentes.  
- **Próximos pasos**:  
  - Extraer “top‑keywords” por clúster para caracterizar cada subtema.  
  - Ajustar parámetros de UMAP (p. ej. `n_neighbors`, `min_dist`) si deseas afinar la separación.  
  - Seleccionar documentos representativos (centroides) para análisis cualitativo.  
```

### Assistant
**Análisis de la gráfica “UMAP de Documentos según Keywords”**  

1. **Ejes y distribución general**  
   - El eje X (umap1) y el eje Y (umap2) son proyecciones abstractas de la similitud temática basada en TF‑IDF de las keywords.  
   - La nube de puntos acuñada entre ~[4.2, 8.5] en X y [1.8, 7.2] en Y indica una dispersión moderada: no hay un único cúmulo denso, sino varios grupos semifragmentados.

2. **Clústeres temáticos**  
   - Se distinguen al menos **tres regiones** predominantes de densidad media–alta:  
     1. **Zona inferior‑izquierda** (umap1≈4.5–6.0, umap2≈2.0–3.5)  
     2. **Zona central** (umap1≈6.0–7.5, umap2≈4.0–5.5)  
     3. **Zona superior‑derecha** (umap1≈7.5–8.5, umap2≈5.0–7.0)  
   - Cada región sugiere temas o subtemas distintos: los documentos en la misma zona comparten vocabulario clave.

3. **Patrones temporales (color por Year)**  
   - La paleta viridis (azul→amarillo) codifica años antiguos (más oscuros) a recientes (más claros).  
   - **Mezcla difusa** en casi todas las regiones: los puntos claros y oscuros se entrelazan, lo que sugiere que muchos temas han persistido a lo largo del tiempo.  
   - **Concentraciones ligeras de amarillos** (años más recientes) aparecen en la región superior‑derecha, indicando posibles tópicos emergentes o en expansión.

4. **Outliers y transiciones**  
   - Algunos puntos aislados (por ejemplo, en umap1≈5.0, umap2≈4.8) pueden corresponder a documentos muy atípicos o con keywords muy específicas.  
   - Las transiciones de color dentro de los clústeres no forman trayectorias lineales nítidas, lo que apoya la idea de que la evolución temática no es un proceso único o lineal, sino multifacético.

5. **Conclusiones clave**  
   - Hay **variedad temática**: múltiples grupos semidistintos reflejan diferentes líneas de investigación.  
   - **Estabilidad y novedad** coexisten: la dispersión de colores indica tanto continuidad como la aparición de temas recientes en ciertas regiones.  
   - Úsalo para identificar documentos representativos de cada clúster (centroides) y explorar su contenido como muestra de esos subtemas.  

Este análisis te ayudará a orientar exploraciones más específicas: p. ej., extraer top‑keywords por clúster o trazar su evolución ajustando parámetros de UMAP (n_neighbors, min_dist).

### Human
1. **Sustainability** aparece con **11 publicaciones**, liderando con claridad el campo.  
2. **Business Strategy and the Environment** ocupa el segundo lugar con **3 artículos**, seguido por varias revistas con 2 publicaciones:  
   - Cogent Business & Management  
   - Journal of Cleaner Production  
   - Corporate Social Responsibility and Environmental Management  
   - Cleaner and Responsible Consumption  
3. El resto del top 10 está compuesto por revistas con 1 artículo cada una, lo cual indica dispersión más allá del núcleo principal.

**Implicaciones:**

- **Canal principal**: Sustainability actúa como el foro de publicación dominante para investigaciones sobre sostenibilidad y PYMES.  
- **Especialización temática**: Las revistas del segundo grupo (Journal of Cleaner Production, CSR & Environmental Management, etc.) sugieren énfasis en aspectos medioambientales y de responsabilidad social.  
- **Diversidad de canales**: Aunque existe un líder claro, hay un espectro amplio de revistas de nicho—esto refleja tanto la interdisciplinariedad del tema como la necesidad de difundir hallazgos en foros especializados.  

### Human
Dominancia de la Autoría Individual: Se observa una clara predominancia de artículos con un solo autor, lo que indica que la autoría individual es una modalidad frecuente en este corpus.
Colaboración en Equipos Pequeños: Hay una presencia notable de artículos con 2 y 3 autores, sugiriendo colaboraciones típicas de equipos reducidos (por ejemplo, supervisor–estudiante o colegas cercanos).
Colaboraciones de Mayor Tamaño son Menos Frecuentes: A medida que aumenta el número de autores, el número de publicaciones disminuye, lo que implica que los equipos grandes son la excepción.
Implicaciones para Redes de Coautoría: Esta distribución anticipa una red de colaboración dispersa, con muchos autores aislados o en pequeños clústeres, más que grandes agrupaciones densas.

### Assistant
Aquí tienes una versión condensada, clara y profesional para una diapositiva de presentación:

---

### 🔑 Análisis de Palabras Clave

- **Temas centrales:**  
  Predominan términos como **“sustainability”**, **“small and medium enterprises”** y **“value creation”**, que definen el **núcleo conceptual** del estudio.

- **Diversidad temática:**  
  Más de **150 keywords únicas** reflejan una **amplia variedad de enfoques**: métodos (e.g., *case study*), geografías (e.g., *emerging economies*) y perspectivas multidisciplinarias.

- **Recomendación analítica:**  
  Para análisis avanzados, se sugiere:  
  → **Agrupar sinónimos** (e.g., *SME* ↔ *small and medium enterprises*)  
  → Aplicar **técnicas de reducción/clustering** (e.g., **LDA**, **k-means sobre TF-IDF**) para identificar **tópicos emergentes**.

---

¿Deseas también una nube de palabras o una visualización tipo dendrograma para mostrar agrupamientos temáticos?

### Assistant
A continuación encontrarás un análisis combinado y condensado de ambos textos, manteniendo el nivel de detalle y claridad:

**Resumen Ejecutivo**  
El gráfico de UMAP aplica una reducción de dimensionalidad a las representaciones TF‑IDF de las palabras clave de cada documento, proyectándolas en dos dimensiones (umap1, umap2). Cada punto simboliza un artículo y su posición refleja la similitud temática: los puntos cercanos comparten vocabulario relevante. Además, el color de cada punto, basado en la variable “Year” con la paleta viridis, permite visualizar patrones temporales en la evolución de los temas.

---

## 1. Preparación de datos  
- **TF‑IDF de Keywords**: Se transforma el conjunto de palabras clave en vectores numéricos que destacan la relevancia de cada término en su propio documento frente al corpus.  
- **Dimensionalidad alta → baja**: UMAP reduce esos vectores de cientos o miles de dimensiones a dos, intentando conservar la estructura de vecindad (documentos similares siguen juntos).

## 2. Elementos del gráfico  
- **Ejes umap1 y umap2**: Son coordenadas abstractas sin interpretación semántica directa; solo importan las distancias y agrupaciones.  
- **Puntos**: Cada uno representa un documento.  
- **Color (‘Year’, palette='viridis')**: Indica el año de publicación, facilitando la detección de cambios temáticos a lo largo del tiempo.

## 3. Interpretación  
1. **Clústeres temáticos**  
   - Agrupaciones densas señalan subconjuntos de documentos con palabras clave muy afines.  
2. **Evolución temporal**  
   - Si los colores forman zonas diferenciadas, sugiere que han emergido o evolucionado temas nuevos en ciertos periodos.  
   - Una mezcla uniforme de colores implica estabilidad temática.  
3. **Diversidad del corpus**  
   - Amplia dispersión con múltiples clústeres: gran variedad de temas.  
   - Un único clúster compacto: predominio de un tema central.

---

**Conclusión**  
Este UMAP de documentos según keywords es una herramienta visual eficaz para:  
- Explorar la coherencia temática interna del corpus.  
- Detectar tendencias y cambios en los temas a través de los años.  
- Medir la diversidad y la concentración de tópicos en tu conjunto de datos.  

Si deseas profundizar en algún aspecto (por ejemplo, optimizar parámetros de UMAP o explorar subclústeres), házmelo saber.

### Human
Okay pero me gustaria un analisis tipo google colab, donde tengo el codigo y luego hago la explicacion de la salidas, un grafico, tabla o valores, en una celda de texto markdown

### Assistant
Aquí tienes una versión condensada y clara para usar directamente en una diapositiva de presentación:

---

### 🔑 Análisis de Palabras Clave

- **Temas centrales:**  
  Términos frecuentes como *sustainability*, *small and medium enterprises* y *value creation* revelan el **enfoque conceptual en sostenibilidad y valor compartido en PYMEs**.

- **Alta diversidad temática:**  
  El “long tail” de +150 keywords únicas sugiere **variedad de enfoques**, desde métodos (*case study*, *survey*) hasta contextos regionales (*emerging economies*).

- **Oportunidad analítica:**  
  Se recomienda **agrupar sinónimos** (e.g., *SME* vs *small and medium enterprises*) y aplicar técnicas como **LDA o clustering sobre TF-IDF** para detectar tópicos emergentes.

---

¿Deseas una visualización tipo nube de palabras o una matriz de coocurrencia para complementar esta diapositiva?

### Human
Ayudame a condensar esto para ponerlo en una presentacion

El análisis de la producción académica muestra un crecimiento significativo en el número de artículos entre 2004 y 2025, dividido en tres fases:
Fase Formativa (2004–2019): Producción baja y estable (1–3 artículos por año), con interés aún incipiente y concentrado en pocos núcleos académicos.
Fase de Consolidación (2020–2022): Aumento sostenido de publicaciones, impulsado por la pandemia y la atención a la sostenibilidad en PYMEs. Se forma una comunidad académica más cohesionada.
Fase de Auge Emergente (2023–2025): Explosión de publicaciones: pico en 2023 (58 artículos), ligero descenso en 2024 (44). El crecimiento anual compuesto (CAGR ≈ 44 %) confirma un fuerte impulso sostenido. La caída en 2024 podría deberse a desfases en la indexación o a ciclos de financiación.

### Assistant
Aquí tienes una versión condensada y clara para usar en una diapositiva de presentación:

---

### 📈 Evolución de la Producción Académica (2004–2025)

- **Crecimiento marcado** en publicaciones, con un **CAGR ≈ 44 %**.  
- **Tres fases identificadas**:

  - 🟢 **Fase Formativa (2004–2019)**  
    Producción baja y estable (1–3 artículos/año); interés incipiente y concentrado.

  - 🔵 **Fase de Consolidación (2020–2022)**  
    Aumento sostenido tras la pandemia; formación de comunidad académica.

  - 🟠 **Fase de Auge Emergente (2023–2025)**  
    Pico en 2023 (58 artículos), leve baja en 2024 (44); posible efecto de desfases en indexación o ciclos de financiación.

---

¿Deseas que lo convierta en slide markdown con estilo `reveal.js` u otro formato específico para presentaciones?

### Human
Temas dominantes: Las palabras clave más frecuentes (p. ej. “sustainability”, “small and medium enterprises”, “value creation”, etc.) reflejan el núcleo conceptual del estudio, centrado en prácticas sostenibles en PYMES y creación de valor compartido.
Diversidad temática: Aunque existe un pequeño conjunto de términos muy recurrentes, el “long tail” de keywords (más de 150 términos únicos) indica una amplia variedad de enfoques y subtemas, desde métodos específicos (“case study”, “survey”) hasta dimensiones geográficas (“emerging economies”).
Agrupamiento futuro: Para un análisis temático avanzado, conviene agrupar sinónimos y variantes (p. ej. “sme” vs. “small and medium enterprises”), y aplicar técnicas de reducción de dimensionalidad o clustering (p. ej. LDA, k‑means sobre TF-IDF) para descubrir tópicos emergentes.

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - AI Memory & Context]]
- **Dominio**: AI Memory & Context Knowledge Base
