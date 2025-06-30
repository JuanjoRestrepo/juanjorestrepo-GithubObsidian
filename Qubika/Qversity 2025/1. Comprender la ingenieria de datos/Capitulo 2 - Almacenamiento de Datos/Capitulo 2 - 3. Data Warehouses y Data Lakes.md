---
tags:
  - Qversity
<<<<<<< HEAD
  - DataWarehouse
  - DataLake
Created: 2025-05-14
---
Pre
![[Pasted image 20250514164924.png]]
Recordemos nuestra **Pipeline de Datos**

![[Pasted image 20250514164955.png]]


| Data Lake                                           | Data Warehouse                                      |
| --------------------------------------------------- | --------------------------------------------------- |
| Almacena toda la **Data Cruda**                     | Almacena **Data Específica** para uso específico    |
| Puede ser petabytes (1 millón GBs)                  | Relativamente pequeño                               |
| Almacena **todas las estructuras de datos**         | Almacena principalmente **Data Estructurada**       |
| Rentable en **Cost-Effective**                      | **Más costoso** de actualizar                       |
| Difícil de analizar debido a la falta de estructura | **Optimizado para el análisis de datos**            |
| Requiere un catálogo actualizado                    | Optimizado para **Analistas de datos y de negocio** |
| Usado por **Científicos de datos**                  |                                                     |
| Big data, analítica en tiempo real                  | Consultas ad-hoc, de solo lectura                   |

## Catálogo de Datos para Data Lakes

Es una **fuente de verdades** que **compensa la falta de estructura de un Data Lake**
- Realiza un seguimiento de donde proceden los datos
- Cómo se utilizan?
- Quién es el responsable de su mantenimiento?
- Con qué frecuencia de actualizan los datos?
- **Buena práctica** en términos de *Gobernanza de los Datos, gestión de la disponibilidad, usabilidad,  integridad y seguridad de los datos*
- Garantiza la **reproducibilidad de los procesos** en caso de que surja algún imprevisto
- Si alguien quiere empezar desde el inicio, comenzando por la ingestión de los datos.
- El **Catálogo de Datos evita** **que el Data Lake se convierta en un Pantano de Datos (Data Swamp)**. Esto es debido a la facilidad del Data Lake para almacenar datos

![[Pasted image 20250514171228.png]]

#### Disponer de un Catálogo de Datos es una Excelente Práctica porque permite:
- Confiabilidad
- Autonomía
- Escalabilidad (Permite que **el trabajo con los datos sea más escalable**)
- Velocidad
- Pasar de buscar datos a prepararlos sin depender de una fuente humana de información cuando hayan dudas

## **Base de datos vs. Data Warehouse**

- **Base de datos:**
    - Término general
    - Definido vagamente como _datos organizados_ almacenados y accedidos en una computadora
- **Data warehouse** es un tipo de base de datos.
=======
  - D
>>>>>>> origin/main
