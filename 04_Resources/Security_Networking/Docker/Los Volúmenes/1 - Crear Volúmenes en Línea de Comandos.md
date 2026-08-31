---
title: "1 - Crear Volúmenes en Línea de Comandos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Los volúmenes sirven para almacenar información de manera persistente en uno o varios contenedores. Es útil para que los archivos ya estén integrados en el propio contenedor y podamos disponer de dichos archivos en diferentes contenedores diferentes.

Hay una serie de volúmenes que docker ya tiene creados para que pueda funcionar, que ya vienen creados:
![[Pasted image 20221231200400.png]]
También puedo crear un volumen escribiendo docker volume create, y ahora veremos que está creado:
![[Pasted image 20221231200415.png]]
Y esto sería para eliminarlo:
![[Pasted image 20221231200426.png]]
La idea de los volúmenes es crearlos para que en los contenedores se guarde cierta información en ellos, de esta manera la información se guardará en los volúmenes y no perderemos datos.

Para vincular un directorio del contenedor con el volumen de hacemos de esta manera:
![[Pasted image 20221231200439.png]]
Ahora voy a crear un documento txt en el directorio home:
![[Pasted image 20221231200449.png]]
Ahora si creo otro contenedor diferente, por ejemplo uno de Fedora, y le cargo este volumen, veremos como en este otro contenedor se mantiene el fichero hola.txt:
![[Pasted image 20221231200505.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
