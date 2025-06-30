
# Etapas de la metodología Estadística
---

## Descriptiva:
Consiste en la ***organización de la información en forma útil y comprensible***, mediante la elaboración de cuadros, gráficos y reduciendo los datos por medio de indicadores que faciliten su interpretación.

## Inferencial:
Consiste en el **proceso inductivo que permite inferir** a toda la población proposiciones, basadas en las observaciones y resultados proporcionados por una muestra. Utiliza modelos estadísticos basados en **probabilidades**

## Distribución de frecuencias
Es un **método para organizar y resumir datos**. Bajo este método los datos que componen una serie se clasifican y ordenan, **indicándose el número de veces en que se repite cada valor**.

#### Caso 1: Datos Puntuales
---
![[Pasted image 20240730130952.png]]
![[Pasted image 20240730131002.png]]

Columna 1: Número del Hogar
Columna 2: Número habitantes
Columna 3: Si habitan menores de edad

Una de las alternativas para resumir la anterior información consiste en una ***Tabla de Frecuencias***

![[Pasted image 20240730131116.png]]

![[Pasted image 20240730131351.png]]
![[Pasted image 20240730131512.png]]

#### Caso 2: Datos Agrupados
---
![[Pasted image 20240730131615.png]]

Al tener este tipo de información, utilizar el mismo mecanismo que se usó para agrupar los datos por su distribución en frecuencias ***no es lo mejor***, porque al final resultará que ***todos los registros pueden ser o son únicos, teniendo un frecuencia absoluta de uno***. 
***El objetivo de resumir la información no se cumple***

##### ***¿Qué se puede hacer?***
Agrupar la información. 
En este caso lo haremos por intervalos

### Ejemplo:

![[Pasted image 20240730131902.png]]

![[Pasted image 20240730132006.png]]

Si observamos, los intervalos no se construyeron de cualquier manera, es decir, hay una amplitud entre intervalos.

Con base en estos datos agrupados por intervalos, podemos realizar un **Histograma de Frecuencias**

![[Pasted image 20240730132213.png]]

## Resumen Reducción de Datos
---
![[Pasted image 20240730132305.png]]

## Indicadores
---

### 1. Indicadores de Tendencia Central
- ***Media Aritmética o Promedio*** (Suma todas las características, dividido entre el total de elementos)
- ***Mediana*** (Valor medio, que está en la mitad entre todos los datos)
- ***Moda*** (Valor que más se repite)

Los que más se suelen utilizar son la Media Aritmética y la Mediana. Para ello se debe tener en cuenta que:

- Estos indicadores pueden tener una ***sensibilidad***, es decir, que ciertos indicadores como ***la media pueden afectarse*** cuando los valores son ***muy grandes o muy pequeños***

![[Pasted image 20240730134455.png]]
En este caso, el valor ***70.000*** al ser el más grande, tendrá un efecto significativo en la ***media artimética o promedio***, pues se va a inflar más.

![[Pasted image 20240730134626.png]]

***El promedio, pueder ser el más útil ya que toda en cuenta toda la información***, excepto cuando hay datos atípicos

### 2. Indicadores de Dispersión
![[Pasted image 20240730134743.png]]

- ***Rango*** (Toma en cuenta los valores extremos, osea el mínimo y máximo). No es tan utilizado en la práctica.
- ***Varianza*** (Es un paso intermedio para calcular la desviación estándar)
- ***Desviación Estándar*** (Nos dice en promedio qué tanta oscilación hay entre los datos y el valor de tendencia central que es el promedio.)
- ***Coeficiente de Variación*** (Mide cómo esa variación la puedo cuantificar en términos porcentuales. Nos ayuda a comparar dos grupos a partir de la variabilidad)

### 3. Indicadores de Posición
Permiten hacerse una idea acerca de la forma de la ***distribución de una variable y su dispersión***
#### ![[Pasted image 20240730155225.png]]

![[Pasted image 20240730155236.png]]

![[Pasted image 20240730155322.png]]
![[Pasted image 20240730155546.png]]

Los percentiles se utilizan en ciencia de datos para comprender la distribución de los datos, identificar valores atípicos, y realizar análisis comparativos. Como por ejemplo:

#### **Identificación de valores atípicos**
---
Los percentiles pueden ayudar a identificar valores extremos o atípicos en un conjunto de datos. `Q1 - 1.5(Q3-Q1)` y `Q3 + 1.5(Q3-Q1)`, representan dos límites a partir de los cuales se consideran datos atípicos. Este método fue planteado por John Tukey (1977).
  
#### **Análisis de rendimiento en pruebas estandarizadas**
---
En el sector de la educación, los percentiles se utilizan comúnmente para informar sobre el rendimiento de los estudiantes en pruebas estandarizadas. Un puntaje en el percentil 75, por ejemplo, indica que el estudiante superó al 75% de los participantes.

#### **Evaluación de distribuciones de ingresos**
---
En economía y sociología, los percentiles son útiles para entender la distribución de ingresos. Las curvas de distribución de la riqueza se basan en los quintiles, los cuales corresponden a los percentiles : P20, P40, P60, P80.

#### **Segmentación de audiencia en marketing**
---
En marketing, se pueden utilizar percentiles para segmentar audiencias según el comportamiento del cliente. r

#### **Evaluación de rendimiento en deportes**
---
En análisis deportivo, los percentiles se utilizan para evaluar el rendimiento de los atletas en comparación con otros en ciertos aspectos, como velocidad, resistencia o fuerza.

#### **Establecimiento de límites para decisiones empresariales**
---
Los percentiles pueden utilizarse para establecer límites o umbrales en decisiones empresariales. Basados en un indicador premiar a los empleados que se encuentren del percentil 95 en adelante.

#### **Comparación de rendimiento de modelos en aprendizaje automático**
---
En el desarrollo de modelos de aprendizaje automático, los percentiles pueden ser útiles para comparar el rendimiento de diferentes modelos en diferentes regiones de la distribución de datos.

#### **Determinación de valores críticos en salud**
---
En estudios de salud, los percentiles se utilizan para establecer valores de referencia para medidas biológicas como el índice de masa corporal (IMC), la presión arterial, entre otros.


### 4. Indicadores de centro
Una vez que se han organizado los datos y se ha observado su distribución a través de tablas o gráficos de frecuencias, en ocasiones se requiere de **indicadores** que resuman los datos, es decir que en forma muy directa puedan indicar rasgos importantes de las observaciones, como su magnitud, su homogeneidad y su simetría

Entre los principales indicadores de tendencia central se encuentran: 
- La **media aritmética** o **promedio aritmético** (o simplemente media o promedio), 
- La **mediana**
- La **moda**

1. **Media aritmética**: Es el indicador de tendencia central más conocido y utilizado por su fácil interpretación y calculo. Consiste en sumar todos los valores de un conjunto de datos y dividirlos por el número de datos.
![[Pasted image 20240924194825.png]]
##### **Propiedades de la media**
- La suma de las desviaciones de los datos con respecto a la media es cero.  $∑(xi−x¯)=0$$∑(xi−x¯)=0$.
- La suma de los cuadrados de las desviaciones de los datos con respecto a un valor $a$ es mínimo cuando  $a=\overline{x}$
- Si $x_i=k$ para todo $i$, entonces, $\overline{x}=k$
- Si todos los datos de una variable se multiplican por una constante $k$, es decir $y_i=kx_i$ entonces $\overline{y} = k\overline{x}$
    
- Si $z_i=ax_i+by_i$ $, donde: **a**, **b** constantes y $x_i$, $y_i$ variables, entonces: $\overline{z}=a\overline{x}+b\overline{y}$

2. **Mediana:** La **mediana** es el número que divide la muestra en dos partes de igual proporción (50% : 50%). Es decir que corresponde al percentil 50.

![[Pasted image 20240924195709.png]]

![[Pasted image 20240924195757.png]]La línea central de las cajas representan las medianas. En ellas se puede evidenciar el valor mayor del grupo juvenil femenino.

3. **Moda:** La **moda** corresponde al dato o valor que más se repite. Es utilizada como medida de tendencia central en variables cualitativas o en cuantitativas discretas con pocos valores.

4. **Media truncada:** Con el fin de evitar que los datos atípicos generen sesgos en el indicador de la media, es posible separar el 90% central de los datos, quitando un 5% de los datos más pequeños y un 5% de los datos mayores. A este indicador se le llama **media truncada** al 10% ($\overline{x}_{0.10}$)

5. **Rango medio:** El rango medio se obtiene al sumar los valores extremos ( mínimo y máximo) y dividir el resultado por dos. Este indicador es de fácil cálculo y útil cuando se desea una estimación empírica y alta precisión en datos simétricos.

![[Pasted image 20240924200233.png]]



### 5. Indicadores de dispersion
---
Supongamos que tenemos dos grupos de participantes que son patrocinados por dos empresas. Se sabe que ambos grupos tienen igual en promedio de edad. Lo que primero se puede pensar es que los dos grupos tienen una composición igual o muy parecida dado que coinciden en el promedio. Pero no es así, los datos que se presentan a continuación tienen medias de 28, pero corresponden a grupos diferentes.

|             |                                                             |
| ----------- | ----------------------------------------------------------- |
| **Grupo 1** | 27, 27, 28, 28, 34, 28, 26, 33, 24, 28, 25, 25, 33, 27, 34, |
|             | 38, 24, 26, 22, 23, 33, 23, 26, 26, 32, 33, 29, 30, 25, 23  |
| **Grupo 2** | 35, 25, 19, 17, 24, 17, 55, 25, 31, 35, 43, 28, 32, 19, 20, |
|             | 17, 25, 18, 21, 22, 17, 35, 29, 20, 54, 46, 24, 29, 40, 18  |

Hace falta otro indicador que nos oriente sobre, qué tan dispersos son los datos con el fin de saber si se trata de grupos parecidos tanto en centro como en variabilidad. Esta necesidad la suplen los `indicadores de dispersión`.

![[Pasted image 20240924200344.png]]

#### **1. Rango**
El rango es el indicador de dispersión más fácil de calcular, pues se obtiene restando los valores extremos de los datos:

$r=max(x)−min(x)$

##### **Ejemplo**
En el caso de los dos grupos:

|**Grupo 1**|**Grupo 2**|
|:--|:--|
|x¯1=28x¯1=28 años|x¯2=28x¯2=28 años|
|r1=16r1=16 años|r2=38r2=38 años|

Este complemento al indicador de centro permite distinguir que se trata de dos grupos diferentes

#### **2. Varianza**
Es la medida de dispersión más utilizada en estadística y está definida por :

![[Pasted image 20240924200504.png]]

Se podría afirmar que la varianza es un promedio de los cuadrados de las diferencias entre los datos y su media.

##### **Propiedades de la varianza**
![[Pasted image 20240924200531.png]]

El problema de la varianza es su **interpretación**, pues sus unidades quedan al cuadrado y en la mayoría de los casos no es posible interpretar los resultados. Por esta razón se optó por utilizar otra medida de dispersión calculada a partir de la raíz cuadrada de la varianza.

#### **3. Desviación estándar**

Es la raíz cuadrada de la varianza

![[Pasted image 20240924200558.png]]

#### **Ejemplo**

|**Grupo 1**|**Grupo 2**|
|:--|:--|
|x¯1=28x¯1=28 años|x¯2=28x¯2=28 años|
|s21=16.62s12=16.62 años22|s22=116.89s22=116.89 años22|
|s1=4.16s1=4.16 años|s2=10.81s2=10.81 años|
|||

Aunque la desviación estándar reduce el problema mencionado anteriormente debido a tener las mismas unidades de la variable, es útil para comparación de dos grupos con igual media. En caso de que las medias sean diferentes es difícil poder realizar las comparaciones.

***Nota: Las propiedades definidas para la varianza no aplican para la desviación estándar dado que la raíz cuadrada no es una función lineal***

#### **4. Coeficiente de variación**
Por último, el coeficiente de variación es un indicador adimensional que indica que tan grande o que tan pequeña es la desviación estándar con respecto a su media en porcentaje y de esta manera podemos resolver el problema de la dispersión para cualquier grupo de datos.

![[Pasted image 20240924200708.png]]

Existen diferentes reglas empíricas para la interpretación del coeficiente de variación. Una de ellas establece como límite el 20% para separar los grupos homogéneos de los heterogéneos, por lo general se utiliza un valor hasta el 20% para determinar que un grupo de datos son homogéneos, de lo contrario se calificará como heterogéneo.

#### **Ejemplo**

|**Grupo 1**|**Grupo 2**|
|:--|:--|
|x¯1=28x¯1=28 años|x¯2=28x¯2=28 años|
|CV1=15CV1=15 %|CV2=39CV2=39 %|

En este caso se obtienen valores diferentes para los dos grupos. El grupo 1 con un valor inferior a 20%, que indica homogeneidad y el grupo 2 con un valor superior que indica heterogeneidad


### 6. Indicadores de forma
---

Los indicadores de forma permiten adicionar elementos a la interpretación de los datos.

#### **1.Curtosis**
Se mide a través del coeficiente de curtosis que mide cuan **puntiaguda** es una distribución respecto a un patrón estándar que es la curva de la distribución normal. Esta característica está relacionada directamente con la dispersión.

![[Pasted image 20240924200855.png]]

De acuerdo con su valor, la puntudez de los datos puede clasificarse en tres grupos:

- **Leptocúrtica**, con valores grandes para el coeficiente (CA>0)
- **Mesocúrtica**, con valores medianos para el coeficiente (CA=0)
- **Platicútrica**, con valores pequeños para el coeficiente (CA<0)

![[Pasted image 20240924200912.png]]

#### **2. Asimetría o sesgo**
Mide que tanto la forma de la distribución de frecuencias de los datos es simétrica o no con respecto a la media. Esta característica de los datos se mide a través del coeficiente de asimetría o sesgo.

![[Pasted image 20240924200938.png]]

- Es **simétrica** si el valor del indicador es 0 (x¯=Mex¯=Me)
- Es **asimétrica a la izquierda**> si el valor del indicador es negativo (x¯<Mex¯<Me)
- Es **asimétrica a la derecha** si el valor del indicador es positivo (x¯>Mex¯>Me)

![[Pasted image 20240924200949.png]]

### **Interpretación**
- **Asimetría negativa** : Una prueba con resultados asimétricos a la izquierda o negativa, indica que pocos obtuvieron resultados bajos y que muchos alcanzaron resultados altos, pudiendo indicar que la prueba era relativamente fácil (poco con poco y mucho con mucho).
- **Simétrica** : En este caso una prueba con resultados simétricos indica que los puntajes se ubicaron al rededor de la media y que unos pocos sacaron puntaje bajo y que los que presentaron resultados altos corresponden a un pequeño grupo. Por lo regular estos son los resultados de pruebas estandarizada como pueden ser las pruebas de estado (poco con poco y poco con mucho).
- **Asimetría positiva** : Los resultados a pruebas con asimetría a la derecha o positiva, presentan resultados acumulados a la izquierda, es decir que muchos obtuvieron resultados bajos y unos pocos resultados altos. Esto haría pensar que la prueba fue exigente (mucho con poco y poco con mucho).


|             🔙 Volver a              |               Seguir a ⏭️                |
| :----------------------------------: | :--------------------------------------: |
| [[Datos profesora\|Datos profesora]] | [[Experiencia\| Unidad 1 - Experiencia]] |

