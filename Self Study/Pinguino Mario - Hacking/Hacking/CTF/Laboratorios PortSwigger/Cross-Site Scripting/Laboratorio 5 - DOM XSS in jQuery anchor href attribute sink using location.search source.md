---
title: "Laboratorio 5 - DOM XSS in jQuery anchor href attribute sink using location.search source"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En el enunciado nos comentan que tenemos un botón de submit feedback donde se acontece un XSS:
![[Pasted image 20240524102854.png]]
Una vez accedemos, vemos que se nos añade el parámetro:
```bash
returnPath=/
```
![[Pasted image 20240524102942.png]]
Podemos probar en escribir algo:
![[Pasted image 20240524103348.png]]
Y si pasamos el cursos por encima del Back vemos que se refleja:
![[Pasted image 20240524103803.png]]
Es decir, vemos que se refleja lo que escribimos dentro del código fuente:
![[Pasted image 20240524103847.png]]
Por lo que si usamos el siguiente payload, habremos explotado el XSS:
![[Pasted image 20240524104111.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
