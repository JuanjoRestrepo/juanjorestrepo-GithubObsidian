---
title: "Laboratorio 10 - DOM XSS in document.write sink using source location.search inside a select element"
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
![[Pasted image 20240527115226.png]]
En este caso, para resolver el reto tenemos que escaparnos del elemento “select” y llamar a la función alert. Por lo que entramos en alguno de estos productos:
![[Pasted image 20240527115319.png]]
Debajo del todo, hay una función para comprobar el stock de cada producto:
![[Pasted image 20240527115349.png]]
Si observamos el código fuente de la web, podemos ver el siguiente código javascript:
![[Pasted image 20240527115423.png]]
Analizando un poco el script, básicamente se entiende que además de las tres ciudades por defecto para comprobar el stock, se le puede agregar una más a través de la variable storeIdde la URL. Por lo que podemos probar a añadir esa variable y un valor cualquiera:
![[Pasted image 20240527115801.png]]
Y ya hemos conseguido añadir una nueva categoría:
![[Pasted image 20240527115822.png]]
Yendo al código fuente, confirmamos que efectivamente se ha implementado este cambio:
![[Pasted image 20240527115914.png]]
Por lo que, observando esto, podemos intentar poner un valor que ocasione que nos escapemos del propio elemento options, y ejecute un alert:
```bash
</option><script>alert('XSS')</script>//
```
Y ha funcionado:
![[Pasted image 20240527120053.png]]
Y ya hemos resuelto el laboratorio:
![[Pasted image 20240527120108.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
