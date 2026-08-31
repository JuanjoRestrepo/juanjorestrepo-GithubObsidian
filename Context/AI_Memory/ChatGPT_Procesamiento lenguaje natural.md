---
title: "Procesamiento lenguaje natural"
date: 1732983473.344398
tags: [ai_memory, claude_context]
summary: ""
---

### Assistant
Tu código está bien estructurado en general, pero para evitar errores o redundancia, podemos integrar la generación automática del diccionario `word_freq` directamente desde el DataFrame de Spark, eliminando la necesidad de ingresarlo manualmente en la segunda parte.

Aquí te proporciono una versión refinada que conecta ambas partes y utiliza el DataFrame para generar automáticamente la nube de palabras:

### **Código completo desde cero**

#### Parte 1: Contar palabras desde el PDF

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col
import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Inicializar SparkSession
spark = SparkSession.builder.appName("CountWordsPDF").getOrCreate()

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return ""  # Retorna cadena vacía si no encuentra el archivo
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""  # Retorna cadena vacía para otros errores
    return text

# Ruta al archivo PDF
PDF_Path = '/content/drive/MyDrive/Master Data Science 2024/Gestion De Datos/Actividad 6/colombiaint-3824.pdf'

# Extraer texto del PDF
pdf_text = extract_text_from_pdf(PDF_Path)

if pdf_text:
    # Crear un DataFrame con el texto
    data = [(pdf_text,)]
    df = spark.createDataFrame(data, ["text"])

    # Dividir el texto en palabras
    words_df = df.select(explode(split(lower(col("text")), r"\s+")).alias("word"))

    # Contar las palabras
    word_counts = words_df.groupBy("word").count().orderBy(col("count").desc())

    # Mostrar los resultados
    word_counts.show(50, truncate=False)

    # Convertir a un diccionario para la nube de palabras
    word_freq = {row.word: row['count'] for row in word_counts.collect()}

    # Generar la nube de palabras
    wordcloud = WordCloud(background_color="gray", colormap='viridis').generate_from_frequencies(word_freq)

    # Mostrar la nube de palabras
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Nube de Palabras", fontsize=16)
    plt.show()
else:
    print("No se pudo extraer texto del archivo PDF. Verifica la ruta del archivo y los permisos.")

# Detener la SparkSession
spark.stop()
```

### **Puntos importantes**

1. **Generación automática del diccionario**:
   - Utilizamos `word_counts.collect()` para obtener los datos del DataFrame de Spark como una lista de objetos `Row`, y luego construimos un diccionario `word_freq` directamente.

2. **Expresión regular para dividir palabras**:
   - `r"\s+"` asegura que se dividan palabras usando cualquier cantidad de espacios, tabulaciones, etc.

3. **Visualización de la nube de palabras**:
   - Integramos la generación y visualización de la nube de palabras en una sola sección después de procesar los datos.

### **Resultados esperados**
1. Un conteo de palabras ordenado por frecuencia, mostrado en la consola.
2. Una nube de palabras visualmente atractiva generada dinámicamente.

Con este flujo, no tendrás que definir manualmente el diccionario `word_freq`. ¡Déjame saber si necesitas más ajustes! 😊

### Assistant
¡Gran avance! Tu implementación en Colab es funcional y eficiente para contar palabras y generar una nube de palabras a partir de un archivo PDF. A continuación, te sugiero algunas mejoras y consideraciones para perfeccionar el análisis y adaptarlo al caso propuesto:

---

### **1. Eliminación de palabras irrelevantes**
Muchas palabras comunes (*stop words*) como "de", "la", "y", "que" no aportan valor analítico. Puedes eliminarlas para centrarte en términos más significativos:

```python
from pyspark.sql.functions import regexp_replace

# Lista de palabras vacías (stop words)
stop_words = ["de", "la", "y", "que", "en", "el", "los", "a", "las", "se", "una", "es", "por", "como", "del", "para", "con", "un", "lo", "al", "más", "sobre", "entre"]

# Filtrar las stop words y palabras vacías
words_df_filtered = words_df.filter(~col("word").isin(stop_words))

# Eliminar puntuaciones y caracteres especiales
words_df_cleaned = words_df_filtered.withColumn("word", regexp_replace("word", r"[^\w]", ""))

# Contar palabras limpias
word_counts_cleaned = words_df_cleaned.groupBy("word").count().orderBy(col("count").desc())
word_counts_cleaned.show(50)
```

---

### **2. Generación dinámica de la nube de palabras**
Usar los datos filtrados de Spark para generar la nube de palabras directamente desde el conteo procesado:

```python
# Convertir los resultados de Spark a un diccionario
word_freq_cleaned = {row['word']: row['count'] for row in word_counts_cleaned.collect()}

# Crear la nube de palabras
wordcloud = WordCloud(background_color="white", colormap='viridis').generate_from_frequencies(word_freq_cleaned)

# Mostrar la nube
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
```

---

### **3. Exportar los resultados**
Guarda el conteo de palabras en un archivo para futuras referencias:

```python
word_counts_cleaned.write.csv("conteo_palabras_limpias.csv", header=True)
```

Esto generará un archivo CSV con las palabras y sus frecuencias.

---

### **4. Consideraciones para el caso planteado**
- **Adaptación al español**: Revisa la lista de *stop words* en español para asegurarte de que estás eliminando todas las palabras funcionales irrelevantes.
- **Visualización adicional**: Puedes crear gráficos de barras para mostrar las palabras más frecuentes, lo que podría complementar la nube de palabras.

```python
# Crear un gráfico de barras
import pandas as pd
import seaborn as sns

# Convertir a Pandas para graficar
df_cleaned = word_counts_cleaned.limit(10).toPandas()

# Gráfico
sns.barplot(x="count", y="word", data=df_cleaned, palette="viridis")
plt.title("Top 10 Palabras Más Frecuentes")
plt.xlabel("Frecuencia")
plt.ylabel("Palabras")
plt.show()
```

---

### **5. Reflexión y conclusiones**
- **Ventaja de Spark**: El procesamiento distribuido permite manejar textos de mayor tamaño y realizar análisis más complejos si decides ampliar el alcance del caso.
- **Aplicaciones futuras**: El mismo enfoque puede aplicarse a análisis de sentimientos, categorización de temas o identificación de intenciones en textos más grandes.

¿Te gustaría que trabajemos en alguna parte específica, como optimizar el preprocesamiento o analizar más profundamente el archivo PDF?

### Assistant
¡Entendido! Si no deseas eliminar palabras comunes como *stop words*, nos enfocaremos en mejorar la claridad y presentación de los resultados sin aplicar filtros adicionales. A continuación, te sugiero algunas modificaciones útiles:

---

### **1. Mostrar resultados más claros**
Si deseas mantener todas las palabras, incluidas las comunes, pero quieres resaltar su frecuencia, puedes organizar el resultado para que sea más legible:

```python
# Mostrar las palabras más frecuentes en un formato ordenado
word_counts.show(50, truncate=False)
```

Esto evitará el truncamiento de palabras en los resultados y mostrará la lista completa de las más frecuentes.

---

### **2. Generación directa de la nube de palabras**
Como no se filtrarán palabras, puedes usar los resultados actuales de `word_counts` para generar la nube de palabras sin cambios adicionales:

```python
# Crear un diccionario a partir de los resultados de Spark
word_freq = {row['word']: row['count'] for row in word_counts.collect()}

# Generar la nube de palabras
wordcloud = WordCloud(background_color="white", colormap='viridis').generate_from_frequencies(word_freq)

# Mostrar la nube
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras sin Filtrar")
plt.show()
```

---

### **3. Exportar todas las palabras**
Si deseas guardar el conteo completo de palabras (sin omitir ninguna) en un archivo para su análisis posterior:

```python
word_counts.write.csv("conteo_palabras_completo.csv", header=True)
```

Esto generará un archivo CSV con todas las palabras procesadas y sus frecuencias.

---

### **4. Gráfico de barras de las palabras más frecuentes**
Incluso sin filtrar, un gráfico de barras puede ayudar a destacar la relevancia de las palabras más comunes:

```python
# Convertir a Pandas
top_words_df = word_counts.limit(20).toPandas()

# Gráfico
sns.barplot(x="count", y="word", data=top_words_df, palette="coolwarm")
plt.title("Top 20 Palabras Más Frecuentes (Sin Filtrar)")
plt.xlabel("Frecuencia")
plt.ylabel("Palabras")
plt.show()
```

---

### **5. Reflexión del análisis sin filtro**
- Al incluir todas las palabras, el análisis mostrará con precisión cuáles son las más frecuentes, independientemente de su utilidad semántica.
- Mantener todas las palabras puede ser útil en algunos contextos, como análisis estilísticos o estudio de estructuras lingüísticas.

¿Hay algún detalle específico que quieras ajustar o profundizar en el análisis? 😊

### Human
Vamos desde cero.

Este es el codigo
# prompt: contar palabras de un archivo pdf usando python y spark

#!pip install pyspark
#!pip install PyPDF2

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col
import PyPDF2
path = '/content/drive/MyDrive/Master Data Science 2024/Gestion De Datos/Actividad 6/colombiaint-3824.pdf'

# Inicializar SparkSession
spark = SparkSession.builder.appName("CountWordsPDF").getOrCreate()

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return ""  # Return empty string if file not found
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""  # Return empty string for other errors
    return text

# Ruta al archivo PDF
PDF_Path = '/content/drive/MyDrive/Master Data Science 2024/Gestion De Datos/Actividad 6/colombiaint-3824.pdf'
pdf_file_path = "colombiaint-3824.pdf" # Reemplaza con la ruta a tu archivo

# Extraer texto del PDF
pdf_text = extract_text_from_pdf(PDF_Path)

# Crear un DataFrame con el texto
if pdf_text:
    data = [(pdf_text,)]
    df = spark.createDataFrame(data, ["text"])

    # Dividir el texto en palabras
    words_df = df.select(explode(split(lower(col("text")), "\s+")).alias("word"))

    # Contar las palabras
    word_counts = words_df.groupBy("word").count().orderBy(col("count").desc())

    # Mostrar los resultados
    word_counts.show(50, truncate=False)
else:
    print("No se pudo extraer texto del archivo PDF. Verifica la ruta del archivo y los permisos.")

# Detener la SparkSession
spark.stop()

SALIDA
+-----------+-----+
|word       |count|
+-----------+-----+
|de         |641  |
|la         |314  |
|y          |305  |
|que        |249  |
|en         |228  |
|el         |169  |
|los        |169  |
|a          |142  |
|las        |133  |
|se         |132  |
|datos      |117  |
|una        |85   |
|-          |70   |
|es         |66   |
|estudios   |62   |
|por        |61   |
|como       |61   |
|of         |57   |
|del        |56   |
|•          |54   |
|para       |52   |
|con        |51   |
|the        |50   |
|un         |50   |
|data       |49   |
|lo         |48   |
|ciencia    |47   |
|información|47   |
|and        |45   |
|big        |45   |
|no         |42   |
|análisis   |40   |
|este       |38   |
|al         |35   |
|más        |35   |
|global     |33   |
|sobre      |31   |
|globales   |30   |
|.          |29   |
|e          |29   |
|son        |27   |
|o          |26   |
|entre      |25   |
|ha         |25   |
|desde      |25   |
|sin        |23   |
|,          |23   |
|patrones   |22   |
|puede      |21   |
|ser        |21   |
+-----------+-----+
only showing top 50 rows

sEGUNDA PARTE
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Datos de frecuencia de palabras (ajusta según tu conteo)
word_freq = {
    'de': 641,
'la': 314,
'y': 305,
'que': 249,
'en': 228,
'el': 169,
'los': 169,
'a': 142,
'las': 133,
'se': 132,
'datos': 117,
'una': 85,
'-': 70,
'es': 66,
'estudios': 62,
'por': 61,
'como': 61,
'of': 57,
'del': 56,
'•': 54,
'para': 52,
'con': 51,
'the': 50,
'un': 50,
'data': 49,
'lo': 48,
'ciencia': 47,
'información': 47,
'and': 45,
'big': 45,
'no': 42,
'análisis': 40,
'este': 38,
'al': 35,
'más': 35,
'global': 33,
'sobre': 31,
'globales': 30,
'.': 29,
'e': 29,
'son': 27,
'o': 26,
'entre': 25,
'ha': 25,
'desde': 25,
'sin': 23,
',': 23,
'patrones': 22,
'puede': 21,
'ser': 21,
}

# Crear una instancia de WordCloud
# Generar la nube de palabra
wordcloud = WordCloud(background_color="gray", colormap='viridis').generate_from_frequencies(word_freq)

# Mostrar la nube de palabras
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras")
plt.show()



### Human
Por favor no quites esas palabras que consideras irrelevantes

### Human
Tengo una nueva actividad

Contexto
Desde hace varios siglos, uno de los principales métodos de comunicación de
los seres humanos ha sido el texto escrito. Historias y conocimiento
acumulados a lo largo del tiempo han sido transmitidos de generación en
generación por medio de diarios informativos, revistas o libros.
Con el advenimiento de la era digital, el texto escrito ha tomado una mayor
relevancia. Diariamente son miles de personas las que expresan sentimientos
o posiciones políticas por medio de estados de Facebook o trinos de Twitter.
Es a raíz de estas interacciones masivas, que ocurren en las aplicaciones, que
las grandes empresas, dueñas de las mismas, se han dado cuenta de la
importancia de los textos compartidos. Estos se convierten, prácticamente, en
una mina de información que los empresarios pueden aprovechar para
distintos objetivos como analizar tendencias y sentimientos o verificar los
gustos de los usuarios con fines publicitarios.
Por su parte, en el área investigativa, el conocimiento y los datos están
diseminados en forma escrita a través de artículos científicos y reportes
técnicos. A su vez, la información también está diseminada de forma verbal a
través de interacciones científicas en conferencias, seminarios y consultas
[Friedman & Jhonson], por lo que se vuelve indispensable el uso de un método
con el que los investigadores logren encontrar información valiosa en esta
multitud de fuentes de datos que se pueden encontrar a lo largo y ancho de
la red.
En ese sentido, el Procesamiento del Lenguaje Natural, NLP por sus siglas en
inglés, aparece en escena como un área de las ciencias de la computación que
busca la obtención de información a partir de textos escritos e incluso lenguaje
hablado, y donde el Machine Learning y la Lingüística Computacional son
ampliamente usados [Vrah Shaj]. Uno de los tantos objetivos del NLP es la
extracción de significado a partir de grandes volúmenes de texto: gramáticas
formales que especifican relaciones entre unidades y partes del habla como
sustantivos, verbos o adjetivos [Chapman]. Para lograr esto, NLP hace uso,
internamente, de la técnica conocida como Procesamiento de Texto, una de
las formas de procesamiento distribuido de datos.
Con el procesamiento de texto se busca realizar tareas como tokenización,
conteo de palabras y generación, manipulación y análisis de textos. Algunos
de los usos más frecuentes del procesamiento de textos son el análisis de
temáticas donde se busca categorizar colecciones grandes de textos en temas;
el análisis de sentimientos donde la meta principal es detectar tonos
emocionales de un texto de forma que se pueda clasificar como positivo,
negativo o neutro; y la detección de intención donde el objetivo es detectar la
intención de un texto, por ejemplo si determinado texto busca obtener
información o realizar una compra o una venta.
Caso
Partiendo de lo planteado previamente, imaginen que un profesional está
realizando una investigación sobre determinado tema de su interés y quiere
saber cuántas veces aparecen determinadas palabras en una publicación de
caracter científico que piensa utilizar a modo de referencia bibliográfica en su
propio trabajo investigativo. Teniendo en cuenta que el artículo puede llegar
a tener entre 15 y 20 páginas, sería complicado para el investigador contar
por sí mismo las palabras, por lo que desea usar una herramienta que le
permita procesar el texto y realizar el conteo en un menor tiempo.
Alcance
Para resolver el caso deben tener en cuenta las herramientas que estudiamos
en esta unidad. Recuerden que cada herramienta, Hadoop o Spark, utiliza un
Modelo de Procesamiento Distribuido distinto y goza de ciertas características,
por lo que deben analizar cómo realizar el conteo de palabras y seleccionar la
herramienta que mejor se ajuste al caso propuesto. Adicionalmente,
considerar lo siguiente:
1. Buscar un artículo científico de su interés de entre 10 a 20 páginas. El
texto de este artículo es el que usarán junto a Hadoop o Spark para
realizar el conteo de palabras.
2. El conteo de palabras se debe realizar sobre la totalidad del texto que
compone el artículo.
3. El artículo debe estar en idioma español pues la idea es hacer
comparaciones para dicho idioma.
4. El resultado del conteo de palabras debe tener una estructura similar a
la que se presenta a continuación:
sigamos, 1
aprendiendo, 7
sobre, 4
la, 20
gestión, 5
de, 15
datos, 5




### Human
Hay un error aqui: word_freq = {row['word']: row['count'] for row in word_counts.collect()}
AttributeError                            Traceback (most recent call last)
<ipython-input-14-9ee541e74442> in <cell line: 5>()
      3 
      4 # Datos de frecuencia de palabras (ajusta según tu conteo)
----> 5 word_freq = {row['word']: row['count'] for row in word_counts.collect()}
      6 '''
      7 word_freq = {

1 frames
/usr/local/lib/python3.10/dist-packages/pyspark/traceback_utils.py in __enter__(self)
     73     def __enter__(self):
     74         if SCCallSiteSync._spark_stack_depth == 0:
---> 75             self._context._jsc.setCallSite(self._call_site)
     76         SCCallSiteSync._spark_stack_depth += 1
     77 

AttributeError: 'NoneType' object has no attribute 'setCallSite'

### Human
Esto es lo que llevo en Colab con Python

# prompt: contar palabras de un archivo pdf usando python y spark

#!pip install pyspark
#!pip install PyPDF2

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col
import PyPDF2


# Inicializar SparkSession
spark = SparkSession.builder.appName("CountWordsPDF").getOrCreate()

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return ""  # Return empty string if file not found
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""  # Return empty string for other errors
    return text

# Ruta al archivo PDF
pdf_file_path = "colombiaint-3824.pdf" # Reemplaza con la ruta a tu archivo

# Extraer texto del PDF
pdf_text = extract_text_from_pdf(pdf_file_path)

# Crear un DataFrame con el texto
if pdf_text:
    data = [(pdf_text,)]
    df = spark.createDataFrame(data, ["text"])

    # Dividir el texto en palabras
    words_df = df.select(explode(split(lower(col("text")), "\s+")).alias("word"))

    # Contar las palabras
    word_counts = words_df.groupBy("word").count().orderBy(col("count").desc())

    # Mostrar los resultados
    word_counts.show(50)
else:
    print("No se pudo extraer texto del archivo PDF. Verifica la ruta del archivo y los permisos.")

# Detener la SparkSession
spark.stop()


SALIDA
+-----------+-----+
|       word|count|
+-----------+-----+
|         de|  641|
|         la|  314|
|          y|  305|
|        que|  249|
|         en|  228|
|         el|  169|
|        los|  169|
|          a|  142|
|        las|  133|
|         se|  132|
|      datos|  117|
|        una|   85|
|          -|   70|
|         es|   66|
|   estudios|   62|
|        por|   61|
|       como|   61|
|         of|   57|
|        del|   56|
|          •|   54|
|       para|   52|
|        con|   51|
|        the|   50|
|         un|   50|
|       data|   49|
|         lo|   48|
|    ciencia|   47|
|información|   47|
|        and|   45|
|        big|   45|
|         no|   42|
|   análisis|   40|
|       este|   38|
|         al|   35|
|        más|   35|
|     global|   33|
|      sobre|   31|
|   globales|   30|
|          .|   29|
|          e|   29|
|        son|   27|
|          o|   26|
|      entre|   25|
|         ha|   25|
|      desde|   25|
|        sin|   23|
|          ,|   23|
|   patrones|   22|
|      puede|   21|
|        ser|   21|
+-----------+-----+
only showing top 50 rows


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Datos de frecuencia de palabras (ajusta según tu conteo)
word_freq = {
    'de': 641,
'la': 314,
'y': 305,
'que': 249,
'en': 228,
'el': 169,
'los': 169,
'a': 142,
'las': 133,
'se': 132,
'datos': 117,
'una': 85,
'-': 70,
'es': 66,
'estudios': 62,
'por': 61,
'como': 61,
'of': 57,
'del': 56,
'•': 54,
'para': 52,
'con': 51,
'the': 50,
'un': 50,
'data': 49,
'lo': 48,
'ciencia': 47,
'información': 47,
'and': 45,
'big': 45,
'no': 42,
'análisis': 40,
'este': 38,
'al': 35,
'más': 35,
'global': 33,
'sobre': 31,
'globales': 30,
'.': 29,
'e': 29,
'son': 27,
'o': 26,
'entre': 25,
'ha': 25,
'desde': 25,
'sin': 23,
',': 23,
'patrones': 22,
'puede': 21,
'ser': 21,
}

# Crear una instancia de WordCloud
wordcloud = WordCloud(background_color="gray", colormap='viridis').generate_from_frequencies(word_freq)

# Mostrar la nube de palabras
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show() 

### Human
Mejoremos estas observaciones y analisis

**Primeras Observaciones**

A partir de resultados obtenidos, se tienen las siguientes observaciones:

**Determinantes y Conectores**: Las palabras "de", "la", "que", "en", "el", "los", "las", "se" y "un" dominan la lista. Esto es típico en el español, ya que estas palabras son fundamentales para la gramática y aparecen con frecuencia en cualquier texto.

**Temática**: La presencia de palabras como "datos", "información", "análisis", "ciencia", "global" sugiere que el texto analizado está fuertemente relacionado con temas de ciencia de datos, análisis de información o investigación académica.

**Palabras en inglés**: La aparición de palabras en inglés como "of", "data", "big", "and" indica que el texto podría ser un documento técnico o académico que combina terminología en español e inglés.

**Verbos**: Verbos como "es", "ser", "tener" (aunque no aparece en esta muestra) suelen aparecer con frecuencia, pero en este caso específico, la muestra podría estar sesgada hacia un tipo de texto en particular.


##¿Concuerda el resultado dado por la herramienta con las palabras más utilizadas en el idioma español?

No necesariamente concuerda con las listas más comunes de palabras en español.

Aunque algunas palabras como "de", "la", "que", "el", "los" y "las" son claramente las más frecuentes en el español general, los resultados obtenidos tienen una fuerte influencia de términos técnicos o relacionados con el análisis de datos o la ciencia de datos, tematica a la que se refiere el artículo seleccionado.

#**Conclusión**
Hadoop y Spark son herramientas poderosas para el procesamiento de grandes volúmenes de datos. La elección entre ambas dependerá de las necesidades específicas de tu proyecto. Al comprender las fortalezas y debilidades de cada una, podrás tomar una decisión informada y seleccionar la herramienta más adecuada para tus objetivos.


### Assistant
El error ocurre porque al intentar acceder a `row['word']` y `row['count']` en `word_counts.collect()`, el objeto no tiene el atributo `setCallSite`. Esto generalmente está relacionado con una configuración incorrecta de Spark o con problemas al manipular los datos devueltos.

En este caso, los objetos en `collect()` no son diccionarios sino instancias de un tipo de fila (`Row`). Para resolver el problema, accede a los atributos de la fila directamente como propiedades, en lugar de usarlos como claves de un diccionario. Aquí está el código corregido:

### **Solución corregida**
```python
# Crear un diccionario con las palabras y sus conteos
word_freq = {row.word: row.count for row in word_counts.collect()}

# Generar la nube de palabras
wordcloud = WordCloud(background_color="white", colormap='viridis').generate_from_frequencies(word_freq)

# Mostrar la nube de palabras
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras")
plt.show()
```

### **Explicación del cambio**
- `row['word']` se cambió a `row.word`.
- `row['count']` se cambió a `row.count`.
  
Esto es necesario porque los objetos de tipo `Row` en PySpark no se comportan como diccionarios, sino como objetos con atributos.

### **Pasos si el error persiste**
1. Asegúrate de que la SparkSession esté correctamente inicializada:
   ```python
   spark = SparkSession.builder.appName("CountWordsPDF").getOrCreate()
   ```

2. Verifica que `word_counts` se haya generado correctamente:
   ```python
   word_counts.show()
   ```

Con esta solución, deberías poder generar el diccionario sin problemas. 😊

### Assistant
Aquí tienes una versión refinada de las observaciones, análisis y conclusiones:

---

## **Observaciones Iniciales**

A partir de los resultados obtenidos, se identifican los siguientes puntos clave:

### **1. Presencia de Determinantes y Conectores**
Las palabras más frecuentes en el análisis incluyen "de", "la", "que", "en", "el", "los", "las", "se" y "un". Esto refleja un patrón típico del idioma español, donde los determinantes, preposiciones y conectores desempeñan un papel fundamental en la construcción de oraciones. Estas palabras son funcionales y, aunque no aportan significado específico, son esenciales para la estructura gramatical.

### **2. Temática del Texto Analizado**
La presencia de términos como "datos", "información", "análisis", "ciencia", "global" sugiere que el texto está relacionado con temas de **ciencia de datos**, **análisis de información** o **investigación académica**. Esto resalta el carácter técnico o especializado del documento analizado, enfocado en áreas relevantes como la tecnología o la academia.

### **3. Inclusión de Palabras en Inglés**
La aparición de términos en inglés, como "of", "data", "big", y "and", indica que el texto tiene un enfoque técnico o académico que combina terminología en ambos idiomas. Esto es común en documentos relacionados con ciencias de datos o tecnología, dado el predominio del inglés en estas disciplinas.

### **4. Frecuencia de Verbos**
Aunque en el español general los verbos como "es", "ser" o "tener" suelen ser frecuentes, en este caso su presencia es limitada. Esto podría deberse a la naturaleza temática del texto, que posiblemente prioriza términos técnicos o conceptuales sobre la narrativa general.

---

## **¿Concuerdan los resultados con las palabras más utilizadas en el idioma español?**

No completamente. 

Aunque varias palabras frecuentes como "de", "la", "que", "el", "los" y "las" coinciden con las listas de uso general del idioma español, el análisis muestra una fuerte influencia de términos técnicos específicos de la temática tratada. Palabras como "datos", "información" y "análisis" destacan, lo que indica que el texto está dirigido a un público interesado en **ciencia de datos** o **tecnología**, en lugar de ser un documento de uso cotidiano o generalista.

---

## **Conclusión**

El análisis revela que el texto está fuertemente orientado hacia la ciencia de datos o la tecnología, con una mezcla de terminología técnica en español e inglés. Esto destaca cómo herramientas como Hadoop y Spark son fundamentales para procesar y analizar grandes volúmenes de datos. La elección de estas tecnologías debe basarse en las necesidades específicas del proyecto, considerando factores como escalabilidad, velocidad y complejidad del procesamiento requerido. Este ejercicio subraya la utilidad de estas herramientas para extraer patrones significativos y profundizar en el análisis de datos textuales.

---

Este formato es más estructurado y enfatiza los puntos clave del análisis. ¿Hay algo más que te gustaría ajustar? 😊

### Assistant
Para abordar esta actividad, sigamos los pasos que se deben realizar para cumplir con los requisitos propuestos. Aquí te ofrezco una guía detallada:

---

### **1. Selección de la herramienta**
- **Hadoop**: Es ideal para el procesamiento distribuido de datos en grandes volúmenes, pero su modelo de programación (MapReduce) puede ser más complejo y menos flexible para tareas de análisis de texto.
- **Spark**: Es más rápido que Hadoop, debido al procesamiento en memoria, y tiene soporte nativo para tareas de procesamiento de texto con bibliotecas como `pyspark.sql` o `pyspark.ml`.

**Recomendación**: Usar **Apache Spark** debido a la flexibilidad y eficiencia para procesar textos de tamaño moderado (10-20 páginas) como los artículos científicos. 

---

### **2. Preparación del entorno**
1. **Instalar Apache Spark**:
   - Si trabajas localmente, asegúrate de tener instalado Spark junto con un entorno de Python (e.g., Anaconda).
   - En un entorno distribuido, configura un cluster Spark.
   
2. **Buscar un artículo científico en español**:
   - Selecciona un artículo PDF descargable desde repositorios como *Google Scholar*, *SciELO*, o alguna base de datos académica de acceso abierto.
   - Convierte el contenido del PDF a texto. Puedes usar bibliotecas como `PyPDF2` o `pdfplumber`.

---

### **3. Proceso de conteo de palabras**
#### a) **Extracción de texto**
Extrae el texto completo del artículo, eliminando metadatos y encabezados innecesarios.

#### b) **Tokenización y limpieza**
1. Tokeniza el texto (separa palabras).
2. Normaliza las palabras:
   - Convierte el texto a minúsculas.
   - Elimina puntuaciones y caracteres especiales.
3. Opcionalmente, elimina palabras vacías (*stop words*) como "el", "la", "de", etc., para un análisis más significativo.

#### c) **Conteo con Spark**
Aquí tienes un ejemplo de cómo implementar el conteo de palabras en Spark usando Python (`PySpark`):

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col

# Crear una sesión de Spark
spark = SparkSession.builder.appName("ConteoDePalabras").getOrCreate()

# Leer el texto del artículo
with open("articulo.txt", "r", encoding="utf-8") as file:
    texto = file.read()

# Crear un DataFrame con el texto
df = spark.createDataFrame([(texto,)], ["texto"])

# Tokenización y conteo
conteo_palabras = (
    df.select(explode(split(col("texto"), r"\s+")).alias("palabra"))  # Tokenizar
    .groupBy("palabra")
    .count()  # Contar ocurrencias
    .orderBy(col("count").desc())  # Ordenar por frecuencia
)

# Mostrar resultados
conteo_palabras.show(truncate=False)
```

#### d) **Exportar resultados**
Guarda el resultado en un archivo CSV o formato similar para su análisis posterior:
```python
conteo_palabras.write.csv("resultado_conteo_palabras.csv", header=True)
```

---

### **4. Entrega y análisis del resultado**
El archivo generado tendrá el conteo de palabras con una estructura como esta:

| Palabra       | Frecuencia |
|---------------|------------|
| de            | 15         |
| la            | 20         |
| gestión       | 5          |
| datos         | 5          |
| aprendiendo   | 7          |

---

### **5. Comparación entre Hadoop y Spark (Opcional)**
Si deseas ampliar tu análisis, puedes realizar el conteo también con Hadoop (usando MapReduce o Pig) y comparar el rendimiento y facilidad de uso entre ambas herramientas.

¿Necesitas apoyo en alguna etapa en particular o un ejemplo adaptado al entorno que estás utilizando?

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - AI Memory & Context]]
- **Dominio**: AI Memory & Context Knowledge Base
