---
title: "1 - Operador Typeof"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El operador `typeof` se utiliza para determinar el tipo de una variable o un valor. Devuelve una cadena que representa el tipo del operando.
```javascript
let frase = "Hola soy Mario";
let anio = 2027;            
let interes = 2.7;          
let mayorEdad = true;    
let vacia;                   
let nula = null;              

let frutas = ["fresa", "sandia", "naranja"]; 
let hero = { nombre: "Batman", universo: "DC" };

console.log(frase, interes, mayorEdad);

console.log(typeof frase); // Dirá que frase es un string.
```
![[Pasted image 20241014105335.png]]
También podemos comprobar si un dato es un array:
```javascript
let frase = "Hola soy Mario";
let anio = 2027;            
let interes = 2.7;          
let mayorEdad = true;    
let vacia;                   
let nula = null;              

let frutas = ["fresa", "sandia", "naranja"]; 
let hero = { nombre: "Batman", universo: "DC" };

console.log(frase, interes, mayorEdad);

console.log(Array.isArray(frutas)); // Dirá que es true
```
![[Pasted image 20241014105541.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
