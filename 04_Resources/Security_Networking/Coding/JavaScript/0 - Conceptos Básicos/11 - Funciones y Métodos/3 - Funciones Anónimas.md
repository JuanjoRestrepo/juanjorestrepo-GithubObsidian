---
title: "3 - Funciones Anónimas"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Las **funciones anónimas** en JavaScript son funciones que no tienen un nombre definido. Son útiles en situaciones donde se necesita una función temporal o se desea pasar una función como argumento a otra función. Estas funciones se pueden asignar a variables, usar como callbacks, o definir directamente en la invocación de otra función. A continuación, te presento algunos ejemplos de cómo funcionan las funciones anónimas en JavaScript.
**Definición y Asignación a Variables**

```javascript
const suma = function(a, b) {
    return a + b;
};

console.log(suma(5, 3)); // Salida: 8
```


**Funciones Callback**
una **función callback** es una función que se pasa como argumento a otra función y se ejecuta después de que esa función haya terminado su trabajo

```javascript
function procesarDato(dato, callback) {
    console.log("Procesando dato: " + dato);
    callback();
}

function finalizarProceso() {
    console.log("Proceso finalizado.");
}

// Llamamos a la función `procesarDato` con el callback `finalizarProceso`
procesarDato("12345", finalizarProceso);
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
