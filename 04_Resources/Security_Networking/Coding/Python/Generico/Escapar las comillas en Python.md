---
title: "Escapar las comillas en Python"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Puede darse el caso de que dentro de una variable tengamos un texto que tiene dentro otras comillas dobles, que estén dando error y entrando en conflicto con las comillas que tenemos normales, como este caso:
![[Pasted image 20230117214559.png]]
Por tanto, si queremos solucionar esto, tenemos que escapar las comillas, que significa que donde hay una sola comilla, ahora justo detrás le pondremos una barrita:
![[Pasted image 20230117214640.png]]
Y al imprimirlo nos lo interpreta sin problemas leyendo correctamente las comillas:
![[Pasted image 20230117214711.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
