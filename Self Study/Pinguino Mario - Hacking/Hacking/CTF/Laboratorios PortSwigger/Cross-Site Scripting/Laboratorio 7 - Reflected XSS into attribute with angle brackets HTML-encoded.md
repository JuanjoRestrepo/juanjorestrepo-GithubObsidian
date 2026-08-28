---
title: "Laboratorio 7 - Reflected XSS into attribute with angle brackets HTML-encoded"
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
![[Pasted image 20240524174847.png]]
Dentro del buscador ponemos cualquier dato:
![[Pasted image 20240524175026.png]]
Y por aquí vemos que lo que ponemos en el buscador se refleja arriba:
![[Pasted image 20240524175406.png]]
Teniendo en cuenta los dos últimos puntos, podemos crear un payload que nos cree un nuevo atributo dentro del elemento input para que se nos ejecute un alert. En este caso el payload es:
```bash
'"onmousemove="alert(1)'
```
![[Pasted image 20240524175618.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
