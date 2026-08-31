
A continuación, observaremos la primera parte de la descripción de un proyecto realizado en el Sector salud; presentado por el experto Camilo Rocha; doctor en informática e investigador de la Alianza CAOBA, quien además es en la actualidad el Decano de la Facultad de Ingeniería y Ciencias en la Universidad Javeriana en Cali.


# Parte 1: Contexto

## ¿Cuál es el problema que quiere resolver el proyecto presentado?

En este proyecto queríamos utilizar analítica de datos para entender el  
comportamiento de varias dinámicas asociadas al sector salud en relación con la llegada de la pandemia a Colombia, en particular estamos interesados en saber qué sucedía con la ocupación de  
centros de salud, dinámicas de vacunación en niños por ejemplo y otras actividades que se podían ver entorpecidas por la ocupación de centros de salud.

## ¿Por qué utilizar la ciencia de datos para resolver este problema?

Este es un problema grueso. Nosotros en el equipo de Cali nos centramos en las dinámicas de la propagación del virus y la afectación de estas dinámicas en el sistema de salud. Teníamos datos de varias IPS, teníamos datos de muchos pacientes del nivel de digamos y de los síntomas y síntomas que tenían y cómo esto se estaba afectando la calidad de la atención de los centros de salud. Entonces teníamos fuentes de datos, en principio disponibles de varios actores y queríamos llegar a dos conclusiones por eso principalmente: 
- Primero cuáles eran las dinámicas de propagación del virus
- Segundo cómo estas dinámicas podrían entrar a sugerir a quienes planean cómo utilizar estos recursos a asignar en diferentes centros de salud las personas que estaban contagiadas y principalmente con afectaciones graves de salud.

## ¿Se anticiparon algunos retos para la planeación y desarrollo del proyecto?

SÍ, efectivamente anticipamos algunos retos, al final demos cuenta que no anticipamos suficiente. ¿Qué retos anticipamos? 

- Primero la variedad y de heterogeneidad de los datos que recibimos, pues tenemos datos por ejemplo alcaldía de Cali en caso del proyecto propio nuestro, teníamos datos de el sector central de la salud y esos datos pues no siempre coincidían, entonces allí nosotros estábamos atentos a tomar medidas para poder utilizar sus datos de manera conjunta, esto es un ejemplo porque tenemos más fuentes de datos. Lo que no anticipamos, que para nosotros un reto finalmente, es que había mucha dificultad para conseguir los datos particulares en la ciudad de Cali. Tuvimos acceso a ellos gracias a que cuando era miembro del equipo estaba haciendo digamos el consultor de un grupo de interés de la alcaldía con la cual tuvimos un acceso a esos datos. Ese fue un reto muy grande durante todo el proyecto tiene buena calidad de datos, predicciones y entender las dinámicas que finalmente debíamos entender en la ciudad.

# Parte 2: Experiencia

## ¿Cómo estructuraron el proyecto?
Este proyecto surge en el marco de una convocatoria a nivel nacional de Ministerio de Ciencias (Min Ciencias) cuando llegó la pandemia, Min Ciencias  abrió una convocatoria denominada, "Min Cienciaton" con la cual quería dar respuesta a algunas de las dificultades desde la ciencia que traía consigo la pandemia. Entonces el centro de CAOBA preparó en tiempo récord una propuesta en la cual estamos articuladas varias universidades. Dentro de esta propuesta teníamos cinco proyectos, del cual les estoy contando es uno de esos cinco proyectos: 

## ¿Qué tipo de estructuración se hizo? 
Pues nosotros nos preocupamos mucho por la calidad de los datos, por un lado entonces tenemos que contar con personas que fueran expertas en revisar los datos, en consolidarlos y en generar unos conjuntos de pruebas suficientemente buenos como para poder aplicar las técnicas de analítica de datos. En este equipo propio de este proyecto estamos involucrados dos profesores de javeriana Cali, teníamos una persona experta en salud de Bogotá, teníamos científicos de datos apoyándonos, uno dentro del centro de gerencia y dos tienen estudiantes de maestría aquí, en javieriana Cali. Nosotros teníamos reuniones semanales de seguimiento, no solamente al interior de ese equipo, sino en conjunto con los demás proyectos que tenían las demás universidades y esta dinámica de aproximadamente 9 a 10 meses. Tuvimos una estructuración por etapas y yo quiero mencionar las más importantes en orden secuencial:

1. Primero toda esta cuestión que tuvo que ver con la obtención de los datos, entonces una vez tuvimos los datos nosotros nos planteamos la pregunta investigación. Posteriormente comenzamos a ver qué  técnicas cómo utilizar y qué librerías están disponibles para no hacer todo desde cero.
2. Entonces vemos una segunda etapa digamos la segunda etapa  exploración de herramientas y técnicas que nos podrían llevar a encontrar respuestas a las preguntas que nos planteamos originalmente. Con ello hicimos una escogencia de técnicas y herramientas que finamente utilizamos en el proyecto. 

En paralelo a  nosotros proyectos estaban haciendo básicamente lo mismo.
3. Al final tuve una etapa muy interesante que fue una etapa de consolidación de los proyectos en una sola plataforma y ahí tenemos un equipo liderado por profesores de tu universidad que se encargó de construir los tableros de control en donde se pegaban todos estos modelos y en tiempo real los interesados podían comenzar a consultar los resultados de estas clasificaciones, predicciones y dinámicas que logramos con analítica de datos. 

## ¿Qué dificultades o retos encontraron durante la ejecución del proyecto?
Pues he mencionado la dependencia tan grande que hay de contar con fuentes de datos confiables y disponibles cuando uno necesita y quiero ahondar un poco en este tema porque considero importante para cualquier proyecto analítica, que las reglas de juego estén claras a la  
hora de contar y hacer disponible los datos dentro del proyecto. En particular quiero referirme un modelo de gobernanza que generalmente ayuda a resolver esos problemas. Nosotros no teníamos claro que se necesitaba un modelo gobernanza porque en principio quienes iban a suministrar los datos eran todos agentes del estado. Finalmente nos demos cuenta que eso no funcionaba como todos creímos mientras tenemos que involucrar al ministerio de  
salud, al instituto nacional de salud a la alcaldía local y alguna forma de llegar a un acuerdo en el cual nosotros podemos hacer uso de esos datos bajo ciertas restricciones de confidencialidad.

## ¿Cuáles fueron los resultados obtenidos en este proyecto?
Bueno a nivel de usuario final lo que nosotros logramos fue suministrarle a la convocatoria a través pues de CAOBA fue un tablero en el cual geográficamente se identificaban los casos que se han reportado en sistema de salud dentro la ciudad de Cali y con base en eso podemos hacer predicciones de en dónde y cuándo podrían surgir nuevos casos en la ciudad. 

Esto se hizo haciendo valga la redundancia una Teselación de la ciudad en hexágonos con una librería pública que ha suministrado Uber desde hace varios años y allí nosotros pues aplicando a las técnicas de predicción lográbamos decir cosas por el estilo de lo siguiente: 
- Dentro de 45 días es posible que haya un brote en tal zona en la ciudad con una probabilidad, medida pues con base en lo que hacían los nuevos.
- También logramos con base en eso tratar de predecir cuáles eran un centro de salud más golpeados por estas olas de personas que llegarían a solicitar ayuda médica
- No logramos llegar al punto de decir con qué nivel de gravedad, bajo medio, alto, llegarían las instrucciones pero la idea era que ese proyecto se tuviera se pudiera continuar al interior del ministerio de salud para llegar a ese nivel de detalle
- A nivel técnico nos dejó bastantes aprendizajes: primero trabajar con datos de los referenciados y temporalmente marcados era un reto de principio, entonces logramos aplicar técnicas de **analítica de datos de redes complejas** para poder hacer esta predicción y estas causalidades en tiempo y espacio que finalmente dan soporte a los modelos.

## ¿Cuáles fueron los impactos del proyecto en cuanto a aspectos técnicos, éticos, económicos o ambientales?
Bueno a nivel de lo que estaba escrito en la convocatoria del contrato que nosotros nos comprometimos a cumplir, se lograron las principales metas que nos habíamos trazado, que era **entregar modelos de análisis dinámico y de predicción de comportamientos para las personas que viven en Cali en relación con la pandemia** 

### ¿Qué sucedió después de que entregamos el proyecto? 
Esto se entregó al Ministerio y la idea era que este proyecto continuara su desarrollo internamente, esto también tuvo participación del Instituto Nacional de Salud y de alcaldía de Cali como les mencioné anteriormente y hasta allí llegamos. Nosotros tenemos la expectativa y la firme creencia de que esto se seguirá haciendo y que ha sido útil para aquellas personas que toman decisiones, pueden hacerlo con mayor certeza y efectividad. 

A nivel ético creo que es un ejemplo para mostrar la forma en que trabajamos cuando uno se enfrenta a datos que tienen información de personas que son sensibles como su estado de salud, pues normalmente uno tiene que ser cuidadoso con la forma en que los utiliza y la forma en que los comparten, entonces hay aplicamos también técnicas de administración de los datos para que ese compromiso que teníamos con la alcadía de usar los datos, pero no filtrar los por así decirlo a otras entidades lo logramos con esas técnicas de administración, desde el punto de vista ético es un aprendizaje bastante importante y nos dio nuevos resultados para seguir adelante en proyectos similares en donde teníamos que ser cuidadosos con la información de los usuarios, con la información de los pacientes en este caso concreto.



Para el proyecto se debe presentar de manera concisa la siguiente información: 
a. Cuando y donde se hizo el proyecto 
b. Objetivo del mismo 
c. Etapas realizadas: aquí es fundamental que se pueda mostrar cómo se usa la ciencia de datos en el proyecto. Por ejemplo, indicar qué tipo de técnicas se aplican. 
d. Qué resultados se obtienen: ser precisos y presentar resultados cuantitativos. 
e. Adicionalmente se debe analizar el impacto de cada proyecto teniendo en cuenta diversos grupos interesados (stakeholders. Por ejemplo: la empresa, los clientes, la competencia, la sociedad en general, etc.) y diversos tipos de impacto (técnico, económico, social, ambiental, ético, etc.). 

Incluso si la información disponible no describe de manera explícita estos impactos, se debe deducir, a partir de dicha información, cuáles son los impactos esperables del proyecto.

