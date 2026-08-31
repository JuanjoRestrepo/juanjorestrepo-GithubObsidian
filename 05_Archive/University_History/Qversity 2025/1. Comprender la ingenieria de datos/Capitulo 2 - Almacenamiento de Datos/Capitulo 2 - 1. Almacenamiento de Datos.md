---
tags:
  - Qversity
  - SQL
Created: 2025-05-14
---


En este capitulo se centrará en el almacenamiento. Aprenderemos sobre la **Estructura de Datos**


# Datos Estructurados

- Son fáciles de buscar y organizar
- Tienen un modelo consistente/estructura rígida, como una hoja de cálculo, donde hay **filas (rows) y columnas (columns)** fijas
- Cada columna toma valores de un tipo determinado, como **texto, datos o decimal**
-  Pueden **agruparse** para **formar relaciones** (Facilita la formación de relaciones). Este tipo de organización se llama ***BASE DE DATOS RELACIONAL***

Alrededor del $20\%$ de los datos son estructurados. El *lenguaje de consultas*, ***SQL***, se utiliza para consultar esos datos.

## Employee table

| index | last_name  | first_name | role               | team             | full_time | office         |
| ----- | ---------- | ---------- | ------------------ | ---------------- | --------- | -------------- |
| 0     | Thien      | Vivian     | Data Engineer      | Data Science     | 1         | Belgium        |
| 1     | Huong      | Julian     | Data Scientist     | Data Science     | 1         | Belgium        |
| 2     | Duplantier | Norbert    | Software Developer | Infrastructure   | 1         | United Kingdom |
| 3     | McColgan   | Jeff       | Business Developer | Sales            | 1         | United States  |
| 4     | Sanchez    | Rick       | Support Agent      | Customer Service | 0         | United States  |

### Ejemplo Base de Datos relacional

| office  | address        | number | city     | zipcode  |
| ------- | -------------- | ------ | -------- | -------- |
| Belgium | Martelarenlaan | 38     | Leuven   | 3010     |
| UK      | Old Street     | 207    | London   | EC1V 9NR |
| USA     | 5th Ave        | 350    | New York | 10118    |

# Datos Semiestructurados:

Los Datos Semiestructurados se parecen a los estructurados, pero permiten más libertad. Por eso:

- Son **relativamente fáciles de organizar**
- Están bastante estructurados pero con **mayor flexibilidad**
- Tienen **distintos tipos de datos**
- Pueden **agruparse para formar relaciones**, pero esto **no es tan sencillo** como con los Datos Estructurados
- Se almacenan en **BASES DE DATOS NoSQL**
- Aprovechan los formatos de archivo *JSON, XML, YAML*

### Ejemplo JSON

Aquí se almacenan los artistas favoritos de cada usuario de Spotfix

```json 
{
  "user_1645156": {
    "last_name": "Lacroix",
    "first_name": "Hadrien",
    "favorite_artists": ["Fools in Deed", "Gojira", "Pain", "Nanowar of Steel"]
  },
  
  "user_5913764": {
    "last_name": "Billen",
    "first_name": "Sara",
    "favorite_artists": ["Tamino", "Taylor Swift"]
  },
  
  "user_8436791": {
    "last_name": "Sulmont",
    "first_name": "Lis",
    "favorite_artists": ["Arctic Monkeys", "Rihanna", "Nina Simone"]
  }
  
  // ... (rest of the JSON) }´
}
```

En este modelo podemos ver:
- Cada identificador de usuario, contiene el **apellido** y **nombre** del usuario
- Contiene los **artistas favoritos** del usuario. Sin embargo, este **número de artistas favoritos** puede variar
- **Este tipo de flexibilidad** (variación del número de artistas), **no se permite en las Bases de Datos Relacionales**

# Datos No Estructurados:

- Son datos que **no siguen un modelo**
- **No pueden contenerse** en un formato de **filas y columnas**. Esto dificulta la búsqueda y organización
- Suelen ser: *Imágenes, texto, sonido o videos*
- Suele **almacenarse en Lagos de Datos** (Data Lakes), aunque también en Data Warehouses o Data Bases

##### Nota:
La mayoría de los datos que nos rodean, no están estructurados. Pero pueden ser muy valiosos

### En Spotflix

- Los **Datos No Estructurados** consisten en: *Letras de Canciones, las propias canciones, fotos de álbumes y de perfil de los artistas y los videos musicales*
- Podríamos usar Algoritmos de Machine Learning para:
	- Analizar espectros de canciones
	- Analizar pulsaciones por minuto
	- Progresiones de acordes o géneros para categorizar las canciones. 
	- Incluso, hasta agregar información adicional como el género y otras etiquetas (datos semiestructurados) para facilitar la búsqueda y organización


## [[Capitulo 2 - 2. SQL Databases]]
