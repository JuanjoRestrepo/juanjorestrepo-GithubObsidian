---
title: "4 - Scope o Ámbito de las Variables"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El **scope** o **ámbito** de las variables en JavaScript se refiere al contexto en el que las variables están definidas y desde donde pueden ser accedidas. Existen varios tipos de scope en JavaScript, que determinan la accesibilidad de las variables en diferentes partes del código.

**Scope Global**
Las variables declaradas fuera de cualquier función o bloque se consideran variables globales y pueden ser accedidas desde cualquier parte del código, tanto dentro como fuera de funciones.
```javascript
var nombre = "Mario";  // Variable global

function mostrarNombre() {
    console.log(nombre);  // Puede acceder a 'nombre' porque es global
}

mostrarNombre();  // Imprime: Mario
console.log(nombre);  // También puede acceder fuera de la función: Mario
```
![[Pasted image 20241015084341.png]]
**Scope Local**
Las variables declaradas dentro de una función solo están disponibles dentro de esa función. Esto se conoce como scope local o scope de función.
```javascript
function saludar() {
    var saludo = "Hola";  // Variable local
    console.log(saludo);  // Puede acceder a 'saludo' dentro de la función
}

saludar();  // Imprime: Hola
console.log(saludo);  // Error: 'saludo' no está definida fuera de la función
```
![[Pasted image 20241015084500.png]]
**Ámbito de Bloque**

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
