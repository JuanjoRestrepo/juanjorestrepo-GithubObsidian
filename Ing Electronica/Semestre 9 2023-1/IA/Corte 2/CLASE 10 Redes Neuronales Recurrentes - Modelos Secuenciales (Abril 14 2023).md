---
tags:
  - Semestre9
  - IA
  - RedesNeuronales
  - NeuralNetworks
  - "#Recurrentes"
  - "#RNN"
fecha: 2023-04-14
---





---
banner: https://pythongeeks.org/wp-content/uploads/2022/02/ml-rnn.webp
---
## Motivación

El origen de las Redes Neuronales Recurrentes (RNN)  se da a partir de la necesidad de ***modelar datos secuenciales como texto, audio o series de tiempo.***

Para este tipo de datos, las redes neuronales **fully-connected no son las más adecuadas**, debido a que el resultado del modelado no será el más adecuado.

***NOTA***
- Son **mas comunes en este tipo de datos**, pero no quiere decir que no se puedan utilizar Convolucionales (CNN).
- Por más que las CNN estén relacionadas con procesamiento de imágenes o RNN para texto, es posible utilizarlas al contrario o combinarlas.

Por ejemplo, para nosotros es claro que las dos frases mostradas en la figura, María buscó a Juan y Juan buscó a María, son diferentes debido a que la posici ́on de las palabras  
cambia totalmente el sentido de la oración.

![[Motivacion Redes Recurrentes.png]]

Sin embargo, debido a que las redes fully-connected asumen independencia, la estructura de las frases se pierde y las dos estructuras pueden considerarse similares.  

#### Solución a este problema

Una posible solución son las RNNs, las cuales están diseñadas específicamente para manejar datos secuenciales.  
![[Pasted image 20230420153532.png]]


- La principal característica de las RNN, es que cada unidad oculta está conectada con la unidad anterior. Esto permite mantener la informaci ́on de las unidades pasadas con el fin de conservar la estructura de las secuencias.  
- Las ***RNNs*** y sus modificaciones se han aplicado de forma satisfactoria en tareas de Procesamiento de lenguaje natural y el reconocimiento de voz. Sin embargo, también se pueden aplicar a otro tipo de datos como las imágenes o videos.  


## **Aplicaciones de las RNN útiles**

**1. Reconocimiento del habla**
Donde la entrada es un segmento de audio y la salida es una secuencia de palabras

![[Reconocimiento del habla.png]]

**2. Traducción automática**
Donde la entrada es una secuencia de texto en un idioma
dado y la salida es otra secuencia que representa la traducción de la secuencia de entrada

![[Traduccion Automatica.png]]


**3. Generación de música**
Usualmente este tipo de aplicación no tiene entradas; por su
parte, la salida corresponde a una secuencia que representa una composición musical.

![[Generacion Musica.png]]

**4. Clasificación de sentimientos**
Para este caso particular la entrada es una secuencia de texto que representa una opinión y la salida es una categoría que indica la connotación de la opinión, es decir, si fue un comentario positivo o negativo.

![[Clasificacion Sentimientos.png]]
*Calificación por estrellas de una película
Aprendizaje por categoría* 

-------------------------------------------------------------------------------
Hemos analizado que **las RNN se presentan como una alternativa a las redes fully-connected** **para el modelado de datos estructurados**

Cada entrada $x_j$ de las RNN, puede ser la representación numérica de una palabra, los valores correspondientes a un fragmento de una señal de voz o un fragmento de una serie de tiempo.

• La principal característica de las RNN es que la salida del elemento *t*, $\hat{y_t}$  depende de todas las entradas anteriores $x_{t-1}$, $x_{t-2}$, . . . . Así se preserva la estructura secuencial de los datos.

## **Entradas Red Recurrente**

  
En las redes recurrentes las entradas pueden ser datos de tipo numérico o texto. En los casos de texto, debemos buscar una representación numérica. 

Una alternativa es usar un diccionario y la codificación One-hot
https://medium.com/analytics-vidhya/one-hot-encoding-of-text-data-in-natural-language-processing-

En una codificación en One Hot, cada palabra (incluso los símbolos) que forman parte de los datos de texto dados se escriben en forma de vectores, que constituyen solo 1 y 0.  Entonces, un vector activo es un vector cuyos elementos son solo **1 y 0**

Cada palabra se escribe o codifica como un vector activo, y cada vector activo es **único**. Esto permite que la palabra se identifique únicamente por su vector One Hot y viceversa, es decir, dos palabras n**o tendrán la misma representación de vector One Hot**

![[Vector One Hot Encoding Redes Recurrentes.png]]

En la imagen de la izquierda, las palabras **'The' y 'the'** tienen una codificación diferente, lo que implica que **son diferentes.**

Por lo tanto, estamos **representando** cada palabra y símbolo en los datos de texto como **un único vector One Ho**t que **contiene datos numéricos (1 y 0)** como elementos constituyentes


- Una palabra se representa como un **vector** , 
- La lista de palabras en la oración se puede representar como una **matriz de vectores** o una **matriz**
- Si tenemos una lista de oraciones cuyas palabras están codificadas en One Hot, dará como resultado una matriz cuyos elementos son matrices.

Entonces terminamos con un **tensor tridimensional** que puede alimentar a la red neuronal.

#### Ejemplo en Python
```python
import numpy as np

samples = {'Jupiter has 79 known moons .', 'Neptune has 14 confirmed moons !'} # Sample set for our example`

# Create an empty dictionary`

token_index = {}

#Create a counter for counting the number of key-value pairs in the token_length

counter = 0`

# Select the elements of the samples which are the two sentences

for sample in samples:

for considered_word in sample.split():

if considered_word not in token_index:

`# If the considered word is not present in the dictionary token_index, add it to the token_index`

`# The index of the word in the dictionary begins from 1`

token_index.update({considered_word : counter + 1})

# updating the value of counter`
```

**EXPLICACION CODIGO**
- En la primera línea, tenemos nuestro conjunto de muestras que consta de dos oraciones. 
- A continuación, creamos un **diccionario** de Python vacío para almacenar nuestras **palabras (claves) y sus** **índices (valores)** correspondientes 
- Seguido de un contador establecido en 0 para contar el número de pares clave-valor en el diccionario. El primer bucle for itera sobre las oraciones mientras que el siguiente bucle for en la siguiente línea itera sobre cada palabra en la oración seleccionada y divide cada palabra devolviendo una **lista de cadenas.** 
- Luego, si el valor de la variable _current_word_ no está en el diccionario _token_index_ , lo agregamos al diccionario _token_index_ y le asignamos un índice igual al valor de _contador_variable e incrementarlo en uno para comenzar nuestro índice desde 1 en lugar de 0 y también incrementar el valor del _contador_ en 1.

`print(token_index){'Jupiter': 1, 'has': 2, '79': 3, 'known': 4, 'moons': 5, '.': 6, 'Neptune': 7, '14': 8, 'confirmed': 9, '!': 10}`



------------------------------------------------------

En este sentido, en las redes recurrentes **cada dato de entrada es representado a partir de vector de tamaño P**


## **Valores Capa Oculta**

Tomaremos como referencia la unidad oculta $h_2$, que está relacionada con la entrada $x_2$.

![[Representacion RNN.png]]

• El valor de la capa oculta $h_2$, depende de la entrada  $x_2$ y del valor de la capa oculta pasada $h_1$

La operación para la capa oculta y la capa de salida puede describirse a partir de una red fully-connected, como puede verse en la figura.

![[Operacion Capa Oculta a partir de Red Fully-Connected.png]]

- Una red recurrente está compuesta por tres conjuntos de parámetros: 
$W^{h,x}$, $W^{h,h}$, $W^{y,x}$
- Los parámetros $W^{h,x}$ multiplican a las entradas y los parámetros $W^{h,h}$ multiplican a la capa oculta anterior con el fin de calcular la capa oculta actual.
- La función ***g(·)*** corresponde a las funciones activación vistas en las unidades anteriores. Al igual que en las redes fully-connected, en las capas ocultas se suele usar las función ReLU.

### Para la capa de salida, 

- Los valores de la capa oculta se multiplican por los parámetros $W(y,h)$.  
- La función $g(·)$ debe elegirse de forma cuidadosa, de acuerdo con la salida deseada. Por ejemplo, en casos de clasificación binaria, se usa la función **Sigmoide**.  
- Una particularidad de las RNN es que los conjuntos de parámetros $W(h,x)$, $W(h,h$)$ y $W(y,h)$, son los mismos para todas las entradas $x_t$. 
- Además, dichos parámetros pueden  estimarse a partir del algoritmo de gradiente descendente.

### Hasta ahora hemos asumido una red recurrente básica, en la cual el n ́umero de entradas es igual al n ́umero de salidas.  

Sin embargo, **esta arquitectura puede cambiar de acuerdo con la aplicación.**  
Por ejemplo,

### **En la clasificación de sentimientos **

la entrada es una secuencia de texto, mientras que la salida es una categoría

![[Pasted image 20230420163156.png]]

Es claro que **el número de salidas dependerá del tamaño de la secuencia, mientras que solo se usaría una salida.**  

Este tipo de problemas se puede atacar con un  arquitectura similar a la mostrada en la figura, la cual se denomina **“Many to one”. ** 


### Visualización la Arquitectura de una RNN
![[Pasted image 20230420180601.png]]

### **Otro ejemplo es la generación de música.** 

- Aquí, **la entrada contiene un único elemento puede ser vacío o un número que indique el género musical.**
- **La salida será una secuencia que representa la composición musical** generada.  
- Este problema puede solucionarse con la estructura mostrada en la figura, la cual se denomina **“One to many”.**  
- La característica particular de esta estructura es que **la salida actual servirá como entrada de la próxima unidad**

![[Pasted image 20230420154844.png]]

## **Variaciones Redes Recurrentes**

- Otro tipo de aplicación es e**l reconocimiento de entidades en texto.** **Por ejemplo, reconocer nombres de personajes.** 
- Así, **cada salida puede corresponder a una variable binaria que indica si cada letra representa un nombre.** 
- **Se nota que para este problema, el número de entradas debe ser igual al número de salidas.** 
- Este tipo de arquitecturas se denomina ***“Many to many”.* ** 

![[Pasted image 20230420163344.png]]

### Segunda Versión Many to Many

- En esta versión la secuencia de entrada y salida pueden tener un longitud diferente.
- Este tipo de estructura es **útil para tareas como la  
traducción automática**, en donde **la longitud de una frase en un idioma inicial y su traducción no tienen, necesariamente, la misma longitud. ** 


![[Pasted image 20230420163641.png]]


## Unidades recurrentes con compuerta–(GRU)

Recordemos que unidad tiene como entradas, la  
capa oculta en el instante anterior $h_{t−1}$ y la  entrada actual $x_t$. 

Como salidas, se identifica la  salida en el instante actual $\hat{y_t}$ y el valor de la capa  oculta actual $h_t$.  

![[Pasted image 20230420163941.png]]

**Una de las problemáicas de las redes recurrentes es que en secuencias muy extensas se necesitan muchas unidades**, lo cual repercute en que **se puede perder la relación entre dos elementos muy alejados.**  

Además, este tipo de secuencia extensas hace  que la red sea **propensa a la existencia de gradientes que se desvanecen.** 

#### Por ejemplo, analicemos la siguiente frase:  

*"El **perro** que ya había comido ..., **estaba** lleno"*

Es claro que la conjugación del verbo estar dependerá de si tenemos uno o muchos perros.

**El problema es que hay muchas palabras entre el sujeto “perro” y la acción “estar”. ** 

Esta distancia puede repercutir en que la relación entre el sujeto y el verbo se pierda y así se interprete la frase de forma errónea.  

## Alternativa: Usar compuertas GRU

![[Pasted image 20230420164524.png]]

La idea principal de las GRU es utilizar una nueva componente $Γ_t$ que toma valores entre 0 y 1.  

Esta compuerta permite decidir qué tanta información pasada (representada en $h_{t−1}$) o  que tanta informaci ́on de la entrada actual se  usa para calcular la salida de la unidad $y_t$  

### Matemática detrás de la GRU

Las entradas de esta unidad son: $c_t−1$ = $h_{t−1}$, la cual contiene información de las unidades pasadas, y el elemento de la secuencia $x_t$.   

Una componente importante es $C_t$, la cual es un candidato para convertirse en el valor de la capa oculta $h_t$. Este valor depende de los datos actuales xt y la información pasada $c_{t−1}$. Para esta componente suele usar una función de activación $tanh$.

Una segunda componente esencial es Γt que toma valores entre 0 y 1. Γt permite decidir la cantidad de informaci ́on pasada y presente que se usa en la unidad. Su   cálculo depende de los datos actuales xt y la informaci ́on pasada ct−1; además, usa una activaci ́on Sigmoide para obtener valores entre 0 y 1

Finalmente, el valor de la capa oculta ht se decide a partir de la siguiente ecuación,  

$$
c_t = Γ_t ̃c_t + (1 − Γ_t)c_{t−1}
$$


De esta forma, si Γt es cercano a cero, se conserva la información pasada representada por $c_{t−1}$. Por el contrario, si este valor es cercano a 1, se actualiza la información con la entrada $x_t$, la cual está representada en $c_t$.  

Esto es **útil en las frases similares** al ejemplo debido a que **podemos olvidar las palabras que no son útiles y quedarnos con las que ayuden a entender la información de las oraciones**

#### Tomando como ejemplo la frase:

*"El **perro** que ya había comido ..., **estaba** lleno"*

La red GRU podr ́ıa entrenarse de tal forma que reconozca las palabras que son claves  
para resolver la tarea y descarte las menos importantes

![[Pasted image 20230420172924.png]]

Así,  s**e eliminan las distancias entre las partes más importantes de la frase y reduce la  
posibilidad de que los gradientes tiendan a cero.**  

Existe otro tipo de unidades denominadas las ***Long Short-Term Memory (LSTM).*** 
Podemos consultar el funcionamiento de este tipo de redes en el siguiente art ́ıculo y  
tutorial:

### LSTM
https://www.analyticsvidhya.com/blog/2022/01/the-complete-lstm-tutorial-with-implementation/

Los LSTM no son más que una pila de redes neuronales compuestas de capas lineales compuestas de pesos y sesgos, como cualquier otra red neuronal estándar. Los pesos se actualizan constantemente mediante retropropagación.

Ahora, antes de profundizar, permítanme presentarles algunos términos específicos cruciales de LSTM:

**1.  Celda:** cada unidad de la red LSTM se conoce como “celda”. Cada celda se compone de: 

**3 entradas:**

-   _x(t) —_  token en la marca de tiempo t
-   _h(t_ −1) — estado oculto anterior
-   _c(t-1) —_  estado anterior de la celda,

**y 2 salidas:**

-   _h(t) —_  estado oculto actualizado, usado para predecir la salida
-   _c(t)_  — estado actual de la celda

**2. Gates:** LSTM utiliza una teoría especial para controlar el proceso de memorización. Conocido popularmente como mecanismo de puerta en LSTM, lo que hacen las puertas en LSTM es almacenar los componentes de la memoria en formato analógico y convertirlo en una puntuación probabilística al hacer una multiplicación por puntos usando la función de activación sigmoidea, que lo almacena en el rango de $0 –1$. 
- Las puertas en LSTM regulan el flujo de información dentro y fuera de las celdas LSTM.

Tipos de puertas:

- **Puerta de entrada:** esta puerta permite la entrada de información opcional necesaria del estado actual de la celda. Decide qué información es relevante para la entrada actual y la permite entrar.
- **Puerta de salida:** esta puerta actualiza y finaliza el siguiente estado oculto. Dado que el estado oculto contiene información crítica sobre entradas de celda anteriores, decide por última vez qué información debe llevar para proporcionar la salida.
- **Forget Gate**: Bastante inteligente para eliminar información innecesaria, la puerta de olvido multiplica 0 a los tokens que no son importantes o relevantes y permite que se olvide para siempre.

#### ¿Por qué LSTM es superior a RNN?

![[Pasted image 20230420212633.png]]

se ha notado notablemente que los RNN no tienen buen rendimiento mientras se manejen dependencias a largo plazo. 

##### Problema: Gradiente de Fuga:

- RNN usa una funciónn de activaciónn de Tangente Hiperbólica $tanh$ y su rango de activación e encuentra entre $[-1,1]$, con su derivada en el rango de $[0,1]$.
- Ahora sabemos que las RNN son una red neuronal secuencial profunda. Por lo tanto, debido a su profundidad, las multiplicaciones de matrices aumentan continuamente en la red a medida que la secuencia de entrada sigue aumentando. 
- Por lo tanto, mientras usamos la regla de la cadena de diferenciación durante el cálculo de la retropropagación, la red continúa multiplicando los números con números pequeños.**¿ENTONCES QUÉ PASA CUANDO SE SIGUE MULTIPLICANDO UN NÚMERO CON VALORES NEGATIVOS CONSIGO MISMO?**
	**Se vuelve exponencialmente más pequeño, reduciendo el gradiente final a casi 0, por lo que LOS PESOS YA NO SE ACTUALIZAN MÁS Y LA RED NO APRENDE, EL ENTRENAMIENTO SE DETIENE**
	ESTO LO VUELVE EN UN APRENDIZAJE INEFICIENTE

##### Problema: Gradiente Explosivo:

Concepto similar al problema del gradiente que se desvanece, pero justo al contrario del proceso, es decir, si el valor del gradiente es mayor que 1 y multiplicar un número grande por sí mismo lo hace exponencialmente más grande, tiende a INFINITO, lo que lleva a la explosión del gradiente.

##### **Problema de dependencia a largo plazo en RNN**

#### Conclusión

- Los Long Shot Term Memories (LSTM) son muy eficientes para resolver casos de uso que involucran datos textuales extensos. 
- Puede variar desde síntesis de voz, reconocimiento de voz hasta traducción automática y resumen de texto. Le sugiero que resuelva estos casos de uso con LSTM antes de saltar a arquitecturas más complejas como los modelos de atención.


----------------------------------------------------

## Redes Bidireccionales

#### NOTA:

RNN, GRU y LSTM son **MODELOS SECUENCIALES QUE SOLO SIGUEN UN ÚNICO SENTIDO** 
especialmente donde **LA SALIDA DEPEND ÚNICAMENTE DE LA INFORMACIÓN ACUTAL Y PASADA**
Pero esto puede ser problmático cuando necesitamos contexto para entender el sentido de la secuencia.

### Ejemplo

Si consideramos que tenemos que identificar si la tercera palabra de la frase obedece al nombre de una persona:

- Ella dijo: “Julia es un lenguaje de programación”.  
- Ella dijo: “Julia es mi profesora de idiomas”.  

Si usamos una red unidireccional, tendríamos que predecir la salida con base en la  secuencia: “Ella dijo: Julia”. **La información es insuficiente para deducir** si Julia, es el nombre de una persona o un lenguaje de programación

#### Solución:

- Usar **Redes Bidireccionales**, donde **la predicción de la tercera secuencia dependerá de información pasada, presente y futura.**
- Esto **permite que cada salida del modelo pueda tener acceso a la totalidad de la secuencia**. De esta forma, **es posible conocer el contexto** y entender, por ejemplo, si Julia obedece al nombre de una persona o no.  

#### Componentes Red Bidireccional

1. Corresponde a una **red hacia adelante**. Las capas ocultas de esta primera parte h→ dependen de la información actual y pasada
2. Una **red hacia atrás**. Las capas ocultas de esta segunda parte h← dependen de la información actual y futura.



![[Pasted image 20230420180754.png]]


ANTERIOR:
[[CLASE 9 Redes Neuronales Convolucionales (CNN) - (marzo 31 2023)]]

SIGUIENTE:
[[Clase 11 Decision Trees (Árboles de Decisión)]]