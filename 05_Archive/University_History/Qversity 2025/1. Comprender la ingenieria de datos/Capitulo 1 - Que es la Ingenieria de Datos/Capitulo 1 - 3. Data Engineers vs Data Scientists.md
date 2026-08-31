---
tags:
  - Qversity
  - IngenieriaDatos
  - DataEngineer
  - DataScientist
---

Anteriormente, nos familiarizamos en el **Flujo de Datos en una Organización**, centrándonos en un **Ingeniero de Datos** y mencionando rápidamente al **Científico de Datos**

Para ello, aclaremos en qué aspectos son diferentes y en cuáles se pueden comparar ambos.

**Ingeniero de Datos**
![[Pasted image 20250513150252.png]]
- Se centran en la **primera parte del flujo de datos**. 
- Su función es **ingerir y almacenar los datos** para que sean **fácilmente accesibles** y estén **listos para ser analizados**

**Científico de Datos
![[Pasted image 20250513150305.png]]
- Intervienen en el **resto del flujo de trabajo**
- **Preparan los datos según sus necesidades de análisis**, los **exploran**, *construyen visualizaciones y *ejecutan experimentos* o *construyen modelos predictivos*

#### Resumen clave:

| Aspecto                  | Ingeniero de Datos                                                                           | Científico de Datos                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Enfoque Principal**    | Construcción y mantenimiento de la infraestructura de datos                                  | Análisis, interpretación y modelado de los datos                       |
| **Tareas Clave**         | Crear pipelines, optimizar bases de datos, asegurar la calidad de los datos                  | Explorar datos, construir modelos predictivos, generar insights        |
| **Herramientas Comunes** | SQL, ETL/ELT, plataformas cloud (AWS, Azure, GCP), lenguajes de programación (Python, Scala) | Python (Pandas, NumPy, Scikit-learn), R, herramientas de visualización |
| **Salida Principal**     | Datos accesibles, confiables y bien estructurados                                            | Insights, modelos predictivos, visualizaciones                         |
| **Pregunta Típica**      | ¿Cómo podemos obtener y preparar estos datos?                                                | ¿Qué patrones o predicciones podemos obtener de estos datos?           |

### Ejemplo de Colaboración entre Ing. de Datos y Científico de Datos

![[Pasted image 20250513150742.png]]

|           | Ingeniero de Datos                                                                                                                                                                                        | Científico de Datos                                                                                                        |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Nombre    | Vi                                                                                                                                                                                                        | Julian                                                                                                                     |
| Funciones | Utiliza los datos recolectados. Ingiere y almacena los datos recogidos.              En el ejemplo, Vivian recolecta y almacena datos de clientes, artistas y canciones en sus respectivas bases de datos | Utiliza las tablas de datos para comprender los patrones de escucha de los usuarios o construir motores de recomendaciones |
|           | Se asegura de que las bases de datos esten optimizadas para el analisis, estructura de las tablas, informacion facil de recuperar, etc                                                                    | Accede a las bases de datos para usar los datos que contienen                                                              |
|           | Se asegura de que Julian pueda acceder facilmente a los datos de pistas, artistas y sesiones de escucha, para que pueda analizarlos ahorrándole tiempo para prepararlos                                   | Usa los resultados de esta pipeline de datos                                                                               |
|           | Construye la pipeline que extrae los datos de las sesiones de escucha para que los analisis de Julian, se mantengan actualizados                                                                          |                                                                                                                            |
|           | Expertos en software. Python, Java, SQL. Crear o Actualizar BBDD                                                                                                                                          | Expertos en análisis. Python y R, para consultar a las BBDD                                                                |
|           |                                                                                                                                                                                                           |                                                                                                                            |


# [[Capitulo 1 - 4. The Data Pipeline]]