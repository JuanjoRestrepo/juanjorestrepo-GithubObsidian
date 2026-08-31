---
title: "3 - SQL injection UNION attack, determining the number of columns returned by the query"
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
![[Pasted image 20240507181048.png]]
Si entramos en alguna de las categorías, vemos que se hace una query por detrás, fijándonos en la url:
![[Pasted image 20240507181215.png]]
En este punto lo que hay que hacer es adivinar el número de columnas de la tabla, donde cada NULL representa una columna, y por ejemplo poniendo 3 NULL, acertamos con que la tabla tiene 3 columnas y por tanto se imprime toda la información:
```bash
/filter?category=Accessories+UNION+SELECT+NULL,NULL,NULL--
```
![[Pasted image 20240507181449.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
