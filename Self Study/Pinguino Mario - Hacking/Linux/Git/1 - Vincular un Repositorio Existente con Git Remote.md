---
title: "1 - Vincular un Repositorio Existente con Git Remote"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será inicializar un repositorio local con el comando git init:
![[Pasted image 20230108122519.png]]
Y a continuación pegamos el link del repositorio con el comando git remote y especificando el nombre de la carpeta que creamos antes:
![[Pasted image 20230108122526.png]]
Para comprobar que la conexión se realizó correctamente podemos usar el comando git remote -v:
![[Pasted image 20230108122532.png]]
Para descargar el contenido del repositorio usaremos el comando git fetch y el nombre que pusimos antes:
![[Pasted image 20230108122539.png]]
Pero para recibir de verdad los archivos debemos utilizar un git pull nombre_carpeta main:
![[Pasted image 20230108122548.png]]

# PRIMER PASO

El primer paso será crear el repositorio dentro de nuestro git bash con el comando git init:
![[Pasted image 20230108122611.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
