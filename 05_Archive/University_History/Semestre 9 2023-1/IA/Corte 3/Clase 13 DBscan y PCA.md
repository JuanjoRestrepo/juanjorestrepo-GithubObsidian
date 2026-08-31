---
tags:
  - Semestre9
  - IA
  - "#DBSCAN"
  - "#PCA"
fecha:
---


Todos los `core instance` pertenecen al mismo `cluster`

Un ***epsilon*** mas pequeño repercute en más datos atípicos/outlayers
Toda muestra que no tenga alrededor otra muestra, es atípica
Si yo tengo un ***epsilon*** **muy pequeño**, y un ***min_sample*** **muy grande**, pueden haber **muchos datos atípicos**


Si yo tengo dos ***core_instance***, que no comparten informacion con otro cluster, entonces son diferentes


## **Maldición de la Dimensión**

Cuando tengo más columnas (Parámetros) que filas (Muestras), esto afecta el aprendizaje del modelo, generando sobreajuste

La solución es quitar o combinar columnas entre las más adecuadas, hacer dropout, replantear el modelo

Otra solución es Seleccionar y Extraer Características

## **Selección y Extracción Características**

![[Seleccion y Extraccion Caracteristicas.png]]

## **PCA**

![[Pasted image 20230519104332.png]]

Las direcciones que se eligen en la nube de puntos deben ser perpendiculares

En PCA1 hay mayor dispersión

PCA descubre cuáles son la direcciones en la que hay mayor variabilidad en los datos.
Las otras que PCA genere, 

### **¿Para qué tengo que definir esas direcciones?**

Porque yo tengo que garantizar que la pérdida de información sea mínima.
Por ejemplo, si yo elimino PCA1 y dejo PCA2, los datos estarían sobre el eje de PCA2 probablemente distribuidos así:

![[Pasted image 20230519104936.png]]

Si  yo elimino PCA2 y dejo PCA1, los datos estarían sobre el eje de PCA1 probablemente distribuidos así:
![[Pasted image 20230519105127.png]]

En PCA1 hay mayor varianza, qué tan dispersos están los datos.
Entre más varianza capture PCA, menor pérdida de información habrá. Pero esto genera que PCA sea más sensible ante la presencia de Outlayers

![[Pasted image 20230519105253.png|700]]


Siempre me quedo con el menor valor de los valores propios, porque estos indican la varianza y una varianza más pequeña, significa mayor cantidad de datos, es decir, que habrá menor pérdida de información.

![[Pasted image 20230519105532.png|700]]

**Izquierda: Valores Propios
Derecha: Vectores propios**


[[Clase 12 Fundamentos K-Means]]