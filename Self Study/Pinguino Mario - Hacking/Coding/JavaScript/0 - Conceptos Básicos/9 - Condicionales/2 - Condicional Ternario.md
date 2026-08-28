---
title: "2 - Condicional Ternario"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El operador condicional ternario en JavaScript es una forma concisa de realizar una evaluación condicional.
```javascript
let edad = 18;
let mensaje = (edad >= 18) ? "Eres mayor de edad." : "Eres menor de edad.";

console.log(mensaje); // "Eres mayor de edad."
```
![[Pasted image 20241014120542.png]]
O también se puede guardar en la variable resultado la comprobación:
```javascript
let nombre = "Mario";
let edad = 28;

let resultado = (edad >= 18) ? "Eres mayor de edad." : "Eres menor de edad.";

console.log(resultado);
```
![[Pasted image 20241014120857.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
