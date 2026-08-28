---
title: "4 - Dlanding Volumes"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Son aquellos volúmenes que quedan inoperativos y no sirven, es decir, que ningún contenedor los está usando. Para acceder a ellos puedo poner docker volume ls -f dangling=true:
![[Pasted image 20221231200541.png]]
Si utilizo un -q obtengo los id de estos volúmenes:
![[Pasted image 20221231200549.png]]
Y para borrarlos utilizo xargs docker volume rm:
![[Pasted image 20221231200558.png]]
Y ahora como vemos ya no tengo ningún volumen dangling:
![[Pasted image 20221231200612.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
