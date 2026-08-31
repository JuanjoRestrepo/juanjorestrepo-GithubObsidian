---
title: "7 - Escalada de Privilegios Binario SUID env"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Una vez dentro, tras hacer varias investigaciones, vemos que si buscamos binarios SUID vemos el de env, el cual es vulnerable:
![[Pasted image 20230522161522.png]]
Y ahora podemos lanzarnos una bash como root usando este binario de la siguiente forma:
![[Pasted image 20230522161633.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
