---
title: "Laboratorio 8 - Stored XSS into anchor href attribute with double quotes HTML-encoded"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240524181438.png]]
En este caso, en el laboratorio se nos indica que para resolver el laboratorio tenemos que escribir un comentario que llame a la función alert cuando se haga click en el nombre del autor del comentario. Por lo que entramos en alguno de los artículos; y vemos que hay un lugar de comentarios:
![[Pasted image 20240524181533.png]]
Escribimos cualquier cosa:
![[Pasted image 20240524181858.png]]
Y vemos nuestro comentario:
![[Pasted image 20240524181915.png]]
Y además vemos como en nuestro comentario hay un hipervínculo:
![[Pasted image 20240524182003.png]]
Ese enlace se relaciona con el apartado de website, por lo que insertamos el siguiente payload para que quede almacenado:
```bash
javascript:alert(1)
```
![[Pasted image 20240524182110.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
