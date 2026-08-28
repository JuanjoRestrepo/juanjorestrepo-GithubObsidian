---
title: "0 - Funciones en Javascript"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Las funciones en JavaScript son bloques de código reutilizables que realizan una tarea específica. Se pueden definir de varias maneras, y se utilizan para estructurar el código de manera más eficiente y organizada, existiendo los distintos tipos:
**Función Declarativa**
```javascript
function saludar(nombre) {
    return `Hola, ${nombre}!`;
}

console.log(saludar('Mario')); // Salida: Hola, Mario!
```
![[Pasted image 20241014122620.png]]
**Función Expresiva**
```javascript
const saludar = function(nombre) {
    return `Hola, ${nombre}!`;
};

console.log(saludar('Mario')); // Salida: Hola, Mario!
```
![[Pasted image 20241014122620.png]]

**Funciones Flecha**
```javascript
const saludar = (nombre) => {
    return `Hola, ${nombre}!`;
};

console.log(saludar('Mario')); // Salida: Hola, Mario!

// Versión más corta si solo hay una línea de código
const saludarCorta = nombre => `Hola, ${nombre}!`;

console.log(saludarCorta('Mario')); // Salida: Hola, Mario!
```
![[Pasted image 20241014122620.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
