---
title: "Crear una Tabla con sus Registros"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Aquí vamos a especificar también cuál será la primary key:

![[Pasted image 20221219191958.png]]

Ahora lo mismo en versión detallada:

![[Pasted image 20221219192007.png]]

Ponemos auto_increment en el ID para que se vaya autoincrementando automáticamente, VARCHAR para soportar caracteres númericos y letras, FLOAT para soportar también números decimales, TEXT para soportar un texto largo y DATE para fechas.

CREAR TABLAS ESTABLECIENDO PRIMARY KEY Y FOREIGN KEY

Para ello voy a crear la tabla empleado y la tabla departamento y empleado:

![[Pasted image 20221219192031.png]]

Ahora, si queremos introducir datos, tenemos que tener en cuenta que los registros de cod_departamento está en común en ambas tablas, por tanto debe tener los mismos registros en este campo en ambas tablas:

![[Pasted image 20221219192040.png]]
Los registros de cod_departamento deben ser iguales en ambas tablas.

CONSULTAR LOS DETALLES DE UNA TABLA:

![[Pasted image 20221219192100.png]]

En la parte de abajo, NULL (no) significa que es un campo que no puede ir vacío, obligatoriamente debe tener un registro. En el resto de los casos pueden ir vacíos.

MOSTRAR TODAS LAS TABLAS DE MI BASE DE DATOS:

En nuestro caso sólo tenemos una tabla, pero si tuviera más aparecerían aquí:
![[Pasted image 20221219192121.png]]

CÓMO CONSULTAR LAS BASES DE DATOS QUE TENGO:

![[Pasted image 20221219192130.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
