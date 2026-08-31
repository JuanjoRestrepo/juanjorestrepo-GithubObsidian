---
title: "2 - Copiar Archivos SCP con SSH"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## Para descargar archivos del servidor
Lo haremos con scp utilizando este comando, primero poniendo la IP del servidor desde donde queremos bajarnos el archivo, y luego la ruta de nuestra máquina local donde lo queramos descargar:
![[Pasted image 20230119184948.png]]
## Para subir archivos al servidor
Vamos a subir este archivo:
![[Pasted image 20230119185202.png]]
Para ello ejecutamos el siguiente comando:
![[Pasted image 20230119185251.png]]
Y ya lo tenemos subido:
![[Pasted image 20230119185308.png]]
## Para subir una carpeta entera por SSH
Si queremos subir todos los archivos que estén dentro de una carpeta, lo haríamos de esta forma; aquí tenemos la carpeta:
![[Pasted image 20230119185522.png]]
Y con este comando lo subiríamos todo, ya que con el asterisco indicamos que suba la totalidad de archivos, y con la opción -r que sea recursivo:
![[Pasted image 20230119190046.png]]
Y aquí están:
![[Pasted image 20230119190103.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
