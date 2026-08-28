---
title: "Laboratorio 3 - DOM XSS in document.write sink using source location.search"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio, donde podemos añadir información:
![[Pasted image 20240523232837.png]]
Pero si inspeccionamos la página, vemos que en img se ha añadido el texto que hemos puesto:
![[Pasted image 20240523232906.png]]
Por tanto, podemos añadir el siguiente payload para romper el atributo:
![[Pasted image 20240523233029.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
