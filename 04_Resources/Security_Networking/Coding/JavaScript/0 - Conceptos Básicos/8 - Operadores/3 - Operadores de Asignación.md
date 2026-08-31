---
title: "3 - Operadores de Asignación"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

emy
Los operadores de asignación en JavaScript se utilizan para asignar valores a variables.
```javascript
let num = 10; // Asignación simple

// Operadores de asignación
num += 5;    // Asignación de suma (num = num + 5)
console.log(`Suma: ${num}`); // 15

num -= 3;    // Asignación de resta (num = num - 3)
console.log(`Resta: ${num}`); // 12

num *= 2;    // Asignación de multiplicación (num = num * 2)
console.log(`Multiplicación: ${num}`); // 24

num /= 4;    // Asignación de división (num = num / 4)
console.log(`División: ${num}`); // 6

num %= 5;    // Asignación de módulo (num = num % 5)
console.log(`Módulo: ${num}`); // 1

num **= 3;   // Asignación de exponenciación (num = num ** 3)
console.log(`Exponenciación: ${num}`); // 1 (1 elevado a 3 es 1)

// Ejemplo con un nuevo valor
let a = 5;
let b = 2;

// Operadores de asignación combinados
a += b;     // a = a + b
console.log(`Nuevo valor de a: ${a}`); // 7

a -= b;     // a = a - b
console.log(`Nuevo valor de a: ${a}`); // 5

a *= b;     // a = a * b
console.log(`Nuevo valor de a: ${a}`); // 10

a /= b;     // a = a / b
console.log(`Nuevo valor de a: ${a}`); // 5

a %= b;     // a = a % b
console.log(`Nuevo valor de a: ${a}`); // 1

a **= b;    // a = a ** b
console.log(`Nuevo valor de a: ${a}`); // 1
```
![[Pasted image 20241014110241.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
