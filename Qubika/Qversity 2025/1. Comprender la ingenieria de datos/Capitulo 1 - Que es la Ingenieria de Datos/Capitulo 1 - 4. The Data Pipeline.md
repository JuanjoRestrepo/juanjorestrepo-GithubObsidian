---
tags:
  - Qversity
  - IngenieriaDatos
  - DataEngineer
  - DataPipelines
Created: 2025-05-13
---

## Los datos son el nuevo petróleo

![[Pasted image 20250513153129.png]]

## Analogía del Petróleo y los Datos

Podemos entender el flujo de datos de manera similar al procesamiento del petróleo crudo:

![[Pasted image 20250513153244.png]]

1.  **Datos Crudos:** Al igual que traemos petróleo crudo de un yacimiento, recolectamos **datos crudos** de diversas fuentes.
2.  **Transformación:** El traslado del crudo a una unidad de destilación, donde se separa en varios productos, es análogo a la **transformación de los datos**. Aquí, los datos crudos se limpian, se estructuran y se adaptan para diferentes usos.
3.  **Distribución y Uso:**
    * Algunos productos del petróleo se envían directamente a sus usuarios finales (ej: queroseno a aeropuertos a través de **tuberías/pipelines**). De manera similar, algunos datos transformados se utilizan directamente.
    * Otros productos (ej: gasolina a instalaciones de almacenamiento antes de gasolineras) pasan por etapas intermedias antes de llegar al usuario final. Esto también ocurre con los datos.
    * Finalmente, algunos productos (ej: nafta a polímeros sintéticos) sufren transformaciones químicas complejas para crear nuevos productos. Esto se asemeja a la aplicación de modelos y análisis avanzados sobre los datos transformados.

## Pipelines de Datos

Podemos visualizar que tenemos muchos conductos que lo unen todo (**Pipelines**). Estos **pipelines de datos** son los sistemas que transportan, transforman y **entregan los datos desde su origen hasta su destino final**, de forma similar a las tuberías en una refinería de petróleo.

---

## Back to Data Engineering

![[Pasted image 20250513202237.png]]

Similar al proceso de tratamiento del petróleo, las empresas **ingieren datos** de **muchas fuentes distintas** que hay que **procesar y almacenar de diferentes maneras**.

Para ello, necesitamos:
- Tuberías/Pipelines que **automaticen eficazmente ese flujo** de una estación a otra
- Los pipelines de datos garantizan un flujo **constante, actualizado y preciso** de información relevante, lo que habilita a los científicos de datos a trabajar con datos al día.

### En Spotflix

- Tenemos fuentes de las que extraemos datos, por ejemplo, **las acciones y el historial de escucha** de los usuarios en *móbil, escritorio y el sitio web*.
- Los datos se **ingieren** en el sistema de spotflix, **pasando de sus respectivas fuentes** a nuestro **Data Lake**. *Esas son las primeras **3 Pipelines***
- Luego organizaremos los datos por medio de bases de datos, donde podemos organizarlos en:

1. **Datos del Artista**
	1. Nombre
	2. Número de seguidores
	3. Actos asociados
2. **Datos los de Albums**
	1. Sello
	2. Productora
	3. Año de publicación
3. **Datos de las pistas/tracks**
	1. Nombre
	2. Duración
	3. Artistas destacados
	4. Número de veces escuchado/reproducciones
4. **Datos de las Playlists**
	1. Nombre
	2. Canción que contiene
	3. Fecha de creación
5. **Datos de los Clientes**
	1. Nombre de usuario
	2. Fecha de apertura de la cuenta
	3. Nivel de subscripción
6. **Datos de los Empleados**
	1. Nombre
	2. Salario
	3. Responsable del informe/actualizados recursos humanos

Estas serían nuestras **6 nuevas Tuberías/Pipelines**

![[Pasted image 20250513202556.png]]

De igual forma, podríamos extraer datos como:

**Los Álbumes**
- Fotos de la portada. Al tener el mismo formato, podemos almacenarlas sin tener que cortarlas

**Los Empleados**
- Se podrían dividirse en diferentes tablas por departamento, como por ejemplo, *ventas, ingeniería, soporte, etc...*
- De igual forma, podría dividirse más, por oficinas, por ejemplo la de *USA, Belgica y UK*. Esto serviría para **analizar la rotación del personal/empleados**

**Las Pistas/Tracks**
- Tendría que procesarse para *comprobar si el Track es legible*
- Comprobar *si el artista correspondiente está en la BBDD* para *asegurarse que el archivo tiene el tamaño y formato correcto*

---

A partir de esto, es posible utilizar todos estos datos ordenados para **almacenarse en una BBDD de pistas limpias**, la cual se podría utilizar para crear un **Motor de Recomendación**, mediante el **análisis de similitud entre las canciones**


##### En resumen:

Los Data Pipelines aseguran un flujo de datos eficiente, de tal manera que:

**Automatizan la**
- Extracción
- Transformación
- Combinación
- Validación
- Carga

De los datos

**Reducen**
- Intervención Humana
- Errores
- El tiempo que le toma a los datos en fluir por la organización

---

## ETL and Data Pipelines

### ETL

- Es un marco popular usado para **diseñar Pipelines de datos**
- Permite dividir el flujo de datos en 3 pasos secuenciales
	1. **Extract** data
	2. **Transform** extracted data
	3. **Load** transformed data to another database (En una nueva BBDD)

La clave aquí está, en que **los datos se procesan antes de almacenarse**

### Data Pipelines

- **Mueven datos** de un sistema a otro
- **Pueden seguir ETL** pero **no todo el tiempo**
- Los datos **no pueden ser transformados**
- Los datos **pueden ser cargados directamente en aplicaciones**


# [[Resumen Capitulo 1]]