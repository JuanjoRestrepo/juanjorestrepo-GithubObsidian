---
title: "Laboratorio 1 - Reflected XSS into HTML context with nothing encoded"
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
![[Pasted image 20240411221220.png]]
Donde tenemos el siguiente payload que debemos de usar para explotar un XSS:
```bash
<script>alert(1)</script>
```
Si pegamos esto en el buscador, habremos completado el laboratorio:
![[Pasted image 20240411221305.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
