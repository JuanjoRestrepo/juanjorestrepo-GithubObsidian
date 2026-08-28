---
title: "Variables"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos crear variables dentro del bloque DECLARE, para posteriormente utilizarlas y ejecutarlas dentro del bloque BEGIN. Por ejemplo en la siguiente captura podemos ver cómo creamos distintas variables y luego dentro del BEGIN las ejecutamos:
![[Pasted image 20230102201506.png]]
Con dbms_output.put_line estamos haciendo un print, para imprimir el valor de las variables; y luego con el || lo estamos concatenando.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
