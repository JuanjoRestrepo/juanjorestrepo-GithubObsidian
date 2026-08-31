---
title: "2 - Bucle do While"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En JavaScript, el bucle `do while` se utiliza para ejecutar un bloque de código al menos una vez incluso cuando la condición no se cumpla, tal y como ocurre en este caso que no entraríamos dentro del bucle, pero aún así lo que está dentro del do se ejecutará:
```javascript
let numeros = 47;

do{
    console.log(numeros);

    numeros--;
}while(numeros > 77);
```
![[Pasted image 20241014121414.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
