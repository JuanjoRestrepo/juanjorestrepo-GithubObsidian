---
title: "6 - PKEXEC - Escalada de Privilegios"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En caso de encontrarnos con el binario SUID de pkexec, podemos escalar privilegios de esta forma:
![[Pasted image 20230507113855.png]]
Por lo que buscamos un exploit para explotar esta vulnerabilidad y lo ejecutamos en la máquina víctima:
![[Pasted image 20230507113929.png]]
Lo compartimos con la máquina víctima, lo ejecutamos y ya somos root:
![[Pasted image 20230507114002.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
