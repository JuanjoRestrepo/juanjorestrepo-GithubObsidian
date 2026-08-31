---
title: "Laboratorio 9 - Reflected XSS into a JavaScript string with angle brackets HTML encoded"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240527113935.png]]
Al buscar por algo en el campo de búsqueda, vemos como la palabra que buscamos se encuentra dentro del código fuente dentro de javascript:
![[Pasted image 20240527114059.png]]
Podemos probar con el siguiente payload, pero no va a funcionar porque javascript no permite espacios:
```bash
' alert('XSS') '
```
![[Pasted image 20240527114452.png]]
Para hacer un bypass de esto, podemos usar guiones:
```bash
'-alert("XSS")-'
```
![[Pasted image 20240527114612.png]]
Y ya habremos completado el laboratorio:
![[Pasted image 20240527114631.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
