---
title: "2 - Named Pipe Impersonation"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Un _**named pipe**_ es una técnica que tiene el sistema operativo _**Windows**_ para facilitar la comunicación entre procesos. Por lo que, si se mira desde el punto de vista de un _**pentester**_, ésta puede ser utilizada para lograr un objetivo como el de ejecutar un código en un contexto privilegiado.

--------------------

Por ejemplo, si intentamos acceder a la flag, vemos que no tenemos permisos y debemos escalar privilegios:
![[Pasted image 20230731094326.png]]
Y con el comando load incognito y después list_tokens -u podemos ver que el token del usuario administrador está disponible:
![[Pasted image 20230731094619.png]]
Y con el comando impersonate_token podemos pasar a ser el usuario administrador:
![[Pasted image 20230731094805.png]]
Y ya accedemos dentro del directorio del usuario administrador:
![[Pasted image 20230731094845.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
