# Métodos
---
En esta unidad nos ocuparemos de construir conocimiento en torno a tres conceptos. Conceptos básicos de estadística , análisis exploratorio de datos y manejo del software R.

Utilizaremos los pasos de la **Metodología Estadística** como estrategia para ubicar los métodos estadísticos empleados en este curso :

1. **Definición del problema**
2. **Definición de los objetivos**
3. **Definición de las variables de interés**
4. **Diseño del experimento**
5. **Recolección de la información**
6. **Procesamiento de los datos**
7. **Análisis descriptivo o exploratorio de datos**
8. **Inferencia estadística**
9. **Conclusiones y recomendaciones**

La **Metodología Estadística** está basada en el método científico que corresponde a un procedimiento iterativo de aprendizaje, el cual está compuesto por las siguientes etapas:

1. Formulación de una hipótesis,
2. Observación,
3. Análisis de información, prueba de la hipótesis, interpretación de resultados y decisión.

Es necesario tener en cuenta al realizar un análisis exploratorio de datos los pasos previos a este, como son la definición del problema objeto de estudio, cual será nuestra meta (objetivos) o finalidad del estudio. Que variables debemos recoger para poder cumplir con el objetivo propuesto, además del diseño del experimento, es decir como se requiere recolectar la información, cuanta información, las fuentes y los medios para su procesamiento.

Después de tener claridad sobre los pasos anteriores (1 a 6 de la metodología estadística) se empieza el análisis exploratorio de datos. Con él realizamos una primera aproximación a los objetivos planteados.

  
Contenido de la unidad :

- **Conceptos básicos de Estadística**
    - Conceptos
    - Importar datos
    - Limpieza de datos

- **Análisis de datos**
    - Tablas de contingencia
    - Indicadores
        - Indicadores de posición
        - Indicadores de centro
        - Indicadores de dispersión
        - Indicadores de forma

- **Visualización de datos**
    - Representación variables cualitativas
    - Representación variables cualitativas
    - Representaciones bivariadas
    - Representaciones multivariadas

- **Software R**
    - Introducción
    - Objetos en R
    - Referencias


# Conceptos básicos
---
## **¿Qué es ESTADÍSTICA?**

**ALGUNAS DEFINICIONES DE ESTADÍSTICA**

- _“Estudio matemático de la incertidumbre y la variabilidad, que proporciona herramientas y métodos para describir, modelar y analizar fenómenos aleatorios y tomar decisiones basadas en la información disponible” Andrei Nikolaevich Kolmogorov (1933)_.
- _“Ciencia que trata de la toma de decisiones en presencia de incertidumbre mediante el uso de datos observados”. Fisher, R. A. (1959)_
- _“Conjunto de métodos para recopilar, organizar, resumir, presentar y analizar datos, así como para obtener conclusiones válidas y tomar decisiones razonables basadas en tal análisis”. Walpole, R. E (2012)_
- _“Ciencia que utiliza métodos para recopilar, describir, analizar e interpretar datos, así como para tomar decisiones basadas en dichos análisis”. David R. Anderson (2013)_

La **Estadística** surge como la herramienta ideal para cercar los efectos de incertidumbre inherentes a la gran mayoría de procesos biológicos, químicos, industriales y de comportamiento humano, en donde predominan los efectos del azar y la incertidumbre.

El objetivo de la **Estadística** se centra en brindar apoyo en la transformación de datos en información. 
Teniendo en cuenta que: 
- Los datos son sólo la ***representación numérica o categórica de una medición.***
- La información es ***la integración de esos datos y factores del contexto*** para generar un criterio suficiente en la toma de decisiones.

## **¿Dónde aplicarla?**
---
La **Estadística** es una ciencia transversal a las diversas disciplinas del conocimiento, como, por ejemplo: finanzas, ingeniería, salud, economía, contabilidad, mercadeo, sociología y ciencias, entre muchas otras. Algunos ejemplos de su aplicación son:

- **Finanzas**: se realizan estudios para estimar el riesgo que tiene una inversión o el préstamo de dinero por parte de una entidad bancaria.
- **Ingeniería**: la estadística permite realizar el control de calidad de productos.
- **Salud**: es utilizada para realizar múltiples investigaciones que generan mejores tratamientos para las enfermedades.
- **Economía**: la estadística permite estudiar los determinantes del desempleo o el crecimiento económico en una región.
    
Encontraríamos más ejemplos donde se tiene la ***necesidad de contar con información que nos permita tomar decisiones confiables***

### **Actividad**
De acuerdo con tu área de profesión, identifica alguna situación o actividad donde sea necesaria la Estadística.

#### Respuesta:
En el campo de la ingeniería electrónica, la estadística es fundamental en varias áreas:

**1. Control de Calidad Industrial y Pruebas de Productos:**
- **Descripción:** En la fabricación de componentes electrónicos, la estadística se utiliza para monitorear y controlar la calidad del producto. Esto incluye la identificación de defectos y la variabilidad en el proceso de producción.
- **Aplicación Estadística:** Uso de gráficos de control y análisis de capacidad del proceso para asegurarse de que los productos cumplan con las especificaciones requeridas.

**2. Análisis de Datos de Sensores:**
- **Descripción:** Los sistemas electrónicos a menudo recopilan datos de sensores que deben analizarse estadísticamente para extraer información útil.
- **Aplicación Estadística:** Métodos de regresión, análisis de series temporales y técnicas de aprendizaje automático para analizar y predecir el comportamiento de sistemas basados en datos de sensores.

**3. Análisis de Confiabilidad y Vida Útil:**
- **Descripción:** La estadística se utiliza para predecir la confiabilidad y la vida útil de los componentes y sistemas electrónicos.
- **Aplicación Estadística:** Métodos como el análisis de supervivencia y modelos de riesgos proporcionales para analizar datos de tiempo de fallo y mejorar el diseño y la durabilidad de los productos.

**4. Procesamiento y Análisis de Señales:**
- **Descripción:** En el procesamiento de señales, la estadística se usa para filtrar ruido, detectar señales y mejorar la precisión de los sistemas de comunicación.
- **Aplicación Estadística:** Métodos como la estimación espectral y el análisis de Fourier para el procesamiento y análisis de señales.

## **Conceptos**
---
### **1. Análisis descriptivo**
La Estadística Descriptiva comprende los métodos para organizar, resumir y presentar datos de manera informativa. Su fin es únicamente exploratorio y se limita a describir lo observado en una población o muestra.

Su objetivo es la exploración sin restricciones de los datos en busca de regularidades interesantes. Las conclusiones solo se aplican a los individuos y a las circunstancias para los cuales se obtuvieron los datos, además son informales y se basan en lo que se observa en los datos.
#### Ejemplo
Descripción de la producción mensual de café durante el año 2023 través de una tabla o gráfico lineal o de barras, además se puede comparar las variaciones porcentuales del año 2016 respecto al 2022.


### **2. Inferencia estadística**
La estadística inferencial consiste en el proceso inductivo que permite inferir o generalizar a toda la población características observadas en una muestra.
Su objetivo es responder a preguntas concretas que se plantearon antes de la obtención de los datos. Las conclusiones se aplican a un grupo más amplio de individuos o situaciones, son formales y se hace explicito el grado de confianza que se tienen sobre ellas.
#### Ejemplo
A partir de una muestra aleatoria regional en el Valle del Cauca de 550 estudiantes se encuentra que el 45% de ellos están cursando primaria, esta proporción se generaliza a toda la población del departamento.


## **3. Validez**
Es posible hacer uso de los pasos de una persona para medir la distancia entre dos puntos. ¿Este sería confiable?

La respuesta a esta pregunta es **NO**. Dado que los pasos de una persona pueden ser diferentes a los de otra persona debido a la diferencia en sus tallas. Las mediciones realizadas por diferentes personas genera una variabilidad extra inherente al sujeto que realiza la medición, afectando así los datos que se obtienen a partir de este.
La mejor alternativa en este caso es hacer uso de instrumentos calibrados, estandarizados o validados, como un flexómetro, rueda métrica, etc. De tal manera que, si la medición se toma varias veces con el mismo instrumento, esta no varié, de una a otra medición.
Es el grado en que la medición puede generalizarse a otras situaciones no medidas, depende en gran proporción de la conformación adecuada de la muestra a través de métodos estadísticos.
#### Ejemplo
Un estudio desea concluir sobre el ingreso promedio por vivienda de las familias de la ciudad Cali. Si en el estudio solo se encuestan familias que pertenecen al estrato 1 ¿Se podría concluir que el ingreso promedio calculado sobre ese grupo representa el promedio de ingresos para toda la ciudad?
La respuesta es **NO**, la información obtenida a partir de ese estudio no podrá ser generalizada a toda la población dado que sólo se tuvo en cuenta cierto sector de la ciudad y se ignoraron las familias del estrato 2 al 6.


## **4. Unidad de análisis**
Son los elementos u objetos que tiene información sobre el fenómeno que se estudia, es decir aquellos objetos descritos por un conjunto de datos. Los individuos pueden ser personas, pero también pueden ser animales o cosas.
#### Ejemplo
Si se estudia el peso promedio de los estudiantes en una carrera de la universidad, cada uno de los estudiantes son los individuos.


## **5. Variable**
Corresponde a características tomadas de la unidad de análisis. A esta variable se asocia un número o una palabra, carácter, de acuerdo a reglas predeterminadas. Las variables se pueden clasificar según su origen, naturaleza o relación con otras variables :

![[Pasted image 20240722173924.png]]

### **Por su origen**
Una variable es aleatoria cuando los valores resultantes de una medición no se pueden predecir de antemano. Podría decirse que ese valor se desconoce por completo. Si antes de medir, puede predecirse el valor que tendrá la variable, entonces se dice que ésta tiene carácter determinístico.

### **Por su naturaleza**
Si el conjunto de posibles valores que puede tomar constituyen un conjunto de valores finito o infinito numerable o de manera más resumida si proceden de un conteo se denominan discretas. Si la variable puede tomar cualquier valor en un rango infinito no numerable como es el caso de los valores en el campo de los números reales se denominan variables continuas. Estas últimas tambien pueden ser asociadas con los procesos de medición.

### **Por su relación con otras variables**
Si su comportamiento está relacionado o depende de otra variable se califica como dependiente en caso contrario se clasifica como independiente. Relacionado a este concepto está el de causalidad.

Inicialmente nos concentraremos en la clasificación de las variables debido a su naturaleza :

#### **Variables cualitativas**
Sus valores (categorías o modalidades) no se pueden asociar naturalmente a un número, ni se pueden hacer operaciones matemáticas con ellos, pero son de gran utilidad en la clasificación de objetos.
##### **Ejemplo**
- Nacionalidad de un estudiante
- Profesión de una persona
- Defecto de un artículo

#### **Variables cuantitativas**
Toman valores numéricos y se pueden hacer operaciones matemáticas con ellos. Estas se clasifican en dos grupos: continuas y discretas.

#### **Variables continuas**
Las variables continuas pueden tomar cualquier valor real dentro de un intervalo, en general proceden de la medición de características.
##### **Ejemplo**
- Estatura de los estudiantes de este curso,
- Temperaturas registradas al medio día durante el mes pasado,
- Peso de un teléfono celular

#### **Variables discretas**
Las variables discretas sólo toman valores enteros, por lo general proceden el conteo y empiezan por número de …
##### **Ejemplo**
- Número de hijos en una familia,
- Número de carros en un estacionamiento,
- Número de materias matriculas este semestre por un estudiante


### **Escalas de medición**
Es de gran importancia determinar el tipo de escala de medición de una variable, por cuanto con ella se determina el tipo de análisis a realizar y también la manera apropiada de realizar su presentación gráfica.

![[Pasted image 20240722180214.png]]

#### **Nominal**
En las variables con escala de medición nominal, sus valores no se pueden ordenar, es decir que no existe una forma particular para ordenar sus valores.
##### **Ejemplo**
- Profesión (ingeniero, estadístico, administrador,…)  
- Nacionalidad (colombiano, venezolano, ecuatoriano, …)
- Religión (católico, cristiano, evangélico, agnóstico,…)


#### **Ordinal**
En las variables con escala de medición ordinal, sus valores tienen un orden natural o se puede identificar un orden jerárquico entre sus valores o categorías
##### **Ejemplo**
- Nivel educativo (primaria, secundaria, universitario, especialización, maestría, doctorado, postdoctorado),
- Estrato socioeconómico (1, 2, 3, 4, 5, 6)
- Nivel de estrés ( bajo, medio, alto)
- Evaluación de un servicio (excelente, muy bueno, bueno, regular, muy regular)

#### **De intervalo**
A esta escala pertenecen las variables numéricas donde el cero (0) es un valor arbitrario que no implica la ausencia de una característica. Tambien se puede representar la variable con diferentes tipos de escala numérica.

##### **Ejemplo**
Temperatura de cero grados no indica que no hay temperatura, sólo es un valor que toma la variable para esa escala, que puede variar dependiendo la escala que se esté usando (ºC, ºF o ºK)

Esta escala también utilizada en procesos en los que se mide variables como el estrés laboral. Para ello se utilizan valoración de a serie de preguntas por parte del individuo en escala ordinal. La suma de los resultados obtenidos constituye una medición que se traduce nuevamente a escala ordinal y de esta forma valorar el nivel de estrés que padece una persona. Este proceso se denomina operacionalización de una variable cualitativa ordinal en escala de intervalo.

#### **De razón**
En este caso el cero (0) refleja ausencia de la característica, implica la ausencia de una característica.
##### **Ejemplo**
- Número de hijos de una familia
- Salario que recibe un empleado en una empresa
- Ventas mensuales de una empresa comercializadora de alimentos para mascotas

#### **Población**
Es el conjunto de todos los elementos de interés en un estudio, sobre los cuales se desea información y hacia los cuales se extenderán las conclusiones.
##### **Ejemplo**
- Total de estudiantes matriculados en la universidad para el periodo 2024-1
- Total de la población en la ciudad de Cali a diciembre 31 de 2023.
- Compradores de la póliza de seguro obligatorio SOAT para el 2024

#### **Muestra**
Es cualquier subconjunto representativo de la población, sobre el que se realizan los estudios para obtener conclusiones acerca de las características de la población.
##### **Ejemplo**
- 100 estudiantes seleccionados del total de matriculados en la universidad
- 500 personas seleccionadas de la población de Cali.
- Grupo de personas que compran vehículo nuevo durante el mes de diciembre del 2023 en un determinado concesionario.

![[Pasted image 20240722182651.png]]


#### **Parámetro**
Indicador estadístico calculado teniendo en cuenta los elementos de la población se denominan parámetros y son denotados de manera general como θ𝜃.
##### **Ejemplo**
- Edad mínima de los estudiantes matriculados en la universidad (min)
- La proporción de personas con empleo formal en Colombia (p𝑝).
- La esperanza de vida de los colombianos (μ𝜇)

Para el cálculo de estos parámetros se debe contar con la información del ceso correspondiente.


#### **Estimador**
Indicador estadístico calculado teniendo en cuenta los elementos de la muestra, de manera general se representan por θˆ𝜃^.
##### **Ejemplo**
- Edad mínima en una muestra de 100 estudiantes matriculados en la universidad para el 2024-1 (x¯𝑥¯).
- Proporción muestral de personas con empleo de una muestra de 500 personas de la ciudad de Cali (pˆ𝑝^).
- Promedio de la edad de las personas fallecidas durante el 2023 en Colombia

En este caso los valores corresponden a valores obtenidos de una muestra.


## **Tipos de muestreo**
Para seleccionar los datos podemos utilizar muestreos probabilísticos o no probabilísticos que se dividen en diferentes tipos como se indica en el siguiente diagrama

## **Muestreos probabilísticos**
El muestreo probabilístico es un método de selección de la muestra en el que métodos que garantizan una selección aleatoria de los elementos de la muestra, es decir que cada elemento de la población tienen igual probabilidad de ser elegido dentro de una muestra. Esto garantiza además de representatividad de los elementos seleccionados con respecto a las características de la población, independencia entre los valores seleccionados, los cuales permiten características deseables al momento de realizar inferencias sobre los resultados obtenidos

## **Muestreos no probabilísticos**
El muestreo no probabilístico (o muestreo no aleatorio) es la técnica de muestreo donde los elementos son elegidos a juicio del investigador. No se conoce la probabilidad con la que se puede seleccionar a cada individuo.

![[Pasted image 20240722182916.png]]

#### **Reto**
Los muestreos por internet utilizando redes sociales se clasifica dentro de los muestreos no probabilísticos descritos.


---
# **Importación de datos**
La importación de los datos es una de las etapas importantes del proceso para el análisis de datos, que depende del formato y las fuentes generadoras los datos. Esta etapa forma parte del ciclo los de datos.

![](https://centromagis.github.io/metodosySIM1/img/importar.png)
**Figura : 1.5** Ciclo de datos  
Tomado de [Ciencia de Datos y Políticas Públicas](https://datosgcba.github.io/ciencia-de-datos-politicas-publicas/docs/)

  
En **R** se puede importar los datos de diferentes formas:


### **1. Utilizando el menú RStudio**

![](https://centromagis.github.io/metodosySIM1/img/importar_datos.png)

|   |   |   |
|---|---|---|
|**formato .txt**|_File/Import Dataset/From Text (base)_|formato texto separado por espacios|
|**formato .csv**|_File/Import Dataset/From text (base)_|formato csv separado por ; o por ,|
|**formato .xlsx**|_File/Import Dataset/ From Excel_|formato excel|
|**formato .dat**|_File/Import Dataset/ From SPSS_|formato SPSS - programa estadístico|
|**formato .sas7bdat**|_File/Import Dataset/ From SAS_|formato SAS - programa estadístico|
|**formato .dta**|_File/Import Dataset/ From Stata_|formato STATA - programa estadístico|
||||

### **Nota**
Los anteriores caso implican que tengamos la base de datos descargada en una carpeta de nuestro PC

  
### **2. Utilizando API y token desde un repositorio externo**
Podemos importar la base de datos de un repositorio que maneje API a través de un token. En este caso debemos solicitar el token e instalar el paquete `RSocrata`

### **Ejemplo**
El siguiente código importa la base de datos de la Secretaria de Salud correspondiente a las personas reportadas con Covid-19 para el territorio Colombiano. Para ello se debe solicitar en la plataforma de Datos Abiertos Colombia un token y realizar la siguiente solicitud
```R
install.packages("RSocrata", dependencies = TRUE)   
library(RSocrata)    # llamado de libreria
token <- "zxMsD6eXc0zlEMryRGW87Hwrz"  # token
Colombia <- read.socrata("https://www.datos.gov.co/resource/gt2j-8ykr.json", app_token = token) # lectura 
```

Este proceso tarde unos minutos pues la base es grande

Para guardar el archivo en una carpeta `data`, se recomienda el formato `RDS` por ocupar menos espacio. En este caso se guarda el archivo descargado con el nombre de _Colombia.RDS_ en la carpeta _data/_

```R
saveRDS(Colombia, file = "data/Colombia.RDS") 
```
  

### **4. Desde un paquete de R instalado**
Es psosible trabajar con una `dataset` disponible en los paquetes de R. Para ello solo utilizamos la función `data()`


### **Ejemplo**
```R
data(iris)  
data(cars) 
data(vivienda_faltantes)  
```
  
### **Nota**
se tiene tengo un archivo en un equipo, puede utiliza la función: `file.choose()` , para conocer la ruta donde esta el archivo y luego se copia la ruta obtenida con Ctrl+C,

En este caso se genera la ruta “data/Colombia.RDS”, como resultado de ejecutar la función anterior y ubicar el archivo a importar. (`Colombia<- readRDS("data/Colombia23.RDS")`)

R permite importar datos en diferentes formatos :
**Tabla 1.1** : formatos de datos importados en R

|Formato|libreria R|código|
|:--|:--|:--|
|.texto|`library(readr)`|`datos <- read_delim("ruta_del_archivo/datos.txt", delim = ",")`|
|.csv|`library(readr)`|`datos <- read.csv("datos.csv")`|
|.xlsx|`library(readxl)`|`datos <- read_excel("datos.xlsx", sheet = "hoja1")`|
|.json|`library(jsonlite)`|`datos <- fromJSON("datos.json")`|
|.stata|`library(haven)`|`datos_stata <- read_dta("datos_stata.dta")`|
|.spss|`library(haven)`|`datos_spss <- read_sav("datos_spss.sav")`|
|.sas|`library(haven)`|`datos_sas <- read_sas("datos_sas.sas7bdat")`|


---
# **Ordenar y limpiar los datos**
Una de las tareas más importante al realizar un proyecto de Ciencia de Datos corresponde a la preparación de los datos (Limpieza de datos o data cleaning) que posteriormente va a permitir el modelamiento adecuado de los datos.

![](https://centromagis.github.io/metodosySIM1/img/ordenar.png)

Este ciclo comprende :

- Importación de los datos - ya tratado -
- Fusión de datos
- Datos faltantes
- Estandarización
- Normalización
- Elinación de registros duplicados
- Verificación y enrequecimiento
- Exportación de los datos

Al importar una base de datos que está conformada por una matriz con nn filas o registros y mm columnas o variables se presentan problemas relacionados con:

- Datos faltantes (NA)
- Reemplazar los datos faltantes - imputación
- Datos extraños o atípicos
- Necesidad de estandarizar los valores con el fin varias variables sean comparables (una misma escala)
- Construir nuevas variables a partir de las contenidas en la base
- Cambiar el formato de una variable - formato corto y formato largo -
- Aumentar los registros contenidos en dos bases - adicionar registros -
- Agregar variables contenidas en dos bases

A contunuación se presentan algunos de estos temas que permiten tratar y dejar lista la base de datos de interes para iniciar el análisis de datos

# **Tratamiento de datos faltantes**
El tratamiento de datos faltantes es un aspecto crítico en Ciencia de Datos, ya que ellos pueden afectar de manera significativa la calidad y validez de los análisis y modelos que realicemos. Acontinuación se presentan algunas estrategias comunes para manejar los datos faltantes:


### **1. Eliminacion de los registros o filas**
Si los **datos faltantes** son pocos en comparación con el tamaño total del conjunto de datos, una estrategia es eliminar los registros o filas que contienen datos faltantes. Sin embargo, esta estrategia puede llevar a una pérdida de información si los datos faltantes son sistemáticos o si se eliminan muchas observaciones en comparación con el tamaño de la base de datos.


### **Ejemplo**
A partir de la base de datos `rotacionNA` contenida en `paqueteMETODOS`, se plantera examinar una muestra de ella de tamaño `1000 x 25` que se puede obtener con el siguiente código :

```R
library(paqueteMETODOS) # carga paqueteMETODOS
library(dplyr)          # carga paqiete dplyr 
data("rotacionNA")      # carga data set rotacionNA del paqueteMETODOS
set.seed(123)           # fija semilla para numeros aleatorios
rotacionNA<-sample_n(rotacionNA, 1000) # toma una muestra de tamaño 1000 de la data
datosNA <- rotacionNA  # copia el contenido a datosNA
str(datosNA)  # explora contenido de datosNA
```

Con la función `str()` se obtiene una visualización del tamaño de la base de datos, las variables que la conforman y el tipo de variables y una muesrta de los primeros valores.

Ahora para visualizar que variables y con que frecuencia se presentan los datos faltantes o `NA` utilizamos el siguiente código
```R
library(dplyr)
faltantes <- colSums(is.na(datosNA)) %>%
                 as.data.frame() 

faltantes
```

La función `colSums(is.na(datosNA))` totaliza el número total de datos faltantes por variable para la data `datosNA`

```R
# install.packages("naniar")
library(naniar)
gg_miss_var(datosNA) # grafico de datos faltantes
```
![[Pasted image 20240730183331.png]]
En esta gráfica podemos visualizar que las viables : Viaje de Negocio, Estado Civil, Rotacion, Genero, Departamento y Horas Extras presentan datos faltantes. Para ello se utiliza la función `gg_miss_var(datosNA)`

Otra forma de detectar y representar gráficamente los datos faltantes es utilizando la función `md.pattern(datosNA, rotate.names = TRUE)` del paquete `mice`
```R
# install.packages("VIM")
VIM::aggr(datosNA, cex.axis = 0.5, cex.lab= 0.8)  # graficos de datos faltantes
```
![[Pasted image 20240730183352.png]]

En este caso se observa una primera fila que represnta los registros tienen informaciçon completa (sin datos faltantes). Las filas restantes donde aparecen cuadrados en rojo, representan los datos faltantes para las variables Viaje de Negocio, Estado Civil, Rotacion, Genero, Departamento y Horas Extras .

Detectados la proporción de datos faltantes procederemos como una primera estrategia a eliminarlos por completo


#### **Eliminación de datos faltantes**
La función : `na.omit()` , permite elimitar todos los registros contenidos en la base de datos que contenga datos faltantes (NA)

- **Verifique que se han eliminado los datos faltantes**
```R
# install.packages("VIM")
datosSINA <- na.omit(datosNA)  # elimina todos los valores con  NA
VIM::aggr(datosSINA, cex.axis = 0.4, cex.lab= 0.8)
cat("dimensión dataSINA : ", dim(datosSINA))
```
Este proceso elimina 100 de los registros, dejando una data de `900 x 25` .


### **2. Tratamiento de datos faltantes como una categoría**
En el caso de variables categóricas o cualitativas sus valores faltantes se pueden encontrar a partir del modelamiento la sub-base con registros completos

los datos faltantes pueden tener un significado propio y no deben ser imputados ni eliminados. En lugar de eso, puedes considerar tratar los datos faltantes como una categoría adicional en el análisis o modelo (faltante) .

```R
datosNA <- rotacionNA
datosNA$Otro_motivo <- 0
datosNA$faltante[is.na(datosNA$`Viaje de Negocios`)] <- 1 
VIM::aggr(datosNA, cex.axis = 0.4, cex.lab= 0.8)
```

![[Pasted image 20240730183453.png]]

## **2. Imputación de valores**
Si no se desea eliminar los registros que contiene datos faltantes, dado que se puede perder un gran porcentaje de la información, entoces se recurre a reemplazar estos valores, primero calculado el valor por el cual se debe reemplazar (**imputación de datos**).

Para realizar este procedimiento se tienen varias alternativas, cambiando los datos faltantes por :
- cero
- la media
- mediana
- por el valor de un registro completo semejante al del dato faltante - tecnicas avanzadas de imputación

### **Ejemplo**
### **Caso imputación por cero**
En el caso de la data `rotacionNA`, es posible que los empleados al ser interrogados, entendieron que no debian responder la pregunta: **Horas Extras**, cuando no trabajan horas por fuera de su jornada laboral.

En otros casos es posible que se trate de un dato faltante real -no respuesta - y se deba reeplazar por un valor que lo represente.

El caso de reemplazar los `NA` por **cero** en la variable `Horas_Extra`, se procede la siguiente forma:

```R
datosNA$Años_Experiencia[is.na(datosNA$Años_Experiencia)] <- 0
```
![[Pasted image 20240730183531.png]]

### **Caso reemplazo por la media**
En el caso de reemplazar el `NA` por el valor correspondiente a la media se asigna este valor de la siguiente manera:

![[Pasted image 20240730183656.png]]
```
media Años_Experiencia :  12
```


#### **Caso reemplazo por la mediana**
En el caso de reemplazar el NA por el valor correspondiente a la mediana se asigna este valor de la siguiente manera:

```R
datosNA <- rotacionNA
# Calcula la mediana de la variable "Años_Experiencia"
mediana_Años_Experiencia <- median(datosNA$Años_Experiencia, na.rm = TRUE) %>%
                    round(,0)

datosNA$Años_Experiencia[is.na(datosNA$Años_Experiencia)] <- mediana_Años_Experiencia
VIM::aggr(datosNA, cex.axis = 0.4, cex.lab= 0.8)
```

![](https://centromagis.github.io/metodosySIM1/recurso13_files/figure-html/unnamed-chunk-10-1.png)

Show

```
mediana Años_Experiencia :  10
```

### **Caso reemplazo por la moda**
En el caso de la variable piso, que corresponde cualitativa de escala ordinal, si se desea reemplazar por la moda a los datos faltantes procedemos de la siguiente forma:

```R
# install.packages("DescTools")
library(DescTools)
moda_Estado_Civil <- Mode(datosNA$Estado_Civil, na.rm = TRUE)
datosNA$Estado_Civil[is.na(datosNA$Estado_Civil)] <- moda_Estado_Civil
VIM::aggr(datosNA, cex.axis = 0.5, cex.lab= 0.8)
```

![](https://centromagis.github.io/metodosySIM1/recurso13_files/figure-html/unnamed-chunk-11-1.png)

```R
cat("moda Estado_Civil : ", moda_Estado_Civil)

OUTPUT: moda Estado_Civil :  Casado
```


# **Fusión de datos**
Una de las necesidades importante en el manejo de bases de datos la conforma el agregar mas registros o filas a una base de datos o de agregar nuevas variables.

Esta etapa implica combinar datos provenientes de múltiples fuentes en una única estructura de datos, permitiendo un análisis más completo y holístico. La fusión de datos se utiliza comúnmente cuando se trabaja con conjuntos de datos que comparten una o más variables en común, como identificadores únicos, fechas o categorías.

En **R**, uno de los paquetes más utilizados para realizar la fusión de datos es el paquete `dplyr`, que forma parte del grupo de paquetes agrupados en `tidyverse`

En este caso se presentan dos casos :
- Adicionar registros a una base de datos
- Adicionar variables a una base de datos

## **Adicionar registros**
![](https://centromagis.github.io/metodosySIM1/img/mezcla12.png)


### **Ejemplo**
Para ilustrar el primer caso tomaremos una muestras pequeñas de la base rotacion contenida en paqueteMETODOS

### **data1**
Esta base contiene información de tres variables, correspondientes a 6 personas

```R
library(paqueteMETODOS)
data("rotacion")
id = 1:1470
data= data.frame(id, rotacion)

data1 = data[1:6,c(2,3,4,5)]
data1
```

```
  Rotación Edad Viaje.de.Negocios Departamento
1       Si   41         Raramente       Ventas
2       No   49    Frecuentemente          IyD
3       Si   37         Raramente          IyD
4       No   33    Frecuentemente          IyD
5       No   27         Raramente          IyD
6       No   32    Frecuentemente          IyD
```

### **data2**
Esta segunda base contiene las mismas tres variables pero que corresponden a otras 6 personas y deseamos juntar todos los registros ( en total 12) en una sola base de datos

```R
library(paqueteMETODOS)
data("rotacion")
id = 1:1470
data= data.frame(id, rotacion)

data2 = data[7:12,c(2,3,4,5)]
data2
```

```
   Rotación Edad Viaje.de.Negocios Departamento
7        No   59         Raramente          IyD
8        No   30         Raramente          IyD
9        No   38    Frecuentemente          IyD
10       No   36         Raramente          IyD
11       No   35         Raramente          IyD
12       No   29         Raramente          IyD
```

Para unir estas dos base utilizamos la función `rbind()` del paquete `dplyr`.

```R
library(dplyr)
data20 = rbind(data1,data2)
data20
```

```
   Rotación Edad Viaje.de.Negocios Departamento
1        Si   41         Raramente       Ventas
2        No   49    Frecuentemente          IyD
3        Si   37         Raramente          IyD
4        No   33    Frecuentemente          IyD
5        No   27         Raramente          IyD
6        No   32    Frecuentemente          IyD
7        No   59         Raramente          IyD
8        No   30         Raramente          IyD
9        No   38    Frecuentemente          IyD
10       No   36         Raramente          IyD
11       No   35         Raramente          IyD
12       No   29         Raramente          IyD
```

  
### **Adicionar variables**
En la adición de variables se presentan dos casos El primero corresponde a la unión de dos o más columnas contenidas en bases diferentes pero que deben estar ordenadas en la misma forma para que coincidan los registros.

En el segundo caso las bases de datos deben contener una llave que permita indexar sus registros.

### **Caso 1**
![](https://centromagis.github.io/metodosySIM1/img/mezcla34.png)


### **Ejemplo**
Para ilustrar este caso tomaremos una muestra de la data `rotacion` contenida en `paqueteMET` para conformar las bases `data3`, `data4` y `data5`:


### **data3**
Conformada por 10 registros y tres variables dentro de las cuales esta id que sirve en este caso para verificar que los registros están en un mismo orden.

```
   id Rotación Edad
1   1       Si   41
2   2       No   49
3   3       Si   37
4   4       No   33
5   5       No   27
6   6       No   32
7   7       No   59
8   8       No   30
9   9       No   38
10 10       No   36
```

  
### **data4**
data4 contiene además del identificador otras dos variables

```
   id Viaje.de.Negocios Departamento
1   1         Raramente       Ventas
2   2    Frecuentemente          IyD
3   3         Raramente          IyD
4   4    Frecuentemente          IyD
5   5         Raramente          IyD
6   6    Frecuentemente          IyD
7   7         Raramente          IyD
8   8         Raramente          IyD
9   9    Frecuentemente          IyD
10 10         Raramente          IyD
```


En este caso se tienen las funciones :
- `cbind()` Utilizada para combinar dos o mas conjuntos por columnas, agregando un conjunto de columnas. Es decir pegar dos datas que presentan el mismo orden de registros
- 
```R
cbind(data3, data4[,2:3])
```

```
   id Rotación Edad Viaje.de.Negocios Departamento
1   1       Si   41         Raramente       Ventas
2   2       No   49    Frecuentemente          IyD
3   3       Si   37         Raramente          IyD
4   4       No   33    Frecuentemente          IyD
5   5       No   27         Raramente          IyD
6   6       No   32    Frecuentemente          IyD
7   7       No   59         Raramente          IyD
8   8       No   30         Raramente          IyD
9   9       No   38    Frecuentemente          IyD
10 10       No   36         Raramente          IyD
```


### **Caso 2**
![](https://centromagis.github.io/metodosySIM1/img/mezcla35.png)

- `merge()`. Se utiliza para combinar conjuntos de datos por columnas clave específicas, independientemente del número de filas.


### **data5**

```
   id Viaje.de.Negocios Departamento
3   3         Raramente          IyD
4   4    Frecuentemente          IyD
5   5         Raramente          IyD
6   6    Frecuentemente          IyD
7   7         Raramente          IyD
8   8         Raramente          IyD
9   9    Frecuentemente          IyD
10 10         Raramente          IyD
11 11         Raramente          IyD
12 12         Raramente          IyD
```

```R
merge(data3, data5, by = "id", all = TRUE)
```

```
   id Rotación Edad Viaje.de.Negocios Departamento
1   1       Si   41              <NA>         <NA>
2   2       No   49              <NA>         <NA>
3   3       Si   37         Raramente          IyD
4   4       No   33    Frecuentemente          IyD
5   5       No   27         Raramente          IyD
6   6       No   32    Frecuentemente          IyD
7   7       No   59         Raramente          IyD
8   8       No   30         Raramente          IyD
9   9       No   38    Frecuentemente          IyD
10 10       No   36         Raramente          IyD
11 11     <NA>   NA         Raramente          IyD
12 12     <NA>   NA         Raramente          IyD
```

  
  

### **Nota**
En el caso de unir columnas mediante la función `cbind()` , se combinan dos base de datos (`data3` y `data4`) de igual número de filas y que corresponde información que corresponde a las mismas personas. Para que no parezca la variable id repetida se quita de data4 dejando solo las columnas 2 a 3 - `data4[, 2:3]` - .

Para el caso de la función `merge()` , se requiere tener un indice que identifique cada registro y por tanto no es necesario que los registros en las bases a unir se encuentren ordenadas. Para ello utilizamos las bases data3 y data5. En ellas se puede notar que la primera presenta los registros de las personas con id del 1 al 12, mientras que la data5 los registros correspondientes a las personas con id del 3 al 14. Es por esta razón que se toma como base la data3 y sobre ella se agregan los registros que coincidan al comparar su id con los de la `data5`. Quedando vacíos los registros de las personas con id 1 y 2.



# **Transformación de datos**
Una de las etapas importantes dentro del ciclo de datos corresponde a la transformación de las variables. Dentro de los procesos más importantes en este aspecto están :
- Construcción de nuevas variables
- Estantarización de variables
- Normalización de variables
Para presentar estos procesos se utiliza la data `rotación` contenida en `paqueteMETODOS`, iniciando con su importación y descripción:

```R
library(dplyr)
data(rotacion)
set.seed(123)
datos <- sample_n(rotacion, 1000)
# variables <- c("Edad", "Antigüedad", "Antigüedad_Cargo", "Años_ultima_promoción", "Años_acargo_con_mismo_jefe")
datos = datos[, c(2,18,21,22,23,24)] # se seleccionan variables de interes para facilitar su visualizacion
str(datos) # Muestra los datos originales
```

```
tibble [1,000 × 6] (S3: tbl_df/tbl/data.frame)
 $ Edad                      : num [1:1000] 24 34 46 24 45 39 30 46 34 34 ...
 $ Años_Experiencia          : num [1:1000] 6 10 24 4 22 21 6 12 6 15 ...
 $ Antigüedad                : num [1:1000] 5 10 24 2 20 19 6 9 5 15 ...
 $ Antigüedad_Cargo          : num [1:1000] 3 7 13 2 8 9 4 8 0 14 ...
 $ Años_ultima_promoción     : num [1:1000] 1 5 15 2 11 15 1 4 1 0 ...
 $ Años_acargo_con_mismo_jefe: num [1:1000] 4 7 7 0 8 2 1 7 2 7 ...
```

## **Construcción de variables**
Es usual que se requiera construir variables a partir de las variables existente en la data. Este proceso se puede realizar de dos formas:
- Utilizando la transformación directamente
- Utilizando la función `mutate` del paquete `dplyr`

### **Ejemplo**
Supongamos que se desea contruir un indicador de razón que involucre las variables Años de Experiencia y Antigüedad

![[Pasted image 20240730184924.png]]

Este indicador podrá suministra información sobre si el empleado ha sido contratado con experiencia previa o si por el contrario se ha adquirido su experiencia en la empresa.

**Transformación directa**

```R
datos$Indicador1 = datos$Antigüedad/datos$Años_Experiencia
str(datos) 
```

```
tibble [1,000 × 7] (S3: tbl_df/tbl/data.frame)
 $ Edad                      : num [1:1000] 24 34 46 24 45 39 30 46 34 34 ...
 $ Años_Experiencia          : num [1:1000] 6 10 24 4 22 21 6 12 6 15 ...
 $ Antigüedad                : num [1:1000] 5 10 24 2 20 19 6 9 5 15 ...
 $ Antigüedad_Cargo          : num [1:1000] 3 7 13 2 8 9 4 8 0 14 ...
 $ Años_ultima_promoción     : num [1:1000] 1 5 15 2 11 15 1 4 1 0 ...
 $ Años_acargo_con_mismo_jefe: num [1:1000] 4 7 7 0 8 2 1 7 2 7 ...
 $ Indicador1                : num [1:1000] 0.833 1 1 0.5 0.909 ...
```

**Transformacion utilizando la función mutate del paquete dplyr**
```R
datos <- mutate(datos, Indicador2 = Antigüedad / Años_Experiencia)
str(datos) # Muestra los datos originales
```

Otra de las transformaciones importantes en el análisis de datos corresponde a la **estandarización** y la **normalización** de las variables, las cuales permiten el cambio de escala, permitiendo realizar comparaciones.


## **Estandarización**
Consiste en restar a la media de una variable a todos sus valores y dividiendo este resultado por su desviación estándar. Esta transformación hace que la nueva variable tenga media cero y varianza uno. El procedimiento permite ajustar la escala de varias variables y se aplica cuando estas presentan distribuciones simétricas.

![[Pasted image 20240730185013.png]]

### **Ejemplo**

```R
datos <- sample_n(rotacion, 1000)
datos$Edad_estandarizada1 = (datos$Edad - mean(datos$Edad))/sd(datos$Edad)
datos$Edad_estandarizada2 = scale(datos$Edad)
str(datos[,c(2,25,26)]) 
```

```
tibble [1,000 × 3] (S3: tbl_df/tbl/data.frame)
 $ Edad               : num [1:1000] 40 54 40 55 34 30 46 26 36 45 ...
 $ Edad_estandarizada1: num [1:1000] 0.321 1.87 0.321 1.981 -0.343 ...
 $ Edad_estandarizada2: num [1:1000, 1] 0.321 1.87 0.321 1.981 -0.343 ...
  ..- attr(*, "scaled:center")= num 37.1
  ..- attr(*, "scaled:scale")= num 9.04
```

```r
summarytools::descr(datos[,c(2,25,26)])
```

```
Descriptive Statistics  

                       Edad    Edad_estandarizada1    Edad_estandarizada2
----------------- --------- ---------------------- ----------------------
             Mean     37.10                   0.00                   0.00
          Std.Dev      9.04                   1.00                   1.00
              Min     18.00                  -2.11                  -2.11
               Q1     31.00                  -0.68                  -0.68
           Median     36.00                  -0.12                  -0.12
               Q3     43.00                   0.65                   0.65
              Max     60.00                   2.53                   2.53
              MAD      8.90                   0.98                   0.98
              IQR     12.00                   1.33                   1.33
               CV      0.24   -5784092685267730.00   -5784092685267730.00
         Skewness      0.36                   0.36                   0.36
      SE.Skewness      0.08                   0.08                   0.08
         Kurtosis     -0.40                  -0.40                  -0.40
          N.Valid   1000.00                1000.00                1000.00
        Pct.Valid    100.00                 100.00                 100.00
```

La estandarización en el contexto de la limpieza y ajuste de datos en ciencia de datos se refiere al proceso de transformar las variables para que tengan una media de cero y una desviación estándar de uno. Este paso es comúnmente realizado para asegurar que las variables tengan escalas comparables y para facilitar la interpretación y el análisis de los modelos. Este procedimiento también se conoce con los nombres de **z-score normalization** o **z-score scaling**.


## **Normalización**
Esta transformación escala los valores de una variable a un rango específico, por defecto el rango es [0,1]. Se presenta cuando las variables no siguen una distribución normal, haciendo que las variable tengan el mismo rango. Tambien se conoce con el nombre de **min-max scaling**.

**Normalización manual**
Para realizar la transformación de manera manual debemos de contar con :
- valor mínimo de la variable
- valor máximo de la variable

![[Pasted image 20240730185151.png]]

### **Ejemplo**
**Normalización utilizando la función rescale del paquete scales**

```r
datos <- sample_n(rotacion, 1000)

datos$Edad_normalizada1 = (datos$Edad - min(datos$Edad))/(max(datos$Edad)-min(datos$Edad))

library(scales)
datos$Edad_normalizada2 = rescale(datos$Edad, to =c(0,1))
```

```
tibble [1,000 × 3] (S3: tbl_df/tbl/data.frame)
 $ Edad             : num [1:1000] 20 37 47 49 33 30 41 36 29 38 ...
 $ Edad_normalizada1: num [1:1000] 0.0476 0.4524 0.6905 0.7381 0.3571 ...
 $ Edad_normalizada2: num [1:1000] 0.0476 0.4524 0.6905 0.7381 0.3571 ...
```
