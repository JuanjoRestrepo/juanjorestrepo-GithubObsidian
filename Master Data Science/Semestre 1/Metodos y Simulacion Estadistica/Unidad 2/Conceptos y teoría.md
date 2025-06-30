# **Probabilidad**
---
Muchos relacionamos el concepto de probabilidad con los dados, pues forma parte de su origen y de su desarrollo inicial a través de preguntas y situaciones imaginarias que de alguna forma la moldearon desde la matemáticas.

Sin embargo este concepto va más allá de los casinos y cobra importancia en la toma de decisiones, cuantificando la ocurrencia o no de alternativas disponibles.

En esta unidad inicialmente se revisan los principales conceptos de probabilidad y de variable aleatoria, para finalizar en la inferencia estadística revisando los conceptos de estimación por intervalos de confianza y pruebas de hipótesis.

# **1. Conceptos básicos**
---
### Métodos y Simulación Estadística

Iniciaremos definiendo tres conceptos, a partir de los cuales se construyen la probabilidad:

### **Experimento aleatorio**
Acción que puede ser replicada bajo las mismas condiciones y cuyo resultado no se conoce por anticipado.

##### **Ejemplo**
- $E_1:$ Lanzar una moneda dos veces y observar los resultados obtenidos en sus caras superiores
- $E_2$: Lanzar dos dados y observar la suma de los resultados superiores
- $E_3$: Realizar un examen de estadística y observar el resultado obtenido
- $E_4$: En una salida de campo, observo si se cumple o no, totalmente el objetivo planteado
- $E_5$: Observo el número total de ensayos de laboratorio exitosos en 20 intentos realizados.
    
### **Espacio muestral**
Conjunto de todos los posibles valores que puede tomar el experimento aleatorio. Este conjunto se nombra con una letra mayúscula SS o también con **Ω**

![[Pasted image 20240924202145.png]]

### **Evento aleatorio**
Subconjunto del espacio muestral que es de nuestro interés. Como todo conjunto se nombra con una letra mayúscula por lo general las primeras letras del alfabeto
##### **Ejemplo**

|       |                                     |                                            |
| ----- | ----------------------------------- | ------------------------------------------ |
| $A_1$ | Obtener solo caras                  | A1={(c,c)}A1={(c,c)}                       |
| $A_2$ | Sacar un resultados es inferior a 4 | A2={(1,1),(1,2)(2,1)}A2={(1,1),(1,2)(2,1)} |
| $A_3$ | Ganar el examen                     | A3={x∈R\|3.0≤x≤5.0}A3={x∈R\|3.0≤x≤5.0}     |
| $A_4$ | Cumplir el objetivo de la salida    | A4={1}A4={1}                               |
| $A_5$ | Obtener más de 5 ensayos éxitos     | A5A5= {x∈N\|6≤x≤20}                        |

### **Resumen**

| Experimento aleatorio                                                                   | Espacio muestral                                 | Evento aleatorio                    |
| :-------------------------------------------------------------------------------------- | :----------------------------------------------- | :---------------------------------- |
| Lanzar una moneda dos veces y observar los resultados obtenidos en sus caras superiores | S1S1= {(cc),(cs),(sc),(ss)}{(cc),(cs),(sc),(ss)} | Obtiener solo caras                 |
| Lanzar dos dados y observar la suma de los resultados superiores                        | S2S2= {(1,1),(1,2),…,(6,6)}{(1,1),(1,2),…,(6,6)} | Sacar un resultados es inferior a 6 |
| Realizar un examen de estadística y observar el resultado obtenido                      | S3S3= {x∈R\|0≤x≤5}{x∈R\|0≤x≤5}                   | Ganar el examen                     |
| En una salida de campo, observo si se cumple o no, totalmente el objetivo planteado     | S4S4= {x∈N\|0≤x≤1}{x∈N\|0≤x≤1}                   | Cumplir el objetivo de la salida    |
| Observo el número total de ensayos de laboratorio exitosos en 20 intentos realizados    | S5= {x∈N\|0≤x≤20}{x∈N\|0≤x≤20}                   | Obtener más de 5 ensayos éxitos     |

# **2. Enfoque**
---
La probabilidad es un número entre cero y uno que se asigna a cada resultado de un evento aleatorio, mediante diferentes enfoques. A continuación se definen los enfoque:

- Clásico o a priori
- Frecuentista
- Subjetiva

### **Enfoque clásico**
Es el enfoque más antiguo de probabilidad y está basado en el supuesto de eventos individuales igualmente probables. La probabilidad bajo ese enfoque para el evento AA se calcula como la fracción entre el número de elementos del conjunto $A, n(A)$ y el número de elementos del espacio muestral $n(S)$

$P(A)=n(A)/n(S)$

En el caso del evento $A1={(c,c)}A1={(c,c)}$, su probabilidad se obtiene como:

$P(A1=n(A1)/n(S1)=1/4=0.25$

Para $A_2$, la suma de los resultados es inferior a 6, se obtiene de la siguiente forma

$P(A2)=n(A2)/n(S2)=9/36=0.25$

En la gran mayoría de casos no se cumplen los supuestos anteriores (eventos equiprobables o con igual probabilidad), pues se tienen eventos con diferentes probablilidades, lo cual impide que podamos utilizar el enfoque clásico.

Ente este problemas debemos suponer que lo ocurrido en el pasado seguirá pasando y así mediante el estudiando la información recogida podemos predecir la posibilidad de ocurrencia de un evento futuro.

### **Enfoque Frecuentista**
Este enfoque se basa en la frecuencia con que ocurre un evento AA y el tamaño de muestra nn, permitiendo calcular la probabilidad como una proporción de veces que ocurre un resultado sobre las veces en que se repite el experimento. Cuanto mayor sea el tamaño de muestra mayor será su proximidad al valor de probabilidad.

![[Pasted image 20240924203211.png]]

![[Pasted image 20240924203220.png]]

Si observamos el cobro de un “penalti” en un partido de fútbol, el cobrador tiene un gran número de posibilidades (lugares) para colocar el balón que podemos simplificar en 9 como se muestra en la Figura 2.1 : (1) parte baja a su izquierda, (2) baja al centro, (3) baja a su derecha, (4) parte media a su izquierda, (5) media al medio, (6) parte centro a la derecha y finalmente (7) parte superior a su izquierda, (8) parte superior al centro y (9) parte superior a su derecha . Por su parte el arquero piensa también es estos lugrares para evitar que el disparo termine en gol. Ambos jugadores estudian las frecuencias para determinar cual lugar ofrece mayores probabilidades de obtener éxito desde su rol.

Para calcular la probabilidad de que un jugador ejecute y convierta un gol de “penalti”, debemos utilizar el enfoque frecuentista, contando para ello información pasada y realizando una división entre el número de aciertos sobre el número total de cobros a cargo del jugador.

### **Enfoque subjetivo**
En este caso la probabilidad es valorada y asignada por un **EXPERTO**, es decir que el valor de probabilidad es asignado a juicio de una persona de acuerdo con su experiencia como: un médico, un ingeniero, un abogado, un economista, un biólogo, un científico de datos …

## **Axiomas de probabilidad**
---
![[Pasted image 20240924203309.png]]

# 3. Tipos de Probabilidad
---
Las probabilidad se puede definir para eventos simples ($A$, $B$,…) o compuestos ( ($A \cup B$), ($A \cap B$), ($B \mid A$) ) que incluyen varios eventos. Dependiendo el tipo de evento puede tomar los siguientes nombres:

![[Pasted image 20240925160244.png]]

## **Probabilidad simple o marginal**
- **P(A):** probabilidad de que ocurra A
- **P(A′):** probabilidad de que NO ocurra A
- **P(B):** probabilidad de que ocurra B
- **P(B′):** probabilidad de que NO ocurra B

## **Probabilidad conjunta**
- $P(A \cap B$): probabilidad de que ocurra A y B
- $P(A′\cap B$): probabilidad de que NO ocurra A y ocurra B
- $P(A\cap B′$) : probabilidad de que ocurra A y NO ocurra B
- $P(A′\cap B′$): probabilidad de que NO ocurra A ni B

## **Probabilidad condicional**
![[Pasted image 20240925160512.png]]

$P(B\mid A)$ se puede leer como :

- Probabilidad de que ocurra B dado que el evento A ya ocurrió
- Probabilidad de que ocurra B sabiendo previamente que ocurrió el evento A
- Si sabemos que ha ocurrido el evento A, la probabilidad de que ocurra B

El efecto de conocer la ocurrencia del evento A hace que el espacio muestral de referencia pase de ser S a solo A. Ahora dentro de este nuevo espacio muestral de referencia se debe establecer la probabilidad de que ocurra B

De esta manera la probabilidad se expresa como la razón entre la probabilidad conjunta $P(A∩B)$ con la probabilidad de $A$, $P(A)$.

### **Ejemplo**
Supongamos que se tiene la siguiente información escrita en una tabla de doble entrada o tabla cruzada que contiene dos eventos $A$ y $B$. En la siguiente tabla se representan los tres tipos de probabilidad :

![[Pasted image 20240925161735.png]]
#### **Probabilidades simples o marginales**
- $P(A)=600/900=0.6667$
- $P(A′)=A−P(A)=1−600/900=1−0.6667=0.3333$
- $P(B)=500/900=0.5556$
- $P(B′=400900)=0.4444$

### **Probabilidad conjunta**
- $P(A∩B)=460/900=0.51111$
    
- $P(A′∩B)=40/900=0.0444$
    
- $P(A∩B′)=140/900=0.1556$
    
- $P(A′∩B′)=260/900=2889$

Esta información también se puede representar como un diagrama de árbol

![[Pasted image 20240925162013.png]]

O también como un diagrama de Venn:

![[Pasted image 20240925162030.png]]

Por despeje se pueden obtener la llanada regla de la multiplicación 😀

![[Pasted image 20240925162045.png]]

## **Eventos independientes**
---
En el caso que se requiera evaluar si dos eventos son independientes o no, partiendo de la definición de probabilidad condicional se podría obtener la siguiente regla al despejar $P(A∩B)$ de la ecuación para obtener : $P(A∩B)=P(A)∗P(B|A)$. En caso de que la ocurrencia del evento AA previamente al evento BB, no cambie su probabilidad, se podría escribir que $P(B|A)=P(B)$ y en este caso la regla indica que la probabilidad conjunta de los eventos $A$ y $B$ es igual a la probabilidad de sus probabilidades marginales :

![[Pasted image 20240925171000.png]]

Para determinar si los eventos A y B son eventos independientes se debe cumplir que:

![[Pasted image 20240925171009.png]]

En el caso que se cumplan todas las condiciones, diremos que los eventos son independientes. En caso contrario, los eventos no son independientes. Una aplicación de este concepto se ilustra con los siguientes ejemplos:

### **Ejemplo**
Se tiene un circuito formado por dos componentes A1A1 y A2A2 cada uno con probabilidad de funcionamiento P(A1)=0.90P(A1)=0.90 y P(A2)=0.95P(A2)=0.95 . Determinar la probabilidad de que el componente funcione.

![[Pasted image 20240925171059.png]]

### **Solución:**

Inicialmente se supone que los componentes A1A1 y A2A2 funcionan de manera independiente. Esto implica que $P(A1∩A2)=P(A1)P(A2)$

Como para que el circuito funcione debe funcionar el componente $A_1$ y $A_2$, utilizando el principio de independencia tenemos que:
$P(A1∩A2)=P(A1)P(A2)=0.90×0.95=0.855$
### **Ejemplo**
Ahora supongamos que el circuito anterior está conectado en paralelo. Determinar la probabilidad de que el circuito funciones

![[Pasted image 20240925171208.png]]
### **Solución:**
En este caso solo hay una manera como el circuito no funciona y es cuando ambos componentes no funcionan. Esto implica que la probabilidad de que no funcione bajo el supuesto que los dos componentes son independientes es:

![[Pasted image 20240925171224.png]]

![[Pasted image 20240925171231.png]]



### **Ejemplo**
---
El departamento de crédito de la universidad, informa que el 30% de los pagos realizados en la universidad se efectúan en efectivo, un 40% con tarjeta de crédito y el resto con tarjeta débito. En todos los casos estos pagos solo son recibidos en la caja ubicada en la oficina de Registro Académico de la universidad.

También se conoce que 20% de los pagos realizados en efectivo, 70% de los pagos realizados con tarjeta de crédito y el 80% de los pagos realizados con tarjeta débito, corresponden a pagos por valores superiores a $500 mil pesos

Con el fin de mejorar el servicio, se esta diseñando un sistema de turnos que agilice el procedimiento de atención . El ingeniero a cargo del diseño de sistema requiere le ayude a valorar las prioridades para las personas que deben pagar mas de $500 mil pesos, pues el ingeniero sospecha que es más probable que una persona requiere pagar más de $500 mil pesos, lo haga con efectivo. Ayude al ingeniero con la información necesaria que le permita reafirmar su sospecha o por el contrario a valorar las diferentes posibilidades

### **Solución:**
Definimos los siguientes eventos :

- **E** : El pago se realiza en efectivo
- **TC** : El pago se realiza con tarjeta de crédito
- **TD** : El pago se realiza con tarjeta débito
- **+5** : El pago es por una cantidad superior a $500 mil pesos

![[Pasted image 20240925171305.png]]

![[Pasted image 20240925171314.png]]

![[Pasted image 20240925171326.png]]

## **Probabilidad Total**
Ahora supongamos que el espacio muestral esta formado por un conjunto de eventos lo podemos representar como una partición del conjunto SS así :

![[Pasted image 20240925171352.png]]

![[Pasted image 20240925171358.png]]

En nuestro caso podemos tener solo cinco particiones para simplificar el procedimiento
![[Pasted image 20240925171411.png]]

Podemos resaltar los conjuntos que conforman a BB :
![[Pasted image 20240925171427.png]]

También podemos reconstruir BB como:
![[Pasted image 20240925171439.png]]

En términos de probabilidad tenemos
![[Pasted image 20240925171501.png]]

Este resultado se puede expresar en otros términos de la regla de la multiplicación:
![[Pasted image 20240925171509.png]]

En general:
![[Pasted image 20240925171522.png]]

En el caso que en el ejemplo anterior se requiere calcular la probabilidad $P(+5)$ utilizamos la regla de la probabilidad total:
![[Pasted image 20240925171547.png]]

## Teorema de Bayes
---
Es una fórmula matemática para determinar la probabilidad condicional . La probabilidad condicional es la probabilidad de que ocurra un resultado, basada en un resultado previo. El teorema de Bayes proporciona una forma de revisar las predicciones o teorías existentes (actualizar las probabilidades) dada la evidencia nueva o adicional. En finanzas, el teorema de Bayes se puede utilizar para calificar el riesgo de prestar dinero a posibles prestatarios

![[Pasted image 20240925171630.png]]

### **Ejemplo**
Continuando con el ejemplo anterior puede ser necesario calcular la probabilidad : $P(E|+5)$ para lo cual utilizamos el Teorema de Bayes

![[Pasted image 20240925171651.png]]

En una fábrica de artículos para protección biodegradables, cuatro operarios colocan etiquetas de caducidad en cada articulo al final de la lı́nea de producción. Juan, quien coloca la fecha de caducidad en un 40 % de los paquetes no logra ponerla en uno de cada 200 paquetes; Luis, quien coloca en 30 % de los paquetes, no logra colocarla en uno de 100 paquetes; Maria, quien coloca etiquetas en el 15 % de los paquetes, no lo hace una vez en 90 paquetes; y Santiago que fecha 15 % de los paquetes, falla en uno de cada 200 paquetes. Si un cliente se queja de que su paquete no muestra la fecha de caducidad. ¿Cuál de los empleados es el más probable culpable de esta omisión?

### **Solución**
Información
![[Pasted image 20240925171707.png]]

![[Pasted image 20240925171715.png]]

## **Aplicaciones**

### **Árboles de decisión**
![[Pasted image 20240925171814.png]]

### **Resultados del árbol**

### **Eventos**
- $S$ : sobrevive
- $S′$ : no sobrevive
- $H$ : hombre
- $M$ : mujer

### **Probabilidades**
- $P(S′)=0.62P(S′)=0.62$
- $P(S)=0.28P(S)=0.28$
- $P(M)=0.35P(M)=0.35$
- $P(H)=0.64P(H)=0.64$
- $P(S′|M==0.26P(S′|M==0.26$
- $P(S|M==0.74P(S|M==0.74$
- $P(S′|H)=0.81P(S′|H)=0.81$
- $P(S|H)=0.19$

