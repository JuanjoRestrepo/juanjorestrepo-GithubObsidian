---
title: "Union"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con la sentencia UNION podremos unificar el resultado de dos tablas diferentes en una sola consulta, es decir, se nos suman los registros de una tabla con los de otra, aunque para que funcione es necesario que ambas tablas tengan el mismo número de columnas:

![[Pasted image 20221221213502.png]]

Hay que tener en cuenta que las columnas que se muestran son las de la primera consulta que se haga, por ejemplo si primero se hace la consulta en departments, se mostrarán las columnas de esta tabla:
![[Pasted image 20221221213716.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
