---
title: "Enumerate"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Enumerate es una función incorporada de Python que se utiliza para agregar un contador a un iterable:
```python
nombres = ['Juan', 'María', 'Pedro', 'Ana']
for i, nombre in enumerate(nombres):
    print(i, nombre)
```
Y esta es la salida, donde vemos un número que actúa como índice después de cada valor impreso:
![[Pasted image 20230413113143.png]]
Vemos que la variable i se le va asignando un número y la variable nombre cada uno de los nombres.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
