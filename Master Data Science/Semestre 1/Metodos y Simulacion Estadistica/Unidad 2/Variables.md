
# 1. Variable aleatoria
---
## Introducción
---
El concepto de variable aleatoria constituye uno de los principales pilares de la probabilidad y estadística. A este concepto se pueden asociar dos paradigmas de evolución histórica según J.A. Alberth & B. Ruiz (2013) , El primero basada en el resultado de fenómenos aleatorios y por otro lado el proceso que relaciona los conjuntos de espacio muestral y sus respectivas probabilidades, para definir el concepto de variable aleatoria como función de números reales y el espacio para el sustento matemático.

Este concepto está relacionado a diferentes contextos donde se requiere dar respuesta a preguntas relacionadas con la ocurrencia o no de fenómenos aleatorios que eventualmente se presentarán en el futuro, como por ejemplo:

- ¿Cuánto tiempo se tarda un estudiante en ir de su casa a la universidad?
- ¿Cuál será el resultado en mi próximo examen de estadística?
- El dueño de la cafetería se puede preguntar ¿Cuantas botellas de agua se venderán esta semana?
- ¿Cuánto tiempo tardaría la entrega de un paquete una empresa de mensajería?
- ¿Cuánto tiempo dura la bombilla de un vehículo?
- ¿Qué diámetro tendrá la perforación de una máquina en una lámina de acero que hace parte de una puerta de un vehículo?
- ¿Cuantos mensajes recibiré hoy por WhatsApp?
    
En todos los casos se trata de preguntas que tienen diferentes respuestas, o que no tienen un único valor como respuesta. En este documento se estudiará el concepto de variable aleatoria y mediante la definición de una función matemática que nos permita caracterizar su comportamiento, realizaremos diferentes cálculos de probabilidades de interés. Para ello será necesario retomar conocimientos de cálculo integral que serán expuestos en su momento mediante funciones de fácil manejo.

En esta unidad se tratará el caso univariado discreto, luego el caso continuo,con sus principales características, conceptos relacionados con los vistos en el modulo anterior.


## Definición Variable aleatoria
---
Una variable aleatoria $X$ es una función que asigna a cada valor de un espacio muestral $S$ un número . El conjunto formado por estos números conforman un subconjunto de los reales llamado rango de la variable $X$, ($R_X$)

Las variables aleatorias se clasifican teniendo en cuenta las características de su rango en **discretas**, **continuas**. La distribución de una variable aleatoria será *univariada **si se estudia el comportamiento de una sola variable y serán** multivariadas** si se considera el comportamiento conjunto de varias variables definidas sobre el mismo espacio muestral.

## **Tipos de variables**
---
- Una variable XX se considera **DISCRETA** si su rango RXRX es un conjunto finito o infinito numerable de valores.
- Se considera **CONTINUA** si su rango RXRX es un conjunto de valores infinito no numerable y generalmente corresponde a unión de intervalos.

### **Ejemplo**
Un experimento aleatorio ***E***, consiste en lanzar una moneda balanceada al aire tres veces y observar el orden de caras (*c*) y sellos (*s*) que se obtienen en los tres lanzamientos. El espacio muestral ***S*** de ***E**, estará dado por: |

![[Pasted image 20240925173235.png]]

Donde :

- $X$ es la variable que asigna a cada resultado el número de caras en los tres lanzamientos de la moneda.
    
- $R_X={0,1,2,3}$ determinado por la regla de asignación: número de caras en los tres lanzamientos de la moneda y corresponde al rango de valores que puede tomar la variable aleatoria.
    
- $f_X(x) = P(X = x)$ conforma la función que asigna a cada valor de la variable una probabilidad

En este ejemplo :
- $(X = 0) = \{(s, s, s)\}$ ;
- $(X = 1) = \{(s, s, c), (s, c, s), (c, s, s)\}$ ;
- $(X = 2) = \{(s, c, c), (c, s, c), (c, c, s)\}$ ;
- $(X = 3) = \{(c, c, c)\}$.

Bajo el supuesto que la moneda es balanceada, se cumple que los resultados en SS son igualmente posibles y por lo tanto:

$f_X(0) = P(X = 0) = \frac{1}{8}, \quad f_X(1) = P(X = 1) = \frac{3}{8},$

$f_X(2) = P(X = 2) = \frac{3}{8}, \quad f_X(3) = P(X = 3) = \frac{1}{8}$


## **Variables discretas**
Como se mencionó anteriormente una variable aleatoria se considera como **DISCRETA** cuando el conjunto de posibles valores que puede tomar la variables es un conjunto finito o infinito numerable. En la gran mayor ia de los casos este conjunto corresponde a los números enteros.
Para catacterizar la variable se define la función de distribución de probabilidad que modela la asignación de las probabilidades

### **Función de distribución de probabilidad**
![[Pasted image 20240925175806.png]]

### **Ejemplo**

Las siguientes variables se clasifican como **variables aleatorias discretas** :
- $X$: Número de llamadas que entran a un conmutador diariamente
- $Y$: Número de personas contagiadas por Covid 19 durante un día
- $Z$: Número de quejas reportadas a una sucursal bancaria en un día
- $W$: Número de accidentes producidos en una ciudad
- $S$: Número de huevos producidos diariamente en una avícola
- $T$: Número de hijos en una familia
- $M$: Número de mensajes enviados en un grupo de Whatsapp

Como complemento de $f(x)$ y debido a que puede resultar más interesante calcular probabilidades de rangos de valores se define la función de distribución acumulada $F(x)$

### **Función de probabilidad acumulada**
![[Pasted image 20240925175914.png]]

### **Ejemplo**
El restaurante “Asados y algo más” solo da servicio mediante reservas. De acuerdo con los registros diarios en los últimos diez años se sabe que el treinta por ciento de las personas que reservan no llegan al restaurante. El restaurante tiene veinte puestos y acepta cuarenta reservas. La función de distribución probabilidad que modela el número de personas que llegan al restaurante es $f$, dada por:

![[Pasted image 20240925175942.png]]
![[Pasted image 20240925175952.png]]

$P(X=0)=0P(X=0)=0$

$P(X=15)=0.178863P(X=15)=0.178863$
$P(X<15)=P(X≤14)=0.5836P(X<15)=P(X≤14)=0.5836$
$P(X>15)=1−P(X≤14)=0.4164$

## **Variables continuas**
Como se mencionó se considera una variable como continua cuando el conjunto de valores que puede tomar es un conjunto infinito no numerable, es decir que siempre podrá haber un valor entre dos valores de ella.

Para este caso la probabilidad se puede modelar a través de una función continua, la cual se puede visualizar al construir un gráfico de densidad a partir de una muestra de ellos. A esta función se le llama función de densidad de probabilidad

### **Ejemplo**
En el caso de las **variables aleatorias continuas** por lo general proceden de una **medición** como por ejemplo:

- $T$: Tiempo que tarda un estudiante en responder un examen
- $P$: Peso de un bebe recién nacido
- $E$: Edad de una persona
- $V$: Tiempo que tarda un vehículo en requerir una reparación de su motor
- $D$: Diámetro de un agujero realizado en una lamina de acero
- $X$: Cantidad de azúcar contenida en un refresco
- $C$: Proporción de cemento en concreto

### **Función de densidad de probabilidad**
![[Pasted image 20240925180128.png]]

Para el caso continuo la función de distribución de probabilidad corresponde a una integral

### **Función de probabilidad acumulada**
![[Pasted image 20240925180145.png]]

### **Ejemplo**
Con base en información histórica una compañía que fabrica lavadoras determinó que el tiempo YY (en años) para que el electrodoméstico requiera una reparación mayor se obtiene mediante la siguiente función de densidad de probabilidad:

![[Pasted image 20240925180203.png]]

Para tener la seguridad que $f(x)$ puede ser una función de densidad de probabilidad se debe verificar

# 2. **Valor esperado y Varianza**
---
## **Valor esperado**
El valor esperado o esperanza matemática y la varianza corresponde a dos los conceptos principales asociados a una variable aleatoria. El concepto de esperanza está relacionado en un principio con los juegos de azar, pues los jugadores querían conocer cual era el valor esperado de ganar cuando jugaban un gran número de veces.

La esperanza matemática de una variable aleatoria $X$, corresponde a un valor que representa el valor más probable que ocurra o la media población de la variable aleatoria denotada por $E[X]$ o también $μ$



