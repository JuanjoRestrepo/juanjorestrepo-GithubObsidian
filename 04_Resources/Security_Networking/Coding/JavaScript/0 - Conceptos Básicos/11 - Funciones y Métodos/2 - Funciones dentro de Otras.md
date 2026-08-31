---
title: "2 - Funciones dentro de Otras"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Las **funciones dentro de otras funciones** se llaman funciones anidadas o funciones internas. Esto es útil cuando deseas organizar tu código y crear funciones que solo tengan sentido dentro de una función externa.

Las funciones dentro de otras funciones permiten una mejor organización del código y la creación de funciones que se centran en un contexto específico. Pueden acceder a las variables de la función externa, y su uso es común en situaciones donde se necesita encapsular lógica o crear funciones de manera dinámica.

---------

**Función Interna Simple**
```javascript
function saludar(nombre) {
    function mensaje() {
        return `Hola, ${nombre}!`;
    }
    console.log(mensaje());
}

saludar('Mario'); // Salida: Hola, Mario!
```
![[Pasted image 20241014122620.png]]


**Acceso a Variables Externas**
Las funciones internas pueden acceder a las variables definidas en la función externa:
```javascript
function calcularArea(base, altura) {
    function area() {
        return (base * altura) / 2;
    }
    console.log(`El área del triángulo es: ${area()}`);
}

calcularArea(5, 10); // Salida: El área del triángulo es: 25
```
![[Pasted image 20241014123641.png]]


**Funciones Anidadas para Lógica Condicional**
Puedes usar funciones internas para realizar operaciones específicas o condicionales dentro de la función externa.
```javascript
function verificarNumero(num) {
    function esPar() {
        return num % 2 === 0;
    }

    if (esPar()) {
        console.log(`${num} es un número par.`);
    } else {
        console.log(`${num} es un número impar.`);
    }
}

verificarNumero(7); // Salida: 7 es un número impar.
verificarNumero(10); // Salida: 10 es un número par.
```
![[Pasted image 20241014123652.png]]


**Función Interna con Parámetros**
Las funciones internas también pueden tener sus propios parámetros.
```javascript
function operaciones(a, b) {
    function suma(x, y) {
        return x + y;
    }

    function resta(x, y) {
        return x - y;
    }

    console.log(`Suma: ${suma(a, b)}`);
    console.log(`Resta: ${resta(a, b)}`);
}

operaciones(5, 3);
// Salida:
// Suma: 8
// Resta: 2

```
![[Pasted image 20241014123702.png]]

**Funciones que Retornan Otras Funciones**
Una función externa puede retornar una función interna, lo que permite crear funciones personalizadas.
```javascript
function crearMultiplicador(factor) {
    return function(num) {
        return num * factor;
    };
}

const duplicar = crearMultiplicador(2);
const triplicar = crearMultiplicador(3);

console.log(duplicar(5)); // Salida: 10
console.log(triplicar(5)); // Salida: 15
```
![[Pasted image 20241014123712.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
