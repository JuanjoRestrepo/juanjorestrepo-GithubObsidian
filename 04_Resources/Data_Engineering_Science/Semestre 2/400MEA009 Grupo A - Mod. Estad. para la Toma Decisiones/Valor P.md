---
title: "Valor P"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - modelos-estadisticos
  - apuntes
status: reference
---


![[Pasted image 20260417004148.png]]

El valor P no se usa en machine learning, es algo propio de la estadística inferencial, en donde no se tienen todos los datos (se tiene una muestra, por ejemplo una encuesta), y se quiere contrastar hipótesis respecto de parámetros, distribución, etc de la población total. 

En machine learning, sobretodo en data empresarial, a menudo se tiene todo el dataset completo, quedando la estadística inferencial más a un campo de experimentos de laboratorio, estudios de mercado, de opinión, etc, escenarios donde nunca se puede tener todas las observaciones de las variables. 

En machine learning no se realizan inferencias poblacionales, porque ya se tiene toda la población. A menos que se quiera pensar que la data viene de una muestra más grande, por ejemplo si tengo data de ventas de una empresa, pensar que ésta es una muestra de las ventas de todas las empresas del sector / país / mundo, etc, en cuyo caso tampoco sería correcto, porque la muestra no sería aleatoria por definición.

Este ejemplo aplica para una prueba "unilateral" para la prueba "bilateral" tendrías que dibujar o trazar la zona de rechazo en ambos extremos de la campana.
