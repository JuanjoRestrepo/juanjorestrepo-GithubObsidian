---
title: "Types of SQL Statements"
date: 2026-08-27
tags:
  - self-study
  - general-programming-tools
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# DDL vs DML
---
## **1. DDL: (Data Definition Language)**
---
- Define, change or drop database objects such as tables
- Common DDL statement types include:
	- CREATE: used for creating tables and defining its columns.
	- ALTER: used for altering tables including adding and dropping columns and modifying their datatypes
	- TRUNCATE: used for deleting data in a table but not the table itself
	- DROP: used for deleting tables

### 1.1 CREATE Table:
```SQL
CREATE TABLE table_name
{
	column_name_1 datatype optional_parameters,
	column_name_2 datatype,
	//...
	column_name_n datatype
}
```

Example: Create a table for Canadian provinces
```SQL
CREATE TABLE table_name
{
	id_char(2) PRIMARY KEY NOT NULL,
	name varchar(24)
}
```

![[Pasted image 20231127190028.png]]
- The first column id for storing the abbreviated 2 letter province short codes such as AB , BC, etc. 
- And the second column called name for storing the full name of the province, such as ALBERTA, BRITISH COLUMBIA, etc.

Now, let’s look at a more elaborate example based on the Library database.

![[Pasted image 20231127190128.png]]

This database includes several entities such as AUTHOR, BOOK, BORROWER, etc.

Let’s start by creating the table for the AUTHOR entity.
- The name of the table will be AUTHOR, and its attributes will be the columns of the table such as AUTHOR_ID, FIRSTNAME, LASTNAME, etc  will be the columns of the table
- In this table, we will also assign the Author_ID attribute as the Primary Key, so that no duplicate values can exist

![[Pasted image 20231127190227.png]]

To create the Author table, issue the following command: 

```SQL
CREATE TABLE author ( 
	author_id CHAR(2) PRIMARY KEY NOT NULL, 
	lastname VARCHAR(15) NOT NULL, 
	firstname VARCHAR(15) NOT NULL, 
	email VARCHAR(40), 
	city VARCHAR(15), 
	Country:char(2)
```

- Note that the Author_ID is the Primary Key. 
- This constraint prevents duplicate values in the table. 
- Also note that Last Name and First Name have the constraint NOT NULL. **This ensures that these fields cannot contain a NULL value**, **since an author must have a name.**

### 1.2 ALTER Table ... ADD COLUMN:
```SQL
ALTER TABLE <table_name>
	ADD COLUMN <column_name_1> datatype,
	...
	ADD COLUMN <column_name_n> datatype;
```
- Add or remove columns
- Modify the data type of columns
- Add or remove keys
- Add or remove constraints

For example, to add a telephone number column to the AUTHOR table in the Library database 

to store the author’s telephone number, use the following statement:
![[Pasted image 20231127191115.png]]

- In this example, the data type for the column is BIGINT which can hold a number up to 19 digits long. 
- You also use the ALTER TABLE statement to modify the data type of a column.



## **2. DML: (Data Manipulation Language)**
---
- Read and modify data in tables
- CRUD Operations (***Create, Read, Update and Delete rows***)
- Common DML statement types include: 
	- INSERT: used for inserting a row or several rows of data into a table
	- SELECT: reads or selects row or rows from a table
	- UPDATE: edits row or rows in a table
	- DELETE: removes a row or rows of data from a table.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#General Programming & Tools|Programación general y herramientas]].
- Criterio de producción: Convierte los apuntes en práctica verificable: reproduce ejemplos, documenta supuestos y enlaza el resultado con un caso de uso real.
