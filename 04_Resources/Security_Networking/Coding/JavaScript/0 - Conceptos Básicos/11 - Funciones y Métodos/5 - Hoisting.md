---
title: "5 - Hoisting"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

**Hoisting** en JavaScript es un comportamiento por el cual las declaraciones de variables y funciones se "mueven" al principio de su contexto de ejecución antes de que el código sea ejecutado.
```javascript
console.log(coche);

var coche = "ferrari";
```
Vemos que nos muestra undefined, pero no saca un error:
![[Pasted image 20241015085155.png]]
Pero en cambio se declaramos la veriable con let, será más estricto y aquí sí nos dará error:
```javascript
console.log(coche);

let coche = "ferrari";
```
![[Pasted image 20241015085249.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
