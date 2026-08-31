---
tags:
  - Qversity
  - SQL
Created: 2025-05-14
---


# SQL
- Structured Query Language (Lenguaje de Consulta Estructurado)
- Lenguaje estandar para hacer consultas RDBMS (Rational Database Management System) - Sistema de Gestión de Bases de Datos Relacionales, el cual reúne varias tablas y las relaciona entre si
- Permite *acceder a muchos registros a la vez, agruparlos, filtrarlos y agregarlos*
- Similar al inglés
- Los **Data Engineer usan SQL** para **crear y mantener Bases de Datos**
- Los **Data Scientists usan SQL** para **consultar Bases de Datos**
## Volviendo a la Employee table

| index | last_name  | first_name | role               | team             | full_time | office         |
| ----- | ---------- | ---------- | ------------------ | ---------------- | --------- | -------------- |
| 0     | Thien      | Vivian     | Data Engineer      | Data Science     | 1         | Belgium        |
| 1     | Huong      | Julian     | Data Scientist     | Data Science     | 1         | Belgium        |
| 2     | Duplantier | Norbert    | Software Developer | Infrastructure   | 1         | United Kingdom |
| 3     | McColgan   | Jeff       | Business Developer | Sales            | 1         | United States  |
| 4     | Sanchez    | Rick       | Support Agent      | Customer Service | 0         | United States  |

Para hacer una consulta a la Base de Datos como

#### **Data Engineer**

```SQL
CREATE TABLE employees (
	employee_id INT, 
	first_name VARCHAR(255), 
	last_name VARCHAR(255), 
	role VARCHAR(255), 
	team VARCHAR(255), 
	full_time BOOLEAN, 
	office VARCHAR(255) );
```

- `CREATE TABLE employees`: Instrucción para crear una nueva tabla llamada "employees".
- Columnas y tipos de datos: Define cada columna (nombre) y el tipo de información que almacenará (ej: número entero, texto).
- Ejemplo: `employee_id INT` crea una columna llamada "employee_id" para guardar números enteros.


#### **Data Scientist**

```sql 
SELECT first_name, last_name
FROM employees
WHERE role LIKE '%Data%'; 
```

- `SELECT first_name, last_name`: Selecciona las columnas "first_name" y "last_name" para mostrarlas.
- `FROM employees`: Indica que la búsqueda se realizará en la tabla llamada "employees".
- `WHERE role LIKE '%Data%'`: Filtra los resultados para incluir solo las filas donde la columna "role" contiene la palabra "Data" en cualquier parte del texto.

# Database schema

El **Esquema de la Base de Datos** es el que **rige cómo se relacionan las tablas**

### En Spotflix

- Tenemos una **tabla para álbumes**, que contiene columnas para:
- El *ID único* del álbum
- El *ID único* del artista
- El *título* del álbum, etc...

![[Pasted image 20250514162734.png]]

También tenemos una **Tabla de Artistas** que contiene columnas para:
- El  *ID único* para el artista
- El *nombre* del artista
- Su *biografía*

![[Pasted image 20250514162912.png]]

Estas dos tablas **pueden enlazarse entre sí:**
- A través del *ID único* del artista

![[Pasted image 20250514163019.png]]

También tenemos una **Tabla de Canciones** y de **Listas de Reproducción**, en las que podemos relacionar:
- El *ID del album* de la **Tabla de Canciones** con la **Tabla de Álbumes**
- El *ID de la canción* de la **Tabla de Listas de Reproducción** con la **Tabla de Canciones** 


![[Pasted image 20250514163059.png]]


## [[Capitulo 2 - 3. Data Warehouses y Data Lakes]]