---
title: "len()"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La función len() en python sirve para obtener la longitud de una secuencia, por ejemplo de la siguiente forma:
```python
lista = [1, 2, 3, 4, 5]
longitud_lista = len(lista)
print("La longitud de la lista es:", longitud_lista)
```
![[Pasted image 20230819161455.png]]
Lo mismo ocurre si queremos medir la longitud de un diccionario, donde contará como uno solo cada clave y valor:
```python
diccionario = {'a': 1, 'b': 2, 'c': 3}
longitud_diccionario = len(diccionario)
print("La longitud del diccionario es:", longitud_diccionario)
```
![[Pasted image 20230819161559.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
