---
title: "7 - PATH DE LINUX - Para que se un comando se ejecute con solo poner el nombre"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Linux, el PATH es una variable de entorno que contiene una lista de directorios separados por dos puntos (:), donde el sistema busca los programas y comandos ejecutables cuando se escribe un comando en la terminal en cualquiera de las siguientes ubicaciones:
![[Pasted image 20230218135938.png]]
Por ejemplo, si el directorio /usr/local/bin está incluido en el PATH, y hay un archivo ejecutable llamado "actualizar.sh" en ese directorio, se puede ejecutar ese programa desde cualquier directorio en la terminal simplemente escribiendo el nombre del programa:
![[Pasted image 20230218140121.png]]
### AÑADIR DIRECTORIO AL PATH DE LINUX
No obstante, también podemos añadir un directorio determinado dentro del path de Linux exportando una variable de entorno de la siguiente forma:
![[Pasted image 20230218140428.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
