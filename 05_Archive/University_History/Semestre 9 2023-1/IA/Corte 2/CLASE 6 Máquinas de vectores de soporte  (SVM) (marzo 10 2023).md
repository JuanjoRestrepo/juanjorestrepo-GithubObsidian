---
banner: https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhg5ZOfLYvhYPGxr9Av9FXJnaNdxsK3R0oZGjmiAKNEgXoLFPZYJ1CGswXqEEkIocV30aAWALrwHtFc1N1zIb9prFFxEhNutPwJzAtiz7P-xaYUM-KEpMmVjBK1eSEi6cv0chmB5ch8NPiBukCH1xrophjj0-iUgFA6ppvKQEbPcmpbfMJju1lk802EEQ/w0/svm_intro%20(2).png
tags:
  - "#Semestre9"
  - IA
  - "#SVM"
fecha: 2023-03-10
---
## **Márgenes Duras**

En clasificación binaria la idea es construir un hiperplano de decisión que divida las muestras positivas (con etiqueta $+1$) y negativas (con etiqueta $-1$).

Como ejemplo, consideremos los datos mostrados en la figura, los cuales son linealmente separables ya que pueden dividirse a partir de una recta.

![[Diagrama_Margenes_Duras.png.png]]

De lo anterior, podemos ver que existen infinitas rectas (o hiperplanos) las cuales dividen al conjunto de datos en dos, la idea es encontrar la recta (o el hiperplano) que maximiza laś métricas de clasificación. 

**PARA EL CASO DE LOS SVMs**

- Particularmente, las SVMs seleccionan la recta  que maximice el margen de separación entre las clases
- El margen se define como la suma de las distancias del hiperplano a su punto m ́as cercano en cada clase
- Los puntos m ́as cercanos al hiperplano de separación se denominan vectores de soporte.  

En la siguiente figura se reconocen tres vectores de soporte:

![[Diagrama_Tam_Margen.png]]

En el ***MARGEN*** **NO PUEDE EXISTIR NADA**, debe estar limpio para que el algoritmo CONVERGA

La idea, es ***MAXIMIZAR*** el margen, el canal para evitar errores de clasificación.

![[Diagrama_Margen_Cuaderno.png]]

En lo anterior, si se tiene un Margen pequeño, esto puede llevar a posibles errores de clasificación en el modelo.

Las SVMs determinan el hiperplano de separación a partir de la solución del siguiente problema de optimización cuadrática

![[Ecuacion_1.png]]
$$\min_{w, w_0} \frac{1}{2} \lVert{W } \lVert^2  $$   
sujeto a
$$ y_n(W^TX_n + W_o) \geq 1, n-1 ...,N$$
Donde recordemos que la etiqueta $y_n$ puede ser $1$ ó $-1$

La restricción $y_n(W^TX_n + W_0) \geq 1$ garantiza que todos los puntos estén en el lado  correcto del plano de decisión.

*una vez se entrena el modelo, a este solo le interesan los valores diferentes de cero, **NO TODOS SON NECESARIOS** *

Dado que el problema de optimización tiene restricciones, se usan multiplicadores  de Lagrange; de esta forma, se configura el siguiente “*problema dual*"

![[Ecuacion_2.png]]

Una vez se determinan los valores del vector ***a*** y dada una muestra del conjunto de  prueba ***x***, se puede predecir su etiqueta como:

![[Ecuacion_3.png]]

- Notemos que cuando el valor $a_n = 0$, la muestra xn no participa en el c ́alculo de la predicción.  
- Por el contrario, cuando **$a_n > 0$**, la muestra xn se considera como un vector de soporte y contribute al cálculo de las predicciones.  

- Podemos analizar que el vector a funciona como un filtro. Este filtro elimina, para el cálculo de las predicciones, todas las muestras que no est ́en cercanas al hiperplano de decisión.  
- Por último, el parámetro $w_0$ es necesario para el c ́alculo de las predicciones. Este  valor se determina a partir de la ecuación:
![[Ecuacion_4.png]]

donde ***S*** es el conjunto de de ́ındices correspondientes a los vectores de soporte y ***|S|*** representa el n ́umero de elementos en dicho conjunto.

**2. Márgenes suaves**


## **Márgenes Suaves**

- Las SVMs con m ́argenes duras solo se pueden aplicar a datos linealmente separables. Si los datos no son linealmente separables, el problema de optimización no tiene solución.
- En general, es más común encontrar datos, como en la  figura, donde la estructura es principalmente lineal, pero existen algunos datos que se traslapan.

![[Diagrama_Margenes_Suaves.png]]

Una solución a esta condición, es la inclusión de un conjunto de variables de holgura $\zeta_m \geq 0$ 
-   Las muestras con  $\zeta_m = 0$  están correctamente clasificadas y se encuentran fuera del margen.  
• Para $0 < \zeta_m \leq 1$  la muestra es clasificada  correctamente, pero se encuentra dentro de la  margen.  
• Finalmente, un $\zeta_m > 1$  indica que la muestra está en el lado incorrecto del hiperplano y por lo tanto se clasificar ́a de forma errónea.  


**Al incluir las variables de holgura, el problema de optimizaci ́on se puede reescribir como**

![[Ecuacion_5.png]]
![[Descripcion_Ecuacion_5.png]]



Al igual que con el planteamiento original de las SVMs, se usan los multiplicadores de Lagrange para formular el siguiente “problema dual”

![[Ecuacion_6.png]]

## **SVMs para datos que no son linealmente separables**
  
Las formulaciones vistas hasta el momento se  aplican para datos con estructuras lineales. Sin embargo, es común encontrar datos con estructuras no lineales.

![[Estructura_NoLineal.png]]

Por ejemplo, en la figura se muestra un conjunto datos de una dimensión que no pueden separarse a partir de rectas o hiperplanos.  

• Una alternativa es realizar una transformación no lineal $\varphi$ de los datos a un espacio de mayor dimensión con el fin de mejorar su representación.

![[Transformación_No_Linea.png]]

• Para el ejemplo, vamos a realizar la siguiente transformación no lineal para obtener un espacio de dos dimensiones $φ(x) = [x, x2]$.  
• De esta forma, como se muestra en la figura, la transformación produce datos que son linealmente separables


***El teorema de Cover*** establece que si a un conjunto de datos se le aplica una transformación  no-lineal, donde la dimensión de la transformación es lo suficientemente grande, los datos transformados tienen alta probabilidad de ser linealmente separable.  

• En este sentido, los datos transformados pueden ser clasificados a partir de rectas.  
• Existen infinitas formas de para definir la transformación  φ(x). Dichas transformaciones modifican levemente el problema de optimización. Por ejemplo, el problema dual para las ***SVMs*** con margen suave se escribe como:

![[Problema_Dual_SVMs_Margen_Suave.png]]

• Podemos notar que la única variación es que en lugar de usar los datos originales (no lineales), se usan los datos transformados.  
• Las transformaciones *no-lineales* se suelen realizar, de manera implícita, a partir de las **funciones kernel *κ*.**  
• Las funciones kernel mapean los datos originales a un espacio euclidiano, que en teoría es de dimensión infinita. Este espacio se conoce como ***Espacio de Hilbert*** con ***kernel reproductivo***.  

## **Función Kernel**

Una función kernel es una representación del producto matricial de los datos transformados. De esta forma:
![[Ecuacion_Kernel_1.png]]

Así, el problema dual para las SVMs con margen suave y con función kernel se escribe como:
![[Ecuacion_Kernel_2.png]]

De igual forma, para la ecuación predictiva tenemos:
![[Ecuación_Predictiva.png]]
En donde:
![[Tabla_Kernels.png]]
Los valores *d*, $\sigma^2$, $B_0$ y $B_1$ se denominan hiperparámetros y deben ser elegidos por el usuario

## EN RESUMEN:

**Hiperparámetros de entrada:**  
1. ***C***: error de penalización. Parámetro que controla cuántas muestras pueden violar el margen
Si $C \to \infty$, permite a  "todos" (en teoría) los datos y tendríamos 

3. **Parámetros del kerne**l (por ejemplo σ en el kernel Gaussiano o d en el polinómico)  

**Pasos para el entrenamiento:**  
1. Seleccionar el kernel  
2. Seleccionar los parámetros del kernel  
3. Seleccionar el parámetro ***C***  
4. Resolver el problema de optimización.  

SIGUIENTE:
[[CLASE 7 Redes Neuronales (marzo 17 2023)]]
