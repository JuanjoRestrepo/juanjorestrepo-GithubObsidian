---
title: "Optimizadores-Early Stopping"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---



# 1. Gradiente Descendente

![[Pasted image 20250601183220.png]]

- Método de optimización iterativo para minimizar funciones de pérdida ($L$) en modelos de machine learning.

$$
w^{(t+1)} = w^{(t)} - \alpha \nabla_w L(w)
$$
$t$: Iteración actual
$\alpha$: Tasa de aprendizaje
$\nabla_w L$: Gradiente de la función de pérdida

- Hay dos factores que controlan el tamaño del paso: **el gradiente y la tasa de aprendizaje**
- El gradiente **tiende a cero a medida que la optimización se acerca a un minimo**
- Es común encontrar que en muchas aplicaciones se usa una tasa de aprendizaje que varia con las iteraciones
- En palabras simples, **es llevar el $w$ a la dirección que me minimice la función de costo**

## Gradiente Descendente - Minimos Locales

![[Pasted image 20250601192732.png]]

- Tenemos un imagen, por lo que nuestra grafica sera de dos dimensiones
- Entre mas claro, el valor de loss es mas alto
- Entre mas oscuro, el valor de loss es mas bajo
- Nos interesa que el gradiente llegue a la zona oscura
- Sin embargo, se aprecian varios bayes, que serian
![[Pasted image 20250601193400.png]]
![[Pasted image 20250601193405.png]]
- Los mínimos como el primero, se les conoce como **mínimos locales**
- El problema, es que al haber varios, estos algoritmos **se inicializan de manera aleatoria** por lo que se **pueden iniciar en un mínimo local que puede afectarlo**

![[Pasted image 20250601193547.png]]
- Si vemos al **mínimo global**, el baye mas grande, se termina obteniendo un **loss mucho mas bajo, con un mejor ajuste**

![[Pasted image 20250601194133.png]]

Debido a lo anterior, surgen algunas alternativas

![[Pasted image 20250601194150.png]]

- Aunque se usen todos los datos de entrenamiento, no es la mejor alternativa
- Lo mejor a esto, es meterle un poquito de ruido a la ecuación del gradiente, un poquito de aleatoriedad

$$
w^{(t+1)} = w^{(t)} - \alpha \nabla_w L(w)
$$

Se se sumaria un pequeño ruido gaussiano, etc...

- La ventaja de sumar este ruido, es sacar el gradiente de si se cae en algún mínimo local
- El **gradiente estocástico NO ES CONVENIENTE USARLO** PORQUE:
	- Es muy demorado
	- Es muy oscilatorio

En conclusion
- Es mejor usar el **Batch Size por Lotesitos, por mini lotes**, 10, 20, 30 o potencias de 2. $2^n$
- 

## Gradiente Estocastico

![[Pasted image 20250601195057.png]]

- Es dificil saber donde empezar,  ademas de ser aleatorio, puede ser que empezmos en Gradiente Descendente en la Pos 1 y se vaya bien al minimo global. O que empezemos en la Pos 2 y se vaya a un minimo local


- El estocástico es mas ruidoso y demorado, tiene mas oscilaciones y se tarda mas para llegar al minimo (global)

## Gradiente Estocastico de Media Movil Exponencial Ponderada (Exponentially Weighted Moving Average)

![[Pasted image 20250601195733.png]]

- Al usar el ruido del estocastico, minimiza la probabilidad de encontrar minimos locales

![[Pasted image 20250601200026.png]]

### **Momentum**
- Busca averiguar o tener informacion de gradientes de pasos anteriores para decidir el siguiente paso
- Busca darle un empujon para que no oscile tanto, sino que vaya mas fuerte y busque la direccion donde se encuentra el minimo local
- Al hacer este empujon se cambia la ecuacion:

![[Pasted image 20250601200158.png]]

![[Pasted image 20250601200422.png]]

- El momentum reduce las oscilaciones
- Impide que se quede en mínimos locales
- Mejora los caminos del aprendizaje, es decir, mejora los caminos que recorre el gradiente


#### **RMSprop (Root Mean Square Propagation) I**

![[Pasted image 20250601200843.png]]

![[Pasted image 20250601201250.png]]

- **Ajusta la tasa de aprendizaje en cada iteración**
- Calcula un LR diferente para cada parámetro. Esto es beneficioso, ya que puede ocurrir que **cada parámetro aprenda a un ritmo/tasa diferente**



---

# 3. ADAM (Adaptive Moment Optimization)

![[Pasted image 20250601201418.png]]

![[Pasted image 20250601201927.png]]

- Es el mejor optimizador hasta el momento
- **Combina** el **RMS** y el **Momentum**
- 






---
