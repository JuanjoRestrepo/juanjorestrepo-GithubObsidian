---
tags:
  - Semestre9
  - IA
  - "#KMeans"
fecha:
---


## Definición de la tarea de agrupamiento

En este módulo se estudian los modelo de aprendizaje no supervisado. Esto quiere decir que en nuestras bases de datos no existen etiquetas.  

De esta forma, se tiene un conjunto de datos formados únicamente por atributos de entrada $x_1$, $x_2$, . . . , $x_N$  

La idea es entonces asignar cada una de las muestras ***x** a uno de ***K*** grupos previamente definidos.  

## Fundamentos de K-Medias (K-Means)

  
Los grupos se eligen de tal forma que la distancia entre los puntos de un mismo grupo sea menor a la distancia entre puntos de grupos diferentes.  

Para esto, es conveniente definir el vector μk, el cual representa el centro del k- ́esimo grupo.  

De esta forma, se fija un conjunto de vectores ${(μk)}^K_k=1$   tal que la suma de las distancias de cada   punto a su μk más cercano sea la mínima posible.  

De esta forma, para cada muestra xn, se define un vector binario con rn, compuesto por K valores rnk, donde rnk = 1 si la instancia xn pertenece al grupo k, y rnk = 0 en  
otro caso.  

Se debe aclarar que cada muestra xn solo puede pertenecer a uno de los K grupos.  Por ejemplo, si existen K = 4 grupos y la instancia xn pertenece al grupo 3, luego el vector **$r_n$** se escribe como:

![[Pasted image 20230526081437.png|300]]

Así desde el punto de vista t ́ecnico, debemos encontrar los valores $r_(nk)$ y $μ_k$ que minimicen la distancia entre cada punto xn y su correspondiente centro $μ_k$. Lo anterior se define, 
matemáticamente, como:

![[Pasted image 20230526081630.png|300]]

### Algoritmo de K-medias

![[Pasted image 20230526081659.png|700]]

### Desventajas K-Medias

- El algoritmo de las K-medias solo tienen la capacidad de grupos con forma circular (hiper-esferas en altas dimensiones).  
- Sin embargo, es posible que los datos tengan diferentes estructuras.  

![[Pasted image 20230526081803.png]]

- Por otro lado, las estimaciones que entrega las K-medias son consideradas como clasificación dura. En este sentido un punto es asignado a un ́unico grupo.  
- Sin embargo, en algunas ocasiones se requiere obtener una estimación suave.  
- La estimación suave consiste en que el algoritmo indique la probabilidad de que un punto pertenezca a cada uno de los ***K*** grupos predefinidos.

## Mezcla Gaussiana

### Distribución Gaussiana multivariada  

La solución a las desventajas previamente comentadas es el uso de combinaciones de distribuciones Gaussianas.  

- La función Gaussiana multivariada es una función de densidad de probabilidad que permite evaluar el comportamiento probabil ́ıstico de variables aleatorias.  

- En este sentido, las decisiones que se tomen a partir de este tipo de combinaciones serán probabilísticas (suaves)


[[Clase 13 DBscan y PCA]]
