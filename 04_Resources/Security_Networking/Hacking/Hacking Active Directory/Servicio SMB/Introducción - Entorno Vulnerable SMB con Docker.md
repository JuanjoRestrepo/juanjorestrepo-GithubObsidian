---
title: "Introducción - Entorno Vulnerable SMB con Docker"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

SMB es un protocolo de red para compartir recursos por la red. Por tanto vamos a desplegar un contenedor de docker con este protocolo que tenga vulnerabilidades:
![[Pasted image 20230420105655.png]]
Lo descargamos:
![[Pasted image 20230420105814.png]]
Y lanzamos el docker compose:
![[Pasted image 20230420110045.png]]
Y vemos que tenemos el contenedor con el samba corriendo por el puerto 445:
![[Pasted image 20230420110130.png]]
# MONTURA DEL RECURSO COMPARTIDO EN NUESTRO EQUIPO
Puede ser interesante montarnos todo el recurso compartido de la máquina víctima en nuestro PC por si queremos analizarlo más cómodamente en caso de tener muchas subcarpetas y subdirectorios. Por tanto podemos jugar con las monturas. Por tanto nos creamos un directorio dentro de /mnt donde vayamos a guardar dicho recurso compartido:
![[Pasted image 20230420111531.png]]
Y ahora con el comando mount vamos a montar este recurso compartido en esta carpeta:
![[Pasted image 20230420111651.png]]
Y ahora damos a intro sin poner contraseña ya que estamos haciendo uso de una null session, pero ya vemos que dentro del directorio mounted tenemos el recurso compartido:
![[Pasted image 20230420111727.png]]
Esto es más cómodo porque podemos ver todo el arbol de archivos, lo cual es muy útil en el caso de que hubiera muchos más archivos:
![[Pasted image 20230420111838.png]]
Si queremos desmontar esto, podemos usar el comando umount:
![[Pasted image 20230420111927.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
