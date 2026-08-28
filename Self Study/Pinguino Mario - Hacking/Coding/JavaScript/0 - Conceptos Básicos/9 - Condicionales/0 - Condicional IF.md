---
title: "0 - Condicional IF"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Un condicional if en JavaScript permite ejecutar un bloque de código si una condición específica se evalúa como true:
```javascript
let calificacion = 76;

if (calificacion >= 90) {
    console.log("Excelente");

} else if (calificacion >= 80) {
    console.log("Muy Bien");

} else if (calificacion >= 70) {
    console.log("Bien");

} else if (calificacion >= 60) {
    console.log("Suficiente");
    
} else {
    console.log("Insuficiente");
}
```
![[Pasted image 20241014115619.png]]
También podemos usar condicionales negativos con la exclamación `!` 
```javascript
let quieroCebolla = false;

if (quieroCebolla != true){
    console.log("Tu comida no lleva cebolla");

}else{
    console.log("Tu comida sí lleva cebolla");
}
```
![[Pasted image 20241014120044.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
