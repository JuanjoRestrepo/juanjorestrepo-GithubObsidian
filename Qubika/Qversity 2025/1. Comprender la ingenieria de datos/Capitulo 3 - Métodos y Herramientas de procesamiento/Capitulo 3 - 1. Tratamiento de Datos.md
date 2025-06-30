
Estamos haciendo tratamiento de datos cuando:

- Cuando trasladamos datos al lago de datos
- Cuando los dividimos en diferentes tablas
- Cuando eliminamos pistas corruptas

En pocas palabras, el procesamiento de datos
- Es **convertir Datos Brutos** en **Información con un significado**

---
## Data processing value

**Conceptualmente:**
* Remover datos no deseados
* Para ahorrar memoria, procesos y costos de red
* Convertir datos de un tipo a otro
* Organizar datos
* Para ajustarse a un esquema/estructura
* Incrementar la productividad

**En Spotflix:**
* No hay necesidad de formato sin pérdida
* No pueden permitirse almacenar archivos tan grandes
* Convertir canciones de `.wav` o `.flac` a `.ogg`
* Reorganizar datos del lago de datos a los data warehouses
* Ejemplo de tabla de empleados
* Habilitar a los científicos de datos


## Cómo los ingenieros de datos procesan los datos


* Tareas de **manipulación, limpieza y organización de datos**
    * que pueden **ser automatizadas**.
    * que **siempre necesitarán hacerse**
* **Almacenar** datos en una **base de datos estructurada** de forma sensata
* Crear **vistas sobre las tablas** de la base de datos
* **Optimizar el rendimiento** de la base de datos
* **Rechazar archivos corruptos** de canciones
* Decidir **qué sucede con los metadatos faltantes**
* Separar las tablas de artistas y álbumes...
    * ...pero proporcionar una vista que las combine
* Indexación: *para recuperar más fácil a los datos*


## **Scheduling (Programación/Planificación)**

- Puede aplicarse a cualquier tarea listada en el procesamiento de datos.
- La programación es el pegamento de tu sistema.
- Mantiene cada pieza y organiza cómo trabajan juntas.
- Ejecuta tareas en un orden específico y resuelve todas las dependencias.

## **Manual, time, and sensor scheduling (Programación manual, por tiempo y por sensor)**

- Manualmente
- Ejecutar automáticamente a una hora específica
- Ejecutar automáticamente si se cumple una condición específica
    - Programación por sensor
- Actualizar manualmente la tabla de empleados
- Actualizar la tabla de empleados a las 6 AM
- Actualizar las tablas de departamentos si se añadió un nuevo empleado


## **Batches and streams (Lotes y flujos)**

- **Batches (Lotes)**
    - Agrupar registros a intervalos
    - A menudo más económico
    - Canciones subidas por artistas
    - Tabla de empleados
    - Tabla de ingresos
- **Streams (Flujos)**
    - Enviar registros individuales inmediatamente
    - Nuevos usuarios registrándose
    - Otro ejemplo: escucha en línea vs. sin conexión


## Tools for Scheduling

![[Pasted image 20250514213323.png]]