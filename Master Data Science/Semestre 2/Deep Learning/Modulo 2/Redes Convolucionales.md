---
title: "Redes Convolucionales"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---


![[Pasted image 20250601205004.png]]

# Perceptron Multicapa

- Algoritmo de Aprendizaje Automático
- No es de Deep Learning
- Cumple una tarea de aprendizaje de máquina como:
	- Clasificación
	- Regresión
- En el ejemplo:
	- La entrada es una Imagen (Radiografía)
	- Se le hace un proceso de extracción de características relevantes
	- Dichas características se pasan a una Red:
		- Fully-Connected
		- Densa
		- Perceptrón Multicapa
	- Se le enseña a detectar una radiografía **patológica (con Neumonía) o normal**
- **No están diseñados para extraer características,** pues **ya reciben los datos procesados**

# Los Algoritmos de Deep Learning

- **Extraen características**
- Uno le enseña a estos algoritmos a extraer las mejores características posibles
- Se conecta al final un algoritmo de clasificación **(Red Densa)**
- Tienen la capacidad de procesar los datos y extraer características de las entradas

![[Pasted image 20250603181557.png]]

#### **Nota**
- Si es posible ensamblar un algoritmo de Deep Learning con un Clasificador cualquiera, un SVM, Random Forest, etc...
- Es decir, que en vez de que haya una Red Neuronal, haya un Clasificador cualquiera


### 1. Extracción de características con redes neuronales

Las redes neuronales profundas, especialmente las convolucionales (CNN), son excelentes para extraer representaciones complejas de los datos. 
Estas representaciones pueden ser utilizadas como entradas para clasificadores tradicionales como SVM o Random Forest, que luego realizan la tarea de clasificación.

### 2. Reducción de la complejidad computacional

Entrenar redes neuronales completas puede ser costoso en términos computacionales. 
Al **utilizar las redes neuronales únicamente para la extracción de características** y **delegar la clasificación a modelos más simples**, se puede **reducir significativamente el tiempo y los recursos necesarios** para el entrenamiento y la inferencia.

### 3. Mejora del rendimiento en conjuntos de datos pequeños

Los modelos de _deep learning_ suelen requerir grandes cantidades de datos para generalizar bien. 
En escenarios con conjuntos de datos pequeños, **combinar redes neuronales con clasificadores tradicionales puede mejorar la precisión y evitar el sobreajuste.**

## ¿Cómo funciona el Deep Learning?

![[Pasted image 20250603182954.png]]

![[Pasted image 20250603191244.png]]

- Funciona por capas
	- Estas **ya no son capas de Neuronas**, sino que son **capas de Filtros**
	- **Los filtros hacen las convoluciones**
	- En cada capa convolucional se aplican distintas capas de filtros
- Uno puede aplicar más capaz si es necesario.
	- Estas capas permiten una "profundidad" que permite ir más allá

- En el ejemplo, tenemos **13 capas convolucionales y 5 capas de pooling**

Recordar: [[CLASE 9 Redes Neuronales Convolucionales (CNN) - (marzo 31 2023)]]

- Las capas convolucionales del inicio permiten extraer:
	- Características sencillas como líneas, bolitas, etc...
- Las capas más profundas permiten extraer
	- Características más complejas como ojos, labios, narices
	- Y las más adentro, extraer rostros completos y detallados

### Calcular el número de salidas

Para una convolución bidimensional, con entrada de altura $H$, ancho $W$, *padding* $P$, *stride* $S$, tamaño de kernel $K$ y $F$ filtros:

$$
H_{\mathrm{out}}=\left\lfloor\frac{H+2P-K}{S}\right\rfloor+1,
\qquad
W_{\mathrm{out}}=\left\lfloor\frac{W+2P-K}{S}\right\rfloor+1,
\qquad
C_{\mathrm{out}}=F.
$$

El tensor de activaciones tiene dimensión $H_{\mathrm{out}}\times W_{\mathrm{out}}\times F$; los filtros determinan los canales de salida, no una multiplicación directa del número de entradas.


## Referencias verificadas

- [[Master Data Science/Bibliografía Curada y Actualización 2026|Bibliografía curada]]: *Deep Learning* para fundamentos de convolución y representación jerárquica.
- [Capas convolucionales — Keras 3](https://keras.io/api/layers/convolution_layers/): consultar la especificación de cada capa antes de asumir el comportamiento de padding, stride, dilatación o formato de datos.

## Videos de apoyo

### Padding, strides, max pooling y stacking en las REDES CONVOLUCIONALES

<iframe width="700" height="500" src="https://www.youtube.com/embed/QLy8v6LL_4A" title="Padding, strides, max pooling y stacking en las REDES CONVOLUCIONALES" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### La CONVOLUCIÓN en las REDES CONVOLUCIONALES

<iframe width="700" height="500" src="https://www.youtube.com/embed/ySbmdeqR0-4" title="La CONVOLUCIÓN en las REDES CONVOLUCIONALES" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### ¿Qué son las REDES CONVOLUCIONALES?
<iframe width="700" height="500" src="https://www.youtube.com/embed/HyZFfBU0ADg" title="¿Qué son las REDES CONVOLUCIONALES?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


<iframe width="700" height="500" src="https://www.youtube.com/embed/4sWhhQwHqug" title="Redes Neuronales Convolucionales - Clasificación avanzada de imágenes con IA / ML (CNN)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Crear una Red Convolucional en Python

![[Pasted image 20250603193002.png]]



---
# Arquitecturas Convolucionales


![[Pasted image 20250601214903.png]]



![[Pasted image 20250601214922.png]]

- Probada en el Challenge Image Net
- Problema de Mil Clases
- 



![[Pasted image 20250601214933.png]]


![[Pasted image 20250601214947.png]]



![[Pasted image 20250601215002.png]]




![[Pasted image 20250601215013.png]]


![[Pasted image 20250601215025.png]]

- Lo de los colores, es la parte de Deep Learning
- Lo del final, es la parte de Machine Learning


![[Pasted image 20250601215032.png]]




![[Pasted image 20250601215041.png]]


![[Pasted image 20250601215050.png]]

# SegMent: Algoritmo de Meta

- Muy útil para segmentar
- También la UNet sirve para segmentar imágenes
- Se usa mucho en entornos medicos, industriales, videos, imagenes
