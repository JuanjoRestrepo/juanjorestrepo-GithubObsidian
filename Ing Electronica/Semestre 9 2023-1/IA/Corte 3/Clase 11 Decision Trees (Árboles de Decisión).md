---
tags:
  - "#Semestre9"
  - "#IA"
  - "#DecisionTrees"
  - "#ArbolesDecision"
fecha:
---


## HASTA AQUI VA APRENDIZAJE SUPERVISADO

Son algoritmos que se pueden adaptar a datos NO LINEALES

ESTO FUNCIONA ELIGIENDO CARACTERÍSTICAS, POR MEDIO DE CONDICIONALES

# Ejemplo inicial

![[Pasted image 20230428102104.png]]

Evidentemente no todas pertenecen a una única clase, especialmente si son clases de datos No Lineales

Yo tengo que **variar entre la complejidad del modelo y la cantidad de los datos**, se **sobreajusta**, pues si yo dejo que el modelo siga y siga, probablemente se sobreajusta

Hay balance entre sobreajuste y complejidad del modelo

En este ejemplo empezados analizando el largo del pétalo de una flor, pero también podemos empezar con el ancho del pétalo

# Otras alternativas

![[Pasted image 20230428102247.png]]

Pero cómo podemos definir por cuál empezar? Por qué primero el largo y no el ancho, y viceversa.

**El entrenamiento depende tanto del número de características como el número de muestras**

# Proceso de entrenamiento

Dado un conjunto de entrenamiento el proceso de entrenamiento se centra en dos  decisiones:  

### **Decisión 1:** ¿Cuál característica debemos considerar en cada uno de los nodos?  

***Maximizar la pureza de cada nodoFeature***

Hay que tener en cuenta que la pureza de los nodos es importante. 
![[Pasted image 20230428102702.png]]

De la imagen anterior, el "**Mejor**" es el de la izquierda, pues los dos nodos tienen mayor pureza, es decir, la clasificación no está mezclada, como en el nodo de la derecha que tiene elementos rojos en el nodo de los elementos azules

### **Decisión 2:** ¿Cuándo parar de realizar divisiones?  

Y el **Segundo Cuestionamiento** que surge, es saber cuándo terminar de dividir al árbol, es decir, cuándo parar de hacer los cambios, agregando más ramas, más hojas para que el modelo de clasificación sea el mejor

- Cuando el 100 % de las muestras en un nodo pertenecen a una única clase.  
- Cuando al dividir un nodo se excede la profundidad máxima  (hiperparámetro).  
- Cuando la cantidad de muestras en un nodo es menor que un umbral (hiperparámetro).  
- Cuando las mejoras en la pureza de los nodos no es mayor a un umbral (hiperparámetro).  

### **Valor de GINI**

Si el árbol es muy profundo, tiende a hacer sobreajuste empieza a hace ramificaciones

![[Pasted image 20230428104042.png]]

- VALOR MÁXIMO DE GINI: 0.5
- ESTE VALOR ES PARA DETERMINAR LA IMPUREZA,
- EL MAXIMO ES 0.5, pero ENTRE MÁS PEQUEÑO, MAS CERCANO A CERO, MEJOR

Corrigiendo $P_1 = \frac{500}{85}$,  $P_2 = \frac{35}{85}$, $I = 0.48$

NOTAS USAR EL GINI ES MAS EFICIENTE COMPUTACIONALMENTE QUE LA ENTROPIA

ES MAS FACIL CALCULAR CUADRADOS QUE LOGARITMOS

### **Entropía**

![[Pasted image 20230525160704.png]]

### **Pasos para entrenar**

Se elige la combinación de característica y umbral que maximizan la ganancia de información definida como la reducción de la impureza (Reducción de la entropía o el valor Gini).  

- Dada una característica y un umbral, la ganancia de la informaci ́on se calcula a partir de los siguientes pasos:  
	1. Calcular la impureza del nodo padre $I_f$ .  
	2. Calcular la impureza de los nodos hijos $I_{c1}$ y $I_{c2}$  
	3. Calcular el promedio ponderado de la impureza de los hijos.

![[Pasted image 20230525160948.png]]

donde $N_{c1}$ y $N_{c2}$ corresponde a la cantidad de datos en el nodo uno y dos  
respectivamente.  
• Finalmente, la ganacia de la informaci ́on se calcula como $I_f$ − $I_c$

Con base en el criterio de la ganancia de la informaci ́on elegir cuál combinación de característica y umbral debe elegirse.
![[Pasted image 20230525161025.png]]

#### EN RESUMEN

-   Se inicia con todas las muestras en el nodo padre.  
- Calcular la ganancia de la informaci ́on para todas las posibles combinaciones de caracter ́ısticas y umbrales. Elegir la combinaci ́on que maximiza la ganancia de informaci ́on.
- Dividir los datos de acuerdo con la caracter ́ıstica y umbral elegidos.  
- Repetir el proceso de división hasta que se complete alg ́un criterio de parada:  
	1. Cuando al dividir un nodo se excede la profundidad máxima (hiperparámetro).  
	2. Cuando la cantidad de muestras en un nodo es menor que un umbral (hiperparámetro).  
	3. Cuando las mejoras en la pureza de los nodos no es mayor a un umbral  (hiperparámetro).  

![[Pasted image 20230525161240.png]]

![[Pasted image 20230525161301.png]]
![[Pasted image 20230525161325.png]]


## GANANCIA DE INFORMACION MAXIMA:
- ENTRE MAYOR SEA MEJOR, RECORDANDO QUE EL MAXIMO ES 0.5 y el MIN ES 0 (CERO)
SIEMPRE ME QUEDO CON LA COMBINACION QUE MAXIMICE LA GANANCIA DE INFORMACION

# Combinación de clasificadores  

![[Pasted image 20230525161507.png]]

## Votación de clasificadores

La idea es utilizar la combinación de múltiples clasificadores (weak learners).  
- La predicción ante una nueva entrada se estima como la etiqueta más votada (votación dura).  
- Si todos los clasificadores entregan predicciones en forma de probabilidad; luego dichas probabilidades se pueden promediar. Esto se conoce como votaci ́on suave.  
- Los clasificadores (weak learners) son entrenados sobre el mismo conjunto de datos.  
- Otra alternativa es usar un mismo clasificador (=modelo, =hiperparámetros) y entrenarlo de distintas maneras usando diversas versiones del conjunto de entrenamiento.


## **Bagging vs Pasting**

Para elegir los datos de entrenamiento de cada weak learner, se usa el Bagging (boot- strap aggregating) o el Pastin

![[Pasted image 20230525162826.png]]

![[Pasted image 20230525162849.png]]

BAGGING ES EL MAS USADO

## Bagging vs Adaboost

- Existen otros tipos de combinaci ́on de clasificadores, denominados Boosting.  
- La idea principal es entrenar los modelos de forma secuencial de tal forma que el actual modelo corrige los errores de su predecesor.  
- Los modelos m ́as usados en este contexto son el AdaBoost y el Gradient Boost.  
- En el AdaBoost el nuevo modelo tiene la capacidad de enfocar su atenci ́on en las muestras que su predecesor ajustó de forma incorrecta. 
- Para clasificar una nueva muestra, se efect ́ua una votación por mayor ́ıa ponderada, donde las ponderaciones son proporcionales al rendimiento de cada clasificador en la etapa de entrenamiento.  

## ADABOOST

LOS PESOS A LOS PUNTOS QUE SE EQUIVOCAN SE DAN TOMANDO EN CUENTA AL RESULTADO DE LA CLASIFICACION

![[Pasted image 20230525163008.png]]


### consultar utilizacion en adaboost y stream boosting
https://towardsdatascience.com/the-ultimate-guide-to-adaboost-random-forests-and-xgboost-7f9327061c4f

siempre usar un numero de arboles de decision max 200/300, valores pequeños, cuando use un Bosque Aleatorio


[[Clase 12 Fundamentos K-Means]]
