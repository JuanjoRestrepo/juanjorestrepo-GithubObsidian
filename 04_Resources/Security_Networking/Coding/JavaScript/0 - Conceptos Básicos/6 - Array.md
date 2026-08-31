---
title: "6 - Array"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Los arrays en JavaScript son objetos especiales que permiten almacenar colecciones de datos, pudiendo crear un array utilizando la notación de corchetes `[]`:
```javascript
const frutas = ["manzana", "banana", "naranja"];
```
Y luego podemos acceder a estos elementos con un console.log:
```javascript
console.log(frutas[0]); // manzana
console.log(frutas[1]); // banana
```
Y podemos modificarlo de la siguiente forma:
```javascript
frutas[2] = "kiwi";
console.log(frutas); // ["manzana", "banana", "kiwi"]
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
