---
title: "Insertar Datos en Tablas"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Primero ponemos DESCRIBE ordenadores para obtener información de la tabla por si no nos acordamos:

Recordemos que el id_ordenador después no lo añadimos porque es autoincrementable.

![[Pasted image 20221219192212.png]]

Y a continuación con INSERT INTO seleccionamos la tabla y los campos donde añadiremos información; y con VALUES vamos introduciendo los registros con la información:
![[Pasted image 20221219192220.png]]

  
Ahora si consulto la tabla ordenadores veremos como ya hemos introducido lo anterior correctamente (y vemos como el id_ordenador se añadió automáticamente:
![[Pasted image 20221219192228.png]]

Ahora bien, si se produce un error de foreign key, similar a este:

Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (`hr`.`employees`, CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`))        0.016 sec

Lo que habría que hacer sería primero añadir los campos a la otra tabla donde hay una foreign key vinculada con la tabla que estamos intentando actualizar, añadiendo primero los campos para podemos modificar después nuestra tabla:

![[Pasted image 20221219192238.png]]

Y después ya podemos modificar la tabla employees:

![[Pasted image 20221219192246.png]]

Y ahora vamos a hacer la consulta para comprobar que el trabajador fue añadido correctamente:

![[Pasted image 20221219192258.png]]

INSERT DE FILAS CON VALORES NULOS

Podemos insertar registros con valores nulos de la siguiente manera:

![[Pasted image 20221219192318.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
