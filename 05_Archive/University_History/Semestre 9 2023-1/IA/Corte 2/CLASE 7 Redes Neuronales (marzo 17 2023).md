---
banner: https://img.freepik.com/vector-premium/red-neuronal-fondo-red-neuronal_115739-65.jpg
tags:
  - "#Semestre9"
  - "#IA"
  - "#NeuralNetworks"
  - "#RedesNeuronales"
fecha: 2023-03-17
---
Extension de una regresión logística o una lineaCapa. Una reg logística con "poderes"

Tiene tres tipos de capas:
1. **Capa de Entrada**: se relaciona con los atributos de entrada del conjunto de entrenamiento.
2. **Capa Oculta**: se denomina oculta porque no conozco el valor exacto de las unidades que toman los parámetros. Corresponde a una representación de los datos de entrada Funcionan similar a un Kernel, pero estas mejoran la representación de los datos.
5. **Capa de salida**: se encarga de realizar predicciones de la red.
Se encarga de hacer lo que quiero, regresión, clasificación, etc...

![[Capas_Red_Neuronal.png]]
A pesar de decir que una Red Neuronal tiene 3 capas, en la literatura se dice que tiene 2, porque la oculta "No se tiene en cuenta"

*Las capas mas cercanas a la entrada representan mejor atributos de bajo nivel. 
Las mas cercanas a las de salida, representan mejor atributos como el reconocimiento de rostros, nariz ojos*.

## **CALCULAR SALIDA DE UNA RED NEURONAL**

Estos cálculos son muy similares a los usados en una regresión lineal o una regresión logística.

Para iniciar, vamos a omitir, por ahora, la capa de salida. Esto nos deja una red con la capa de entrada y una capa oculta de tres unidades.   

El primer paso consiste en determinar el valor de las tres unidades: $h_1$, $h_2$ y $h_3$ 

![[Capa_Entrada_y_Oculta_De_Tres_Unidades..png]]

Al igual que con la regresión lineal o la regresión logística, el c ́alculo de los valores de la capa oculta empieza con una combinación lineal de los atributos de entrada.  
• El resultado de esta combinación  lineal pasa a través de una función  ***g(·)***, que se conoce como la ***Función de activación*** 

## **Para calcular ***h1***

$$h_1 = w_1X_1 + w_2X_2 + w_3X_3 + w_4X_4 + w_0$$

Pero lo tengo que pasar a una función:

$$ h_1 = g( w_1X_1 + w_2X_2 + w_3X_3 + w_4X_4 + w_0) $$
La función ***g*** anterior, se conoce como la función de activación

## **Para calcular h2:**

$$ h_2 = g( w_1'X_1 + w_2'X_2 + w_3'X_3 + w_4'X_4 + w_0) $$

**$w_0$ : BIAS, OFFSET.** Se utiliza para garantizar que los valores de salida $h_n$ tengan valores de acuerdo a la condición que yo deseo. Es decir, $h_n > 1$ por ejemplo.

De lo anterior, se puede visualizar como un vector. Donde se hace un producto punto.
- Donde ***W*** es el vector de pesos asociados a una neurona (Verde: Gato, Naranja: Perro, Gris: Aves),
***X*** es el vector de pixeles de la imagen de entrada y ***b/**$w_0$*** es el bias.

La salida de esta multiplicación, es un vector columna ***Score*** relacionado a cada una de las clase *Gato, Perro, Ave*. Esto nos da la predicción para cada una de las imágenes de entrada.

En la primera salida del vector columna,
![[Estructura_RedNeuronal_Basica.png]]

![[Visualizacion_Ecuacion_NN.png]]
**¿Cómo podemos medir que tan buenos son nuestros resultados?**

Sabemos que nuestra Red Neuronal recine parámetros *X: datos entrada,  W: Peso, b: bias (sesgos 
u offset) NN(X, W, b)* 
![[Resultados_Predicciones_NN.png]]
De lo anterior, podemos darnos cuenta que para la clase gato, el vector columna de salida arroja valores de ***3.32*** cuando procesamos la imagen de un gato, por lo tanto, al ser el valor más alto, concluimos que los valores actuales de W y bias son los adecuados para predecir la imagen de *Clase Gato*

En cambio con la siguiente, la del perro, no predice bien que es la imagen de un perro, por lo que dichos valores de W y bias no están clasificando bien la imagen del *perro*. Pero si clasifica bien a un *ave*.

De lo anterior, concluimos que estos valores ***NO SON LOS MÁS ÓPTIMOS***, por lo tanto es importante tener una forma de **cuantificar Qué tan buenos son los pesos y biases actuales**. Para ello se usan las funciones de activación ( ***Sigmoid, ReLu, etc...*** ).

![[Generalizacion_Funciones_Acrivacion_SOFTMAX.png]]
Una forma de cuantificar esto, es mediante la función ***Softmax*** con la cual podemos normalizar los valores de salida **$h_n= WX + b$** en porcentajes probabilísticos para determinar la probabilidad que la entrada tiene de pertenecer a una clase u otra. ***Softmax*** se aplica en la última capa.

Ahora bien, podemos determinar o medir matemáticamente qué tan buenos son los parámetros que le pasamos al modelo para arrojar la probabilidad obtenida anteriormente. Para ello, usamos la ***función de pérdida/Loss Function***, la cual nos indica qué tan grande es nuestro error.


------------------------------------//----------------------------------//-----------------------------------
***NOTA***
- Hay que garantizar que el conjunto de parametros sean estrictamente diferentes. Si fuesen iguales, ***h1*** y ***h2*** serian exactamente los mismos, **dañaríamos el modelo.** 

### **Ejemplo:**
Si esto pasa, si quisieramos reconocer dos rostros, h1 y h2 tendrán pesos diferentes, uno para identificar cejas, boca, nariz... y si fuesen  iguales, reconoceriamos siempre las cejas, lo que es ineficiente para reconocer dos rostros distintos

### **La nomenclatura de una Red Neuronal es la siguiente:**

![[Nomenclatura_Red_Neuronal.png]]
### Ecuación para **h2:**

![[Ecuacion_para_h2.png]]

**De esta forma defino un vector final W:**

$$ h_2 = [ w_{1,0}[1], w_{1,1}[1], w_{1,2}[1], w_{1,3}[1], w_{1,4}[1], w_{2,0}[1], w_{2,1}[1]] $$
W = [ w1,0 [1] , w1,1 [1], w1,2 [1], w1,3 [1], w1,4 [1], w2,0 [1],  w2,1 [1], ]

![[Vector_Final_Wh.png]]

**El mismo procedimiento se emplea para las tres unidades que tiene nuestra capa oculta.**  

- La ́unica diferencia entre el c ́alculo de una unidad y otra, son los parámetros empleados al momento de calcular la combinación lineal.  
- Notemos que los parámetros usados en estos cálculos tienen un ***super ́ındice [1],*** el cual indica que son los parámetros asociados a la primera capa.  

![[Wh_n.png]]
**Este es el Bias. Se requiere para calcular los parametros ***hn***

w1,3

$w_{h,x}$:  ***h:*** numero de la capa actual (capa 1),  ***x:*** numero capa anterior

Notemos que los parámetros usados en estos calculos tienen un super ́***ındice [1]***, el cual indica que son los parámetros asociados a la primera capa:

## Calcular los parámetros de la Capa Oculta:

Para calcular los valores de la capa oculta, necesitamos tantas combinaciones lineales como unidades en la capa.

- Cada combinación lineal requiere una cantidad de parámetros igual al número de atributos en la capa de entrada, más uno adicional para el término independiente.  
- Por lo tanto, para calcular todos los valores de la capa oculta, necesitamos un total de 15 parámetros. ***4 parámetros en la capa de entrada y el bias, y 3 en la capa oculta ***

En la siguiente imagen se puede ver esta combinación lineal de una mejor forma. Donde multiplicamos las 4 entradas $X_1, X_2, X_3$ y $X_4$ obtendremos 12 parámetros (Una matriz 3x4)
![[Visualizacion_Matematica.png]]

Una vez que hemos calculado los valores de la capa oculta, procedemos a calcular la **salida** de la red neuronal. En este cálculo, **omitimos la capa de entrada**, ya que **la salida no depende de los valores de entrada**. 

![[Calculos_hn_Respecto_CapaFinal.png]]
Como se puede observar en la figura, la capa de salida depende de los parámetros con superíndice [2], lo que indica que **pertenecen a la capa 2 de la red neuronal**.

De esta forma, el procedimiento para calcular la salida es similar al seguido previamente en la capa oculta.

- **La diferencia radica en** que **la combinación en la capa de salida no depende de los atributos de entrada sino de los valores de la capa oculta**

- Es necesario que el resultado de la salida de cada neurona, sea el resultado de una **función NO LINEAL**.. Por lo cual, se le aplica una **Función de Activación** que es una Función No Lineal

Cuantos parametros necesito para calcular 

## Red Neuronal de *L* Capas

Hasta este punto, hemos utilizado una red neuronal poco profunda con solo dos capas.  
- No obstante, estos conceptos pueden ser  aplicados sin problemas a **redes neuronales más  profundas**, las cuales pueden tener una **mejor representación del problema** que queremos resolver.

### Ejemplo:

Mostramos una red neuronal con ***L = 3***, es decir, que la red cuenta con tres capas. Debemos recordar que en **el conteo de las capas no se tiene en cuenta la capa de entrada**
![[Red_Dos_Capas_Ocultas.png]]

## Funciones de Activación

- La función de activación ***g(·)*** se usa para calcular el valor de una unidad en alguna capa oculta o en la capa de salida.
- Las funciones de activación añaden una componente no-lineal a las redes neuronales.
- Dado que las Redes Neuronales siempre tienen una forma de linealidad matemáticamente, estas **siempre corresponden a un modelo lineal sin importar cuántas capas ocultas tenga**. 

Por lo que, si concatenamos la salida de una función lineal con otra función lineal, el resultado seguiría siendo otra función lineal. He aquí la importancia de la Función de Activación

- En general, l**as funciones de activación se pueden usar en cualquier capa**. Sin embargo, **hay funciones que son más apropiadas para las capas de salida** **y otras funciones cuyo funcionamiento se ajusta a las capas ocultas**

### **Ejemplos Funciones de Activación:**

**1. Función Identidad**

- Función donde la salida es igual a la entrada.
- Si se usa en todas las capas de activación de una red, el modelo se convierte en lineal.
- **Principalmente se usa en la capa de salida cuando se tienen tareas de regresión**, cuya salida es cualquier valor real.  
![[Funcion_Identidad.png]]

**2. Función Sigmoide**

- Función que genera valores entre 0 y 1.  
- En la actualidad **se usa principalmente en la capa de salida** para tareas de clasificación binaria.  
- **La función Softmax es una generalización de la función Sigomidal**,  la cual **se aplica exclusivamente en la capa de salida** para resolver problemas de **clasificación multi-clase.**  

![[Funcion_Sigmoide.png]]

**3. Función Tangente Hiperbólica**
![[Funcion_Hiperbolica.png]]

- Función que genera valores entre -1 y 1.  
- Se usa como **función de activación en capas ocultas**. Su efecto es **normalizar los valores de entrada alrededor de 0.** 
- Puede llevar a problemas de gradientes que se desvanecen. 

**4. Función ReLu (Rectified Linear Unit))**

- En la actualidad, es **una de las funciones de activación más usadas** debido a que  
ha mostrado buenos resultados en diferentes aplicaciones.
- Se **suele usar exclusivamente en las capas ocultas**.

![[Funcion_ReLu.png]]

**Otras Funciones de Activación**

Existen otras funciones de activaci ́on que usualmente son modificaciones de las funciones vistas previamente. Entre ellas se encuentran:  
- Leaky ReLU.  
- Parametric ReLU.  
- SELU (Scaled Exponential Linear Unit).  
- ELU (Exponential Linear Unit).  

## Parámetros e Hiperparámetros

- En una red neuronal, los parámetros son todos aquellos valores **$w$** que se utilizan para calcular el valor de las unidades de las capas ocultas la capa de salida. 

- Por otro lado, los hiperparámetros son aquellos valores que afectan el cálculo de los parámetros y, por lo tanto, la forma en que la red neuronal aprende a partir de los datos

### ¿Cómo se calculan los parámetros?

- El cálculo de los parámetros en una red neuronal sigue un proceso similar al de modelos más básicos como los modelos lineales.  
- Este cálculo se compone de dos conceptos clave: **la función de costo y el algoritmo de optimización.**  
- La elección de la función de costo debe ser cuidadosa y depende del problema que estemos resolviendo. Por ejemplo:
	- **Para problemas de regresión:** error cuadrático medio.  
	- **En aplicaciones de clasificación binaria:** la entropía cruzada binaria.  
	- **Para clasificación de múltiples:** la entropía cruzada categórica

En cuanto al algoritmo de optimización, **la mayoría de las aplicaciones de redes neuronales utilizan el gradiente descendente** o alguna de sus variantes

### **El método de gradiente descendente**

es un proceso iterativo utilizado para encontrar los valores óptimos de los parámetros de una red neuronal. 

Por ejemplo, si queremos determinar el parámetro $w_{3,4}[1]$ de a primera capa, podemos aplicar el  método de gradiente descendente de la siguiente manera:
![[Ecuacion_Metodo_Gradiente_Descendente.png]]

  
En este caso la derivada $\frac{\partial \zeta(w)}{\partial w_{3,4}[1]}$ se calcula usando el algoritmo de propagación hacia atrás.
![[Backpropagation_Algorithm.png]]

### Hiperparámetros

**Cantidad de capas de una red. A este hiperparámetro se le suele conocer con el  
nombre de profundidad de la red *L***

• **El número de unidades por capa no siempre puede elegirse de forma arbitraria**.  Específicamente, las neuronas en la capa de entrada y salida dependerán del problema que queremos resolver. En la capa de entrada **este número depende de los atributos** y en la capa de salida se presentan los siguientes casos:
	- Si se trata de una **regresión o de una clasificación binaria**, **la capa de salida tendrá una única unidad.**
	- Por el contrario, si enfrentamos un problema de **clasificación multi-clase, nuestra capa de salida tendrá tantas** unidades como clases

**Para las capas ocultas no hay consenso en cómo definir este valor.**  


Existen otros hiperparámetros que afectan el cálculo de los par ́ametros de una red neuronal. Estos incluyen:

- El factor de aprendizaje **η**: este hiperparámetro asociado con el algoritmo de optimización.  
- Funciones de activación. Si bien la activación **ReLU** es la más común en las capas  
ocultas, este es un hiperparámetro susceptible a cambios. Incluso, cada capa puede  
tener su propia función de activación.  
- Otros hiperparámetros incluyen, **el algoritmo de optimización**, el **tamaño del lote**, el **número de ́epocas**, los procedimientos de regularizaci ́on entre otros. Dichos conceptos serán abordados en la próxima unidad

El **procedimiento más usado** para determinar los valores de los hiperparámetros es  
**empírico**. Este consiste en experimentar con diferentes combinaciones de hiperparámetros con el fin de encontrar el que genere los mejores resultados.

  
**Para la búsqueda de hiperparámetros, las bases de datos se dividen en tres grupos:**
- **El conjunto de entrenamiento,** que se usa para estimar los par ́ametros del modelo
- **El conjunto de desarrollo o validación**, sobre el cual se evalúan las diferentes  combinaciones de hiperparámetros.
- **El conjunto de prueba** se emplea para evaluar el modelo definitivo.  

**Unicamente las mediciones de rendimiento hechas sobre el conjunto de prueba sirven  
para concluir sobre el funcionamiento del modelo**


  
## **Los porcentajes de datos en cada conjunto** 

- Se determinan con base en la cantidad de datos. 
- Para **bases de datos con pocas instancias** se acostumbra a usar la división  **60/20/20**
	- **60 % de los datos se usa en el entrenamiento,  20 % forman el conjunto de desarrollo y el 20 % forman el conjunto de prueba.**  

- Si las **bases de datos tienen una cantidad considerable de muestras**, los porcentajes cambian. **No hay una regla exacta para estas divisiones; sin embargo, se suelen usar divisiones como 90/10/10.**  

- Finalmente, **se reconocen al menos tres estrategias para la búsqueda de  hiperparámetros**: 
	- **La búsqueda por grilla, la búsqueda aleatoria y la optimización Bayesiana.** 
	- De las tres, **la búsqueda aleatoria es la más usada** en diferentes aplicaciones de aprendizaje profundo.  


**SIGUIENTE:** 
[[CLASE 8 SOBRE AJUSTE DE REDES NEURONALES (marzo 24 2023)]]

**ANTERIOR:**
[[CLASE 6 Máquinas de vectores de soporte  (SVM) (marzo 10 2023)]]
