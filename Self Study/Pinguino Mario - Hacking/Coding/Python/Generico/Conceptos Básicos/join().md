---
title: "join()"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La función join() se utiliza para concatenar elementos de una secuencia en una sola cadena. Por ejemplo aquí digo que inserte un --> entre cada uno de los elementos de la lista:
```python
palabras = ["Hola", "mundo", "Python", "es", "genial"]
frase = "-->".join(palabras)
print(frase)
```
![[Pasted image 20230819162440.png]]
También podemos concatenar elementos pero estableciendo un delimitador, por ejemplo una coma. De esta forma decimos que el elemento que esté entre nombre y nombre sea la coma y un espacio:
```python
nombres = ["Juan", "María", "Carlos", "Ana"]
cadena_nombres = ", ".join(nombres)
print(cadena_nombres)
```
![[Pasted image 20230819162001.png]]
Alternativa a sed de bash:
```python
texto = "Hola, cómo, estás"
nuevo_texto = "->".join(texto.split(", "))
print(nuevo_texto)
```
![[Pasted image 20230819162234.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
