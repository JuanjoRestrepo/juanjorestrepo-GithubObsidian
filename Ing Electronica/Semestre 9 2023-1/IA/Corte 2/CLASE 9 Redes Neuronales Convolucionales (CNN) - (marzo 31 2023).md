---
banner: https://editor.analyticsvidhya.com/uploads/999181_BIpRgx5FsEMhr1k2EqBKFg.gif
tags:
  - "#Semestre9"
  - "#IA"
  - RedesNeuronales
  - NeuralNetworks
  - "#Convolucionales"
  - "#Convolutional"
  - "#CNN"
fecha: 2023-03-31
---
# Motivación Redes Neuronales Convolucionales

- Hasta ahora hemos visto el tipo de red neuronal más básico principalmente para ***datos estructurados***
- En ciertas condiciones, las redes más básicas, pueden ser aplicadas a datos no estructurados, como imágenes, videos y texto.

Como lo que hicimos en la práctica de clasificación de los números o la ropa, con la base de datos MNIST.

![[Motivacion Redes Convolucionales.png]]

Si convertirmos la imágen anterior, usando la técnica del aplastamiento/flatenning, puede convertirse en un arreglo **unidimensional** con 784 unidades



Redes Neuronales Fully connected: neuronas densas, las de la clase 8 [[CLASE 8 SOBRE AJUSTE DE REDES NEURONALES (marzo 24 2023)]]

Pero esto presenta un problema, el cual es que solo funciona para datos pequeños, de dimensiones pequeñas. Por ejemplo, en la figura se muestra una imagen a color que se representa a partir de un arreglo tridimensional de tamaño **355 x 500 x 3 (largo, ancho, RGB)**

![[Ejemplo Imagen Gato.png]]

- Al convertir la imagen anterior en un **arreglo unidimensional**, la capa de entrada de la red neuronal debe contar con **532500 unidades.** 
- Lo anterior es problemático porque incluso para una red poco profunda, con **una capa oculta con 512 unidades y una capa de salida con una unidad**, **necesitaríamos más de 272 millones de parámetros.**


## ¿Cómo solucionamos este problema?

Usando las redes convolucionales o CNN

- En una CNN, las entradas pasan a través de capas compuestas por un conjunto de filtros que aplican operaciones de convolución.  
- Los filtros son utilizados para la extraer características de los datos de entrada

![[Extraccion de Caracteristicas-Bordes.png]]

- La salida de las capas convolucionales pasan a através de capas de tipo ***Pooling***, las cuales realizan operaciones de ***sub-muestreo***
- **La mayoría de las redes convolucionales se construyen a partir de a conexión sucesiva de capas convolucionales y pooling**.
- Finalmente, las salidas de las etapas convolucionales alimentan capas fully-connected con el fin de llevar a cabo la tarea de aprendizaje requerida, por ejemplo, clasificación o regresión.
- Las redes convolucionales se han aplicado de **forma satisfactoria en tareas visión por computador**. Sin embargo, también existen aplicaciones en otras áreas como el reconocimiento de voz y el procesamiento de lenguaje natural.

# Operación de convolución

Es uno de los conceptos más importantes en las CNN. Un ejemplo de aplicación, es la detección de bordes en imágenes.

![[Deteccion de Bordes Gato.png]]

- La detección de bordes es el resultado de realizar la operación de convolución de la imagen con un filtro.
- Dependiendo de la configuración del filtro, se pueden destacar bordes verticales, horizontales o en diferentes ángulos.

### **En la práctica se hace de la siguiente manera:**

El proceso de extraer los bordes de una imagen se basa en la operación de convolución.

![[Operacion de Convolucion.png]]

En la figura mostramos un ejemplo de detección de bordes verticales, en el cual a una imagen de tamaño 5 x 5 se le aplica un fitro de 3 x 3.

El primer resultado de la convolución corresponde a multiplicar punto a punto cada uno de los valores del filtro con cada uno de los valores correspondientes de la imagen y luego se suman entre sí. 

El primer resultado obtiene la siguiente operación:
**(0 x 1) + (1 x 0) + (1 x -1) + (0 x 1) + (0 x 0) + (1 x -1) + (0 x 1) + (0 x 0) + (0 x -1) = -2**

![[Resultado Ultimo Elemento Convolucion.png]]
***El resultado del último elemento, es -1*** 

Para el caso de RGB, en donde son 3 canales, todos los filtros tienen que estar ubicados en la misma posición y hago la suma de los resultados.

## Diferentes filtros para la convolución

En el ejemplo de extracción de bordes presentado  
previamente, usamos los filtros mostrados en la parte  
superior de la imagen.  

En la siguiente imagen, en la esquina superior izquierda, el filtro para **bordes verticales**, mientras que en la esquina superior derecha se muestra el filtro para extraer **bordes horizontales**.

![[Filtros Convolucion.png]]

Existen diversas variaciones de estos filtros, por ejemplo, el ***filtro de Sobel*** y ***filtro de Scharr***. Cada uno ofrece diferentes propiedades que no son necesariamente útiles para todas las tareas de aprendizaje. 

- Estos filtros no se definen por el usuario, sino que se aprenden por entrenamiento de la Red. El algoritmo se entrena a partir de ***Gradiente Descendente*** 

## **Filtros Adaptativos**

![[Filtros Adaptativos.png]]

En el aprendizaje profundo, la idea es considerar los valores del filtro como parámetros. De esta manera, se puede usar el algoritmo de **Gradiente Descendente** para estimarlos.

- Los filtros diseñados son adaptativos en el sentido que sus parámetros son entrenados con el fin de obtener la mejor representación de los datos para la tarea que estemos resolviendo.
- Estos filtros pueden extraer información de bajo nivel como lineas, esquinas, bordes y de alto nivel como rostros, formas, entre otras.

Sin embargo, hay un problema el cual es que la convolución ocasiona una redducón del tamaño de la imagen, esto se conoce como ***pérdida de información en la salida***

#### **Y esto no es lo ideal. Una solución es usar las técnicas de:**

## Relleno (Padding)

![[Relleno-Padding 1.png]]

Por ejemplo, en la figura se tiene una imagen de tamaño *5 × 5*, es decir cinco filas, cinco columnas. A esta imagen  se le aplica un filtro de tamaño *3 × 3*, lo cual produce una  imagen de tamaño *3 × 3.*  

- Matemáticamente tenemos el siguiente análisis. Suponer que tenemos una imagen de entrada con Nf filas y Nc  columnas, a la cual le aplicamos un filtro de tamaño $f$ x $f$ .  La salida será una imagen de tamaño:
![[Filas y Columnas Resultantes Relleno-Padding.png]]


### **NOTA:**
- El encogimiento de las imágenes es problemático en redes profundas donde se realizan convoluciones sucesivas. Luego de algunas convoluciones el tamaño de la imagen se reduce considerablemente.
- Una alternativa es rellenar la imagen de tal forma que el resultado de la convoluci ́on sea del mismo tamaño que la imagen original.

Por ejemplo, si añadimos dos filas y dos columnas a  
nuestra imagen original, obtenemos una imagen $7 × 7$. Al aplicar la operación de convolución, la imagen de salida conserva el tamaño de la imagen original ($5 × 5$)

![[Relleno-Padding 2.png]]

Comúnmente, se usan dos opciones relacionadas con la cantidad de relleno.
- La opción ***Padding = Valid*** no aplica ningún tipo de relleno. Esto quiere decir que el resultado de la convolución tendrá pérdida de información.
- Con la opción ***Padding = Same*** se aplica el relleno necesario para que la imagen de salida tenga el mismo tamaño que la original.
- Se puede notar entonces que el factor de relleno es un hiper-parámetro asociado con las redes convolucionales.

## **Paso (stride)**

En la operación de convolución, el filtro recorre a la  imagen de izquierda a derecha y de arriba hacia abajo,  con un **paso** (**stride**) de uno. Sin embargo **el valor del paso puede definirse como un hiper-parámetro.**

Suponer que tenemos una imagen de entrada con **Nf filas  y Nc columnas**, a la cual le aplicamos un filtro de tamaño $f$ × $f$ ; además, hemos fijado un paso ***s***. La salida será una imagen de tamaño:

![[Paso Stride Num filas y Columnas.png]]

**NOTA:**
**Tener en cuenta que un paso muy alto puede reducir considerablemente el tamaño del resultado de la convolución**


# Capas Convolucionales

Como hemos visto, la convolución se representa a partir de combinaciones lineales. Esto implica que solo se puede modelar datos con estructuras lineales.

Sin embargo, **es posible utilizar funciones de activación no-lineales**. De esta forma, al resultado se le suma el término independiente **$w_0$.** Finalmente, este resultado pasa a través de la función de activación.

![[Uso de Funciones de Activacion No-Lineales a Capas Convolucionales.png]]

Las funciones de activación usadas en las capas convolucionales son las mismas que ya hemos estudiado previamente: [[CLASE 7 Redes Neuronales (marzo 17 2023)]]

----------------------------------
Hasta este punto hemos entendido el funcionamiento de la convolución. Como ejemplo hemos asumido que existe un único filtro.

Sin embargo, las redes convolucionales se componen de varios filtros, cada filtro con su propio conjunto de parámetros. Por ejemplo, en la figura se muestra una  
capa convolucional con *7* filtros de tamaño *3 × 3*

![[Capa Convolucional 3x3 7 Filtros.png]]

De esta forma, a una imagen de entrada se le aplicarán, de forma independiente, tantas operaciones de convolución como filtros en la capa.


Considerar una imagen de entrada con tamaño *5 × 5* y que tenemos una capa  
convolucional con *7* filtros de tamaño *3 × 3*. Además, supongamos que el paso es  
***stride = 1*** y que el relleno es ***padding=‘valid’***

![[Ejemplo Capas Conv con Imagen 5x5.png]]

De esta forma, como se muestra en la figura, la salida de la capa convolucional  tendrá un tamaño de *3 × 3 × 7.*

### Capas Pooling

Su labor no es extraer caracterisitcas, sino solo hacer compresión de las imágenes. Contrario a las convolucionales, que extraen características pero no compresión

- Esta operación tiene como objetivo reducir el tamaño de las representaciones con el fin de aumentar la velocidad de los cálculos y para robustecer las características extraídas por las capas convolucionales.

Se reconocen dos tipos de pooling: 
- **Max Pooling (M ́aximo)**
- **Average Pooling (Promedio).** 

Veamos un ejemplo para entender su funcionamiento.

#### **EJEMPLO MAX POOLING**

Se tiene una imagen de tamaño *4 × 4* y se le aplica una operación pooling con un **paso de 2** y donde el tamaño
del filtro es de *2 × 2*.

Esto corresponde a dividir la imagen en cuatro partes de tamaño *2 × 2,* como se muestra la figura.

![[Max Pooling 1.png]]

De cada región, se extrae el ***máximo, si usamos Max Pooling*** o ***el promedio si empelamos el Average Pooling*.**

• Las capas Pooling no tienen ningún parámetro que se deba estimar a partir del gradiente descendente. Sin embargo, si tiene hiper-parámetros que deben ser ajustados: El tamaño del filtro y del paso

![[Max Pooling 2.png]]

***NOTA:
ENTRE MAS PROFUNDA ES LA RED, LAS CAPAS: MAYOR CANTIDAD DE FILTROS APARECEN Y EL TAMAÑO DE LA IMAGEN DISMINUYE***


