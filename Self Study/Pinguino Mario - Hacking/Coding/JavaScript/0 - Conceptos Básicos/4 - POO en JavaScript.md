---
title: "4 - POO en JavaScript"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```javascript
// Clase persona usando una función constructora
function Persona(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
    
    // Método
    this.imprimirDetalles = function() {
        console.log(`Nombre: ${this.nombre}, Edad: ${this.edad}`);
    };
}

// Creación de instancias (objetos) de la clase Persona
let persona1 = new Persona('Juan', 30);
let persona2 = new Persona('María', 25);

persona1.imprimirDetalles();  // Imprime "Nombre: Juan, Edad: 30"
persona2.imprimirDetalles();  // Imprime "Nombre: María, Edad: 25"
```
Ejecutaríamos lo siguiente:
![[Pasted image 20240705104548.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
