---
banner: https://live.staticflickr.com/65535/48057305423_0653b5e58f_b.jpg
tags:
  - "#Semestre9"
  - IA
  - "#Sobreajuste"
  - "#RedesNeuronales"
  - "#NeuralNetworks"
fecha: 2023-03-24
---
## 1. Sobre-ajuste y Sub-ajuste


Primero debemos definir qué es un ajuste adecuado.

![[Ajuste_General.png]]

El caso mostrado en la figura representa una  solución adecuada para un problema de regresión. De esto se puede ver que la regresión (***El modelo***) no pasa por todos los puntos; sin embargo, **tiene la capacidad de capturar la estructura de los datos** 

***El ajuste adecuado se caracteriza por obtener métricas de desempeño adecuadas para el conjunto de entrenamiento y prueba.*** 

### **Sobre-ajuste:** 
- Hace referencia cuando el entrenamiento es muy bueno pero falla en el test.  
- Es el fenómeno donde el modelo intenta capturar toda la información de los datos de entrenamiento
- Los datos pueden presentar ruido, **en sobre-ajuste, el modelo identifica patrones ruidosos que pueden afectar su rendimiento en los conjuntos de validación.**  
- El sobre-ajuste se caracteriza por un **rendimiento alto en la etapa de entrenamiento** (Costo bajo, Accuracy alto) y **un rendimiento bajo en el conjunto de validación** (Costo alto, Accuracy  bajo).  
![[Sobreajuste.png]]

  
Existen estrategias que disminuyen el impacto del sobre-ajuste. Entre estas se reconocen: **La regularización, el dropout y la parada temprana (Early stopping).**  

**Otra alternativa es reducir la complejidad de la red**. Por ejemplo, quitando capas ocultas o la cantidad de neuronas por capa. Los modelos más simples son menos propensos a sufrir de sobre-ajuste.  

***Los parámetros $w_n$ tienden a ser muy grandes***

##### **¿Por qué tener una Red con 100 neuronas o muchas, puede generar sobre ajuste?**
- Porque mientras más capas tengamos, estamos aumentando el número de parámetros.

**DATA AUGMENTATION:**
- Es una forma de reducir el sobre-ajuste.  Puedo ajustar las imagenes, rotandolas, haciendole zoom, cortandola.
- Esto es útil porque puede pasar de 100 a 10000 datos. 

**TRANSFERENCIA DE APRENDIZAJE:**

### **Sub-ajuste:**

- El sub-ajuste es el **fenómeno en el cual el modelo no es lo suficientemente robusto para capturar la estructura de los datos.**  
- En general, el sub-ajuste se identifica cuando **el modelo no alcanza el rendimiento esperado.**  
- El rendimiento esperado es un aspecto subjetivo que debe definirse de acuerdo con la aplicación y/o con base en el consejo de un experto.  
- El sub-ajuste **puede minimizarse al utilizar modelos más complejos**. En el caso de las redes neuronales, una solución al sub-ajuste corresponde a agregar m ́as capas o más neuronas por capa.  

![[Subajuste.png]]

## 2. Gradientes que explotan

Como hemos dicho previamente, los m ́etodos de optimización basado en gradiente son los ḿas usados para calcular los parámetros de las redes neuronales.  
- También recordemos que la derivada de un parámetro en las capas menos profundas depende de la multiplicación  de las derivadas de todas las capas más profundas, hasta llegar a la capa de salida.  
- De esta forma, en redes muy profundas, **el cálculo de las derivadas depende de la multiplicación de muchos factores**. **Si estos factores son valores mayores que uno, el valor de los gradientes puede crecer indefinidamente**.  

![[Gradientes_que_Explotan.png]]
***$\eta$ -> ∞*** 
*$\eta$*: Learning rate. Si es pequeño, necesitamos muchas iteraciones para que converja

### ¿Cómo reconocer el fenómeno de los gradientes que explotan?  

- El modelo es inestable. La función de pérdida del modelo varía abruptamente entre cada iteración del entrenamiento.  
- La función de pérdida del modelo toma valores de NaN, ∞ o −∞.

### ¿Cómo minimizar el efecto de los gradientes que explotan?  
- Replantear el modelo. Al usar un modelo con menos capas, se reduce la posibilidad de que los gradientes se vuelvan inestables.  
- Inicializar los parámetros de forma adecuada. Porque si yo inicializo todo con los parámetros $w_1$ me va a dar el mismo cálculo de $w_2$ y así con los $w_n$ lo que significa que la red no va a aprender nada

## 3. Gradientes que se desvanecen

Al igual que con los gradientes que explotan, en redes con muchas capas, el cálculo de las derivadas depende de la multiplicación de varios factores.  Que tienden se conocen como gradientes que tienden a cero

![[Gradientes_Que_Desvanecen.png]]
***$\eta$ -> 0*** 

- Si estos **factores toman valores cercanos o menores que uno** (Los pesos **$w_n$** en cualquier instante), la multiplicación sucesiva de estos tienen como resultado gradientes que tienden a cero.  
- Si el valor de los gradientes tiende a cero, los parámetros permanecerán casi iguales durante las iteraciones del entrenamiento.  
• El uso de **funciones de activación Sigmoidal o Tangente hiperbólica en capas ocultas** también se asocia con el problema de los gradientes que se desvanecen. Esto ocasiona el fenómeno de gradiente que se desvanece por lo siguiente:


#### **¿Cómo reconocer el fenómeno de los gradientes que se desvanecen?**  

- El modelo es incapaz de capturar información de los datos. Esto se percibe en que la función de pérdida permanece sin mayores cambios al pasar las iteraciones.  
- No varía la función de costo o varía muy poco alrededor de un punto. 

#### **¿Cómo minimizar el efecto de los gradientes que se desvanecen?**  

- Replantear el modelo. Al usar un modelo con menos capas, se reduce la posibilidad de que los gradientes se vuelvan inestables.  
- Inicializar los parámetros de forma adecuada.  
- **Evitar el uso de las funciones Sigmoidal y tangente hiperbólica como función de activación en capas ocultas.** 
*La función Sigmoidal es adecuada para las capas de salida en tareas de clasificación binaria.*  


## 3. Regularización

Una de las características que se ha identificado en el fenómeno del sobre-ajuste es que los pesos de la red tienen gran magnitud.  

- La primera forma de solucionar el sobre-ajuste es **modificar la función de costo,  añadiendo un término de regularización que garantice que los parámetros del modelo tienen una magnitud controlada**. De esta forma se disminuye la posibilidad de que el modelo se sobre ajuste.

De esta forma, la función de costo regularizada se escribe como ***Función de Costo***
![[Ecuacion_Regularizacion.png]]


**Función Costo:** se encarga de que el modelo se adapte a los datos de entrenamiento

**Factor de regularización:** se encarga de controlar la magnitud de los parámetros de la red.

**Hiperparámetro $\lambda$:** que controla el nivel de regularización del modelo.  

- **Si $\lambda$ = 0:** no se tiene en cuenta la regularización y la optimización solo minimizar ́a la función de costo. Esto lleva a que el modelo sea propenso al sobre-ajuste
- **Si $\lambda$ >> 1:** el término de regularización tiene mayor peso que la función de costo. 


- En Keras, el valor por defecto es λ = 0,01.

Yo puedo definir a cuales capas les aplico regularizaición. Usualmente, el profe le coloca a todas regularización con el fin de encontrar los mejores parámetros

*Si algunas capas o neuronas se apaga, la complejidad disminuye, quitándole flexibilidad y se hace menos propenso al sobre-ajuste*

### 4. Dropout (Otra forma de reducir el sobreajuste)

El dropout es otro tipo de técnica que reduce el riesgo de sobre-ajuste. Esta técnica consiste en fijar una probabilidad ***p*** para cada unidad de una capa específica, excepto la capa de salida.  

- En cada iteración del entrenamiento cada unidad desaparece, momentáneamente, con una probabilidad ***p.***  
- Esto quiere decir que, en cada iteraci ́on del entrenamiento, se modifica la arquitectura de la red.  

![[Dropout.png]]

¿Por qué apagar neuronas en cada iteración reduce el sobreajuste?


- El valor ***p*** es un hiper-parámetro de la red que se denomina la razón del dropout.  
- El dropout reduce el riesgo de sobre-ajuste ya que, en cada iteración, se reduce la complejidad de la red de forma aleatoria.  
- En keras, el dropout se define como una capa adicional. Así, se tiene la flexibilidad de  elegir a cu ́ales capas se le aplica este proceso.  
- En el siguiente ejemplo, se muestra una capa con 4 unidades, activación **ReLU** y con  capa de dropout con ***p = 0.5.*** Esto quiere decir que, en cada iteración, todas las unidades tienen una probabilidad del 50 % de desaparecer momentáneamente. Esto se hace por capa

El dropout va después de cada capa. Aleatoriamente durante el entrenamiento no se actualiza con el gradiente.

***model.add(Dense(4, activation=’relu’))  
model.add(Dropout(0.5))***


### 5. Parada Anticipada (Early Stopping)

Se aplica en escenarios como los mostrados en la figura, donde se tiene un buen  aprendizaje inicial, en el sentido de que la función de costo para el entrenamiento y la validaci ́on empiezan a decrecer; sin embargo, luego de ciertas iteraciones, la función costo en el conjunto de validación empieza a aumentar dando lugar a un sobre-ajuste del modelo.  
- En estos casos es conveniente modificar el algoritmo de entrenamiento con el fin de interrumpirlo en el momento justo en que la función de costo, en el conjunto de validación, llega a su mínimo.  

Es como un Ctrl+C pero en código, cuando llega al punto más mínimo. No es recomendable.


***Época:*** cuantas iteraciones requiere el algoritmo para
