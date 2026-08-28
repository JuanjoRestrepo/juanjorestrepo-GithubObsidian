---
title: "Conceptos de pruebas de hipótesis"
date: 2026-08-27
tags:
  - maestria
  - semestre-1
  - estadistica
  - apuntes
status: reference
---

Es posible estimar un parámetro de datos muestrales, bien sea una ***estimación puntual*** o un ***intervalo de confianza***

#### **¿Si mi objetivo no es estimar un parámetro, sino determinar el cumplimiento de una hipótesis sobre un parámetro?**

##### Ejemplo: El tiempo de vida de determinado producto es de **8 meses**

Lo que queremos hacer en base a lo anterior, comprobar el cumplimiento de la hipótesis de si realmente son 8 meses de vida


# 1. Pruebas de hipótesis
---
Es un procedimiento estadístico que **a través del estudio de una muestra aleatoria** permite **determinar el cumplimiento de una hipótesis planteada sobre alguna característica** de la población

## Características:
---
- La decisión se toma partiendo de la evidencia que se recaba a través de una muestra aleatoria
- Determina mediante cálculo de probabilidades si el cumplimiento de la hipótesis es razonable

![[Pasted image 20240925142723.png]]

- N: población total
- n: muestra

La muestra que saco me arrojará ***el estimador***, el cual no es una característica fija, es decir, es algo que puede tomar diferentes valores dado que al tomar otro valor aleatorio como muestra, siempre nos puede dar diferentes resultados.

Para verificar que la hipótesis que se plantea es correcta, en este caso, el valor de la media $\overline{x}$ es muy cercano al valor del promedio que se plantea en la hipótesis

Si es incorrecta, el valor de la hipótesis estaría muy alejado del valor que obtuve de la muestra que escogí, siendo una posibilidad para rechazar nuestra hipótesis

***Nota: La decisión final se fundamenta en la evidencia recogida a través de una muestra representativa***

## Definiciones:
---
1. **Hipótesis de investigación:** idea o conjetura que se tiene a priori y que se desea contrastar a través de la realidad
	Ejemplos:
		- ***H1:*** ***La proporción de comestibles duros que no cumple con los estándares de calidad es superior al 2%***
		-  ***H2:*** ***El peso del promedio de las pastillas de Frunas es de 3 g***

2. **Hipótesis de Estadística:** representación de la hipótesis de investigación en forma de **ecuación matemática** y en función de **parámetros poblacionales**
	Ejemplos:
		- ***H1: P > 0.02***  La proporción de comestibles duros que no cumple con los estándares de calidad es superior al 2%
		-  ***H2 $\mu = 3$ :*** El peso del promedio de las pastillas de Frunas es de 3 g

Las hipótesis de investigación pueden desglosarse en dos hipótesis estadísticas que se denominan ***Hipótesis Nula*** e ***Hipótesis Alterna***

3. ***Hipótesis Nula y Alterna:*** La Nula siempre debe plantearse ***en términos de igualdad*** mientras que la Alterna dependerá del ***conocimiento que tenga el investigador*** o de la hipótesis de investigación
	Ejemplos:
		- ***H0: P = 0.02 vs H1: P> 0.02***  La proporción de comestibles duros que no cumple con los estándares de calidad es superior al 2%
		-  ***H0: $\mu = 3$ vs H1: $\mu < 3$ o $\mu > 3$ o $\mu = 3$*** El peso del promedio de las pastillas de Frunas es de 3 g
		DEPENDE DEL OBJETIVO DEL INVESTIGADOR
	
### ¿Bajo qué criterio se acepta o no la Hipótesis Nula?

Dado que no es posible conocerse con total seguridad la verdad o falsedad de la hipótesis, a menos que se examine a TODA LA POBLACIÓN. Para aceptar o rechazarla, solamente es en base a lo que se observe en una muestra aleatoria

El valor del estimador dará alguna evidencia sobre el valor que asume el parámetro

![[Pasted image 20240925145548.png]]

### Errores en las pruebas de hipótesis

![[Pasted image 20240925145632.png]]
![[Pasted image 20240925145803.png]]
![[Pasted image 20240925145823.png]]

## Formulación matemática de referencia

Para contrastar una media poblacional, una formulación bilateral es:

$$
H_0:\mu=\mu_0
\qquad \text{frente a} \qquad
H_1:\mu\neq\mu_0.
$$

Si la desviación estándar poblacional es desconocida y las condiciones del modelo $t$ son razonables, el estadístico de prueba es:

$$
t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}.
$$

Con nivel de significancia $\alpha$, se rechaza $H_0$ cuando el valor $p\leq\alpha$. El error de tipo I tiene probabilidad $P(\text{rechazar }H_0\mid H_0\text{ verdadera})=\alpha$ y el error de tipo II tiene probabilidad $\beta=P(\text{no rechazar }H_0\mid H_1\text{ verdadera})$.

La elección de la prueba exige comprobar independencia, diseño muestral, escala de medición y supuestos distribucionales.
