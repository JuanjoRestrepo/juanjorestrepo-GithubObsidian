---
title: "Comando lsof - Conocer puertos ocupados de mi sistema Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Por ejemplo ejecutamos un servidor web con Python por el puerto 80:

![[Pasted image 20230127190239.png]]
 
Y ahora con el comando lsof -i:80 puero ver qué servicio está ocupando el puerto 80 de mi equipo:

  ![[Pasted image 20230127190310.png]]
Si quisiera detener este servicio con lsof podría utilizar el comando kill -9 de esta forma:
![[Pasted image 20230130113547.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
