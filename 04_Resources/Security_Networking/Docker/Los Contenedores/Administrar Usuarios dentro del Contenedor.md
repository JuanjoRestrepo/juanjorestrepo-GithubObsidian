---
title: "Administrar Usuarios dentro del Contenedor"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Puedo crear un usuario en el Dockerfile como hice anteriormente y luego ejecutar la terminal con ese mismo usuario:
![[Pasted image 20221217110720.png]]
Después de crear la imagen, ahora si ejecuto un terminal el usuario mario aparecerá en el prompt:
![[Pasted image 20221217110727.png]]

¿Pero qué ocurre cuando tenemos dos usuarios y unas veces quiero ejecutar el contenedor con un usuario y otra veces con el otro?

Primero monto la imagen que tenga por ejemplo dos usuarios:

![[Pasted image 20221217110735.png]]

Una vez añadidos dos usuarios al contenedor, a la hora de ejecutar el contenedor puedo elegir con qué usuario se va a ejecutar:

![[Pasted image 20221217110747.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
