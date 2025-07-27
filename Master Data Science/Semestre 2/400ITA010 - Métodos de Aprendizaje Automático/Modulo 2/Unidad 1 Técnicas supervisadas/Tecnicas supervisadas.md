---
title: "Unidad 1: Técnicas Supervisadas"
date: 2025-03-11
tags:
  - MachineLearning
  - Supervisado
  - Clasificación
  - Regresión
  - TelcoChurn
  - "#Semestre2"
  - Master
  - Maestria
  - DataScience
  - JaverianaCali
---

# Unidad 1: Técnicas Supervisadas

## Introducción al Aprendizaje Supervisado

El aprendizaje supervisado es una rama del machine learning en la que se entrena un modelo a partir de un conjunto de datos que incluye tanto **atributos de entrada** $(X₁, X₂, ..., Xₙ)$ como **atributos de salida** $(Y₁, Y₂, ..., Yₘ)$. El objetivo es aprender una función f que permita predecir los valores de salida para nuevas entradas:

$$
  Ŷ = f(X₁, X₂, ..., Xₙ)
$$
Este enfoque es útil para resolver problemas de **clasificación** (predicción de categorías) y **regresión** (predicción de valores continuos). En el contexto del proyecto, se aplicará para predecir la probabilidad de que un cliente de telecomunicaciones presente **churn** (cancelación del servicio) o **no churn**.

---

## Técnicas Supervisadas Más Conocidas

A continuación, se presenta una visión general de algunas de las técnicas más utilizadas en aprendizaje supervisado:

### 1. K-Vecinos Más Cercanos (KNN)
- **Concepto:**  
  No construye un modelo explícito; clasifica un nuevo ejemplo buscando los K ejemplos más similares (vecinos) en el conjunto de entrenamiento y asignando la etiqueta mediante la moda (para clasificación) o la media (para regresión).
- **Parámetro Clave:**  
  El valor de K (usualmente un entero impar y pequeño) se determina experimentalmente.
- **Medidas de Similitud:**  
  Distancia euclidiana, Manhattan, Minkowski, similitud del coseno, etc.

---

### 2. Árbol de Decisión
- **Concepto:**  
  Construye un árbol en el que cada nodo interno representa una pregunta sobre un atributo y cada hoja una predicción.  
- **Proceso:**  
  Se selecciona el orden de las preguntas (usando métricas como ganancia de información o índice GINI) para maximizar la diferenciación de las clases.
- **Ejemplo:**  
  Un nodo puede preguntar "¿El estado civil es soltero?" con ramas correspondientes a las posibles respuestas.

---

### 3. Bosque Aleatorio (Random Forest)
- **Concepto:**  
  Es un método de ensamble que entrena múltiples árboles de decisión sobre subconjuntos aleatorios del conjunto de datos y de atributos.  
- **Ventajas:**  
  Mejora la robustez y reduce el sobreajuste, proporcionando además un ranking de importancia de las variables.
- **Parámetros:**  
  Número de árboles, número de atributos a considerar en cada árbol, etc.

---

### 4. Máquina de Vectores de Soporte (SVM)
- **Concepto:**  
  Busca trazar una frontera de decisión que maximice el margen entre dos clases.  
- **Aspectos Clave:**  
  Solo se utilizan los datos cercanos a la frontera (vectores de soporte) para definirla.  
- **Optimización:**  
  Se resuelve un problema de optimización cuadrática; el kernel (por ejemplo, el radial) permite tratar problemas no lineales.
- **Parámetros:**  
  C (regularización) y gamma, que deben optimizarse mediante grid search o validación cruzada.

Ver más
[[CLASE 6 Máquinas de vectores de soporte  (SVM) (marzo 10 2023)|Clase 6 SVM Pregrado]]


---

### 5. Perceptrones Multicapa (MLP)
- **Concepto:**  
  Inspirados en la estructura de las neuronas, los MLP se componen de capas de unidades (neuronas) conectadas entre sí mediante pesos.  
- **Proceso de Aprendizaje:**  
  Utiliza la técnica del gradiente descendente y el algoritmo de backpropagation para ajustar los pesos y minimizar el error.
- **Aplicación:**  
  Son capaces de aprender relaciones no lineales y complejas entre los atributos.

---

### 6. Redes Profundas
- **Concepto:**  
  Evolución de los perceptrones multicapa con arquitecturas más complejas, múltiples capas y diversidad en las funciones de activación.
- **Modelos Destacados:**  
  Redes convolucionales (para procesamiento de imágenes) y redes recurrentes LSTM (para secuencias de datos).
- **Aspectos Importantes:**  
  La inicialización de la red y el ajuste de hiperparámetros son críticos para el éxito del entrenamiento.

---
# Momento de formulación de las hipótesis
## 1. Máquinas de vectores de soporte (SVM)

Para más info de las diapositivas: [[Ing Electronica/Semestre 9 2023-1/IA/Corte 2/CLASE 6 Máquinas de vectores de soporte  (SVM) (marzo 10 2023)|SVMs Pregrado]]

<iframe width="400" height="200" src="https://www.youtube.com/embed/e-83gUpdQtQ" title="M2U1 - Máquinas de vectores de soportes" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Esta nota se centra en el **algoritmo SVM** explicado en el video de Gloria Álvarez. Se integra la transcripción del video junto con explicaciones complementarias para facilitar su comprensión y aplicación práctica en problemas de clasificación.

---
### 1. Introducción

- **Contexto:**  
  En problemas de clasificación binaria, se busca separar las muestras (por ejemplo, etiquetas +1 y -1) mediante un hiperplano que maximice el margen de separación entre las clases.
  
- **Aplicación en el Curso:**  
  Las SVM se estudian dentro del módulo de técnicas supervisadas, ya que permiten construir modelos robustos para predecir la pertenencia de una muestra a una clase, sin asumir una distribución específica de los datos.

---
### 3. Fundamentos de SVM

#### 3.1 SVM de Margen Duro

- **Concepto Básico:**  
  Se construye un hiperplano de separación que divide perfectamente las muestras linealmente separables. La idea es encontrar el hiperplano que maximice el margen, es decir, la distancia mínima desde el hiperplano a los puntos más cercanos de cada clase.

- **Margen y Vectores de Soporte:**  
  El margen se define como la suma de las distancias desde el hiperplano a los vectores de soporte (los puntos más cercanos de cada clase). La restricción para cada muestra es:
  $$
  y_n (w^T x_n + w_0) \geq 1 \quad \text{para todo } n,
  $$
  
  lo que garantiza que cada muestra esté correctamente clasificada.

- **Problema de Optimización:**  
  Se resuelve un problema de optimización cuadrática (usualmente mediante multiplicadores de Lagrange) para maximizar el margen. Solo las muestras con $a_n > 0$ (vectores de soporte) contribuyen a la función predictiva.

#### 3.2 SVM de Margen Suave

- **Motivación:**  
  En datos reales, es común que exista superposición entre las clases, por lo que no es posible una separación perfecta.

- **Variables de Holgura ($\xi$):**  
  Permiten que algunas muestras violen la restricción del margen. Se interpretan de la siguiente manera:
  - $\xi = 0$: Muestra correctamente clasificada y fuera del margen.
  - $0 < \xi \leq 1$: Muestra correctamente clasificada, pero dentro del margen.
  - $\xi > 1$: Muestra clasificada incorrectamente.
  
- **Reformulación del Problema:**  
  La restricción se ajusta a:
  $$
  y_n (w^T x_n + w_0) \geq 1 - \xi_n,
  $$
  
  y se añade una penalización en la función objetivo:
  $$
  \text{Minimizar } \frac{1}{2} \|w\|^2 + C \sum_{n=1}^{N} \xi_n,
  $$
  donde $C$ es un hiperparámetro que controla la tolerancia a las violaciones del margen.

#### 3.3 SVM para Datos No Lineales: Uso de Funciones Kernel


- **Transformación No Lineal:**  
  Cuando los datos no son linealmente separables en el espacio original, se utiliza una transformación no lineal $\phi(x)$ que mapea los datos a un espacio de mayor dimensión donde es más probable que sean separables.

- **Función Kernel:**  
  Permite calcular el producto interno en el espacio transformado sin conocer explícitamente la transformación:
  
  $$
  K(x_n, x_m) = \phi(x_n)^T \phi(x_m).
  $$
  
  Ejemplos de funciones kernel:
  - **Kernel Polinomial**
  - **Kernel Gaussiano (RBF):** $K(x_n, x_m) = \exp\left(-\frac{\|x_n - x_m\|^2}{2\sigma^2}\right)$
  - **Kernel Sigmoide**

- **Función de Predicción con Kernel:**  
  La función predictiva se reescribe como:
  
  $$
  f(x^*) = \sum_{n=1}^{N} a_n y_n K(x_n, x^*) + w_0,
  $$
  
  donde solo las muestras con $a_n > 0$ (vectores de soporte) influyen en la predicción.

---

### 4. Proceso de Entrenamiento y Predicción

1. **Selección del Kernel y Ajuste de Parámetros:**  
   Elegir la función kernel adecuada (por ejemplo, polinomial o gaussiano) y ajustar sus hiperparámetros, junto con el parámetro $C$.
   
2. **Resolución del Problema de Optimización:**  
   Formular y resolver el problema dual mediante multiplicadores de Lagrange para identificar los vectores de soporte.
   
3. **Identificación de Vectores de Soporte:**  
   Determinar las muestras con $a_n > 0$, que serán utilizadas en la función de predicción.
   
4. **Predicción:**  
   Clasificar nuevas muestras utilizando la función predictiva basada en el kernel seleccionado.

---
### 5. Ventajas y Desventajas

#### 5.1 Ventajas
- **Generalización y Robustez:**  
  Las SVM ofrecen una buena generalización, especialmente en espacios de alta dimensionalidad y con conjuntos de datos relativamente pequeños.
  
- **Solución Única:**  
  La formulación matemática mediante optimización garantiza una solución óptima.
  
- **Flexibilidad con Kernels:**  
  Permiten abordar problemas no lineales sin requerir suposiciones específicas sobre la distribución de los datos.

#### 5.2 Desventajas

- **Costo Computacional:**  
  El entrenamiento puede ser intensivo, especialmente con grandes volúmenes de datos.
  
- **Sensibilidad a Hiperparámetros:**  
  La elección correcta de $C$ y los parámetros del kernel es crítica para el buen desempeño del modelo.
  
- **Complejidad en el Ajuste:**  
  La calibración de hiperparámetros puede requerir un extenso proceso de validación y experimentación.

---
### 6. Conclusiones

- Las SVM se basan en un fundamento teórico sólido que garantiza una solución óptima mediante la maximización del margen.
- La incorporación de márgenes suaves y funciones kernel amplía su aplicabilidad a problemas tanto lineales como no lineales.
- Es crucial ajustar de manera adecuada los hiperparámetros ($C$ y los parámetros del kernel) para lograr un modelo de clasificación robusto.
- A pesar de sus ventajas, el costo computacional y la complejidad en el ajuste pueden representar desafíos en la práctica.

---
## 2. Perceptrones Multicapa (MLP)

Esta nota se centra en la técnica de los **perceptrones multicapa**, explicada en el video de Gloria Álvarez. Se integra la transcripción del video junto con explicaciones complementarias para facilitar su comprensión y aplicación en problemas de clasificación, mostrando la evolución desde modelos simples hasta redes más complejas.

Para más info de las diapositivas: [[Ing Electronica/Semestre 9 2023-1/IA/Corte 2/CLASE 6 Máquinas de vectores de soporte  (SVM) (marzo 10 2023)|SVMs Pregrado]]

<iframe width="400" height="200" src="https://www.youtube.com/embed/HiDQOuMcsbc" title="M2U1 - Perceptrón multicapa Parte 1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### 2. Introducción

- **Contexto:**  
  Los perceptrones multicapa (MLP) son una extensión de los perceptrones simples y fueron desarrollados para abordar problemas que no son linealmente separables, como el problema XOR.  
- **Aplicación:**  
  Se utilizan para tareas de clasificación compleja en las que se requiere una mayor capacidad de representación, gracias a la incorporación de capas ocultas y funciones de activación no lineales.

---

### 3. Historia y Concepto

- **Origen:**  
  Los primeros estudios sobre perceptrones se remontan al siglo XIX (Ramón y Cajal) y se formalizaron en 1943.  
- **Evolución:**  
  - **Perceptrón Simple:** Adecuado para problemas linealmente separables.  
  - **Perceptrones Multicapa (MLP):** Introducen una o más capas ocultas para superar las limitaciones de los modelos simples y resolver problemas no lineales.
- **Importancia:**  
  El desarrollo de técnicas de aprendizaje como el *back propagation* permitió entrenar MLP de manera efectiva, sentando las bases para el aprendizaje profundo.

---

### 4. Arquitectura de los MLP

- **Estructura General:**  
  - **Capa de Entrada:** Recibe el vector de características de entrada ($x_1, x_2, \dots, x_n$).  
  - **Capas Ocultas:** Una o más capas que transforman la información mediante operaciones lineales seguidas de funciones de activación.  
  - **Capa de Salida:** Produce la predicción final (por ejemplo, clasificación en categorías).
- **Conectividad:**  
  Cada neurona en una capa está conectada a todas las neuronas de la siguiente capa mediante pesos ($w_{ij}$) y tiene asociado un sesgo ($b$).
- **Cómputo en una Neurona:**  
  La entrada neta se calcula como:
  $$
  net = \sum_{i=1}^{n} w_i x_i + b,
  $$
  y la salida se obtiene aplicando una función de activación:
  $$
  y = f(net).
  $$

---

### 5. Algoritmo de Back Propagation

- **Objetivo:**  
  Ajustar los pesos y sesgos de la red para minimizar el error entre la salida predicha y la salida real.
- **Proceso General:**  
  1. **Propagación hacia adelante:** Se calcula la salida de cada capa.  
  2. **Cálculo del Error:** Se determina el error (por ejemplo, usando el error cuadrático medio).  
  3. **Propagación hacia atrás:** Se utiliza el gradiente descendente para ajustar los pesos.
- **Actualización de Pesos:**  
  El ajuste se realiza según:
  $$
  w_{ij} \leftarrow w_{ij} - \eta \frac{\partial E}{\partial w_{ij}},
  $$
  donde $\eta$ es la tasa de aprendizaje.

---

### 6. Funciones de Activación

- **Tradicionales:**  
  - **Sigmoidal:**  
    $$
    \sigma(x) = \frac{1}{1 + e^{-x}}
    $$
  - **Tangente Hiperbólica:**  
    $$
    \tanh(x)
    $$
- **Modernas:**  
  - **ReLU (Rectified Linear Unit):**  
    $$
    \text{ReLU}(x) = \max(0, x)
    $$
  - **SoftPlus:**  
    $$
    \text{SoftPlus}(x) = \ln(1 + e^x)
    $$
  Estas funciones permiten introducir no linealidades y mejorar la capacidad de la red para modelar relaciones complejas.

---

### 7. Conclusiones y Observaciones

- **Capacidad de Resolución:**  
  Los MLP pueden resolver problemas no linealmente separables gracias a la incorporación de capas ocultas y funciones de activación no lineales.
- **Evolución Histórica:**  
  Desde los perceptrones simples hasta las redes profundas, la evolución de estos modelos ha sido crucial para el desarrollo del aprendizaje profundo.
- **Importancia del Método Back Propagation:**  
  Es fundamental para el entrenamiento de MLP, permitiendo ajustar los pesos de manera eficiente.
- **Aplicaciones Actuales:**  
  Los MLP se utilizan en una amplia variedad de campos, desde reconocimiento de voz hasta clasificación de imágenes, demostrando su versatilidad y robustez.

---
## 3.  Perceptrón Multicapa Parte 2: Back Propagation

Esta nota se centra en la técnica de los **perceptrones multicapa**, explicada en el video de Gloria Álvarez, en el que se aborda la evolución de los perceptrones simples hacia redes más complejas capaces de resolver problemas no linealmente separables.  


<iframe width="400" height="200" src="https://www.youtube.com/embed/HiDQOuMcsbc" title="Video Perceptrones Multicapa" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

### 2. Introducción

- **Contexto:**  
  Los perceptrones multicapa (MLP) son una extensión de los perceptrones simples, diseñados para resolver problemas que no son linealmente separables, como el problema XOR.  
- **Aplicación:**  
  Se utilizan para tareas de clasificación compleja en las que se requiere una mayor capacidad de representación, gracias a la incorporación de capas ocultas y funciones de activación no lineales.

---

### 3. Historia y Concepto

- **Origen:**  
  Los primeros estudios sobre perceptrones se remontan al siglo XIX (Ramón y Cajal) y se formalizaron en 1943 con la idea de que las neuronas tienen una activación binaria basada en un umbral.
- **Evolución:**  
  - **Perceptrón Simple:** Adecuado para problemas linealmente separables.  
  - **Perceptrones Multicapa (MLP):** Introducen una o más capas ocultas para superar las limitaciones de los modelos simples y resolver problemas no lineales.
- **Importancia:**  
  El desarrollo de técnicas de aprendizaje como el *back propagation* permitió entrenar MLP de manera efectiva, sentando las bases para el aprendizaje profundo.

---

### 4. Arquitectura de los MLP

- **Estructura General:**  
  - **Capa de Entrada:** Recibe el vector de características de entrada ($x_1, x_2, \dots, x_n$).  
  - **Capas Ocultas:** Una o más capas que transforman la información mediante operaciones lineales seguidas de funciones de activación.  
  - **Capa de Salida:** Produce la predicción final, que puede ser una o varias salidas según la tarea.
- **Conectividad:**  
  Cada neurona en una capa se conecta a todas las neuronas de la siguiente capa mediante pesos ($w_{ij}$) y tiene asociado un sesgo ($b$).
- **Cómputo en una Neurona:**  
  La entrada neta se calcula como:
  $$
  net = \sum_{i=1}^{n} w_i x_i + b,
  $$
  y la salida se obtiene aplicando una función de activación:
  $$
  y = f(net).
  $$

---

### 5. Algoritmo de Back Propagation

- **Objetivo:**  
  Ajustar los pesos y sesgos de la red para minimizar el error entre la salida predicha y la salida real.
- **Proceso General:**  
  1. **Propagación hacia adelante:** Se calcula la salida de cada capa.  
  2. **Cálculo del Error:** Se determina el error (por ejemplo, usando el error cuadrático medio).  
  3. **Propagación hacia atrás:** Se utiliza el gradiente descendente para ajustar los pesos.
- **Actualización de Pesos:**  
  El ajuste se realiza según:
  $$
  w_{ij} \leftarrow w_{ij} - \eta \frac{\partial E}{\partial w_{ij}},
  $$
  donde $\eta$ es la tasa de aprendizaje.

---

### 6. Funciones de Activación

- **Funciones Tradicionales:**  
  - **Sigmoidal:**  
    $$
    \sigma(x) = \frac{1}{1 + e^{-x}}
    $$
  - **Tangente Hiperbólica:**  
    $$
    \tanh(x)
    $$
- **Funciones Modernas:**  
  - **ReLU (Rectified Linear Unit):**  
    $$
    \text{ReLU}(x) = \max(0, x)
    $$
  - **SoftPlus:**  
    $$
    \text{SoftPlus}(x) = \ln(1 + e^x)
    $$
  
Estas funciones introducen no linealidades y mejoran la capacidad de la red para modelar relaciones complejas.

---

### 7. Conclusiones y Observaciones

- **Capacidad de Resolución:**  
  Los MLP pueden resolver problemas no linealmente separables gracias a la incorporación de capas ocultas y funciones de activación no lineales.
- **Evolución Histórica:**  
  La transición del perceptrón simple a las redes profundas ha aumentado el poder expresivo y es la base del aprendizaje profundo actual.
- **Importancia del Método Back Propagation:**  
  Es fundamental para el entrenamiento de MLP, permitiendo ajustar los pesos de manera eficiente.
- **Aplicaciones Actuales:**  
  Los MLP se utilizan en una amplia variedad de campos, desde el reconocimiento de voz hasta la clasificación de imágenes, demostrando su versatilidad y robustez.




## Continuar

|         ⏭️ Seguir a          |
| :--------------------------: |
| [[0.Tecnicas no supervisadas]] |


