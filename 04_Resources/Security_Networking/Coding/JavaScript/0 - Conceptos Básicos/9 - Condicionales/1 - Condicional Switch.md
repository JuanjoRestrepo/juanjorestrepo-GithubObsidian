---
title: "1 - Condicional Switch"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En JavaScript, el `switch` es una estructura de control que permite ejecutar diferentes bloques de código en función del valor de una expresión. Es una alternativa a múltiples sentencias `if-else` cuando se necesita comparar una variable contra diferentes valores.
```javascript
let dia = 3; // Suponiendo que 1 es lunes, 2 es martes, etc.

switch (dia) {
    case 1:
        console.log("Hoy es lunes.");
        break;
    case 2:
        console.log("Hoy es martes.");
        break;
    case 3:
        console.log("Hoy es miércoles.");
        break;
    case 4:
        console.log("Hoy es jueves.");
        break;
    case 5:
        console.log("Hoy es viernes.");
        break;
    case 6:
        console.log("Hoy es sábado.");
        break;
    case 7:
        console.log("Hoy es domingo.");
        break;
    default:
        console.log("Día no válido.");
        break;
}
```
![[Pasted image 20241014120429.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
