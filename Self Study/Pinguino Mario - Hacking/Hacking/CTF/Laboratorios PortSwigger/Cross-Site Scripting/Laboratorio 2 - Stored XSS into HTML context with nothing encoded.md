---
title: "Laboratorio 2 - Stored XSS into HTML context with nothing encoded"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este es el laboratorio:
![[Pasted image 20240411221922.png]]
Y si entramos en alguna de las categorías, veremos un lugar donde poner comentarios:
![[Pasted image 20240411222241.png]]
Ponemos lo siguiente, donde en el campo de comentario vamos a inyectar el XSS:
![[Pasted image 20240411222421.png]]
Y con esto habremos vulnerado la web y completado el laboratorio:
![[Pasted image 20240411222436.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
