---
title: "5 - Escalada de Privilegios en Ubuntu 12.04"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vamos a ver la versión de ubuntu que estamos utilizando, y vemos que es la 12.04, para ello podemos usar lsb_release -a:
![[Pasted image 20230322020833.png]]
Podemos buscar por internet algún exploit para esta versión de ubuntu, y nos encontramos con un exploit de la web de Exploit-DB:
![[Pasted image 20230322021046.png]]
![[Pasted image 20230322021100.png]]
Nos lo bajamos y lo compartimos con la máquina víctima:
![[Pasted image 20230322021119.png]]
![[Pasted image 20230322021131.png]]
![[Pasted image 20230322021150.png]]
Ahora que ya lo tenemos dentro de la máquina víctima, simplemente tenemos que compilarlo para poder ejecutarlo; y por tanto utilizamos el comando gcc -o escalada 37292.c:
![[Pasted image 20230322021240.png]]
Y ahora sólo tenemos que ejecutar el script de ./escalada y ya somos usuarios root:
![[Pasted image 20230322021308.png]]
Y aquí tenemos la flag de root:
![[Pasted image 20230322021350.png]]
![[Pasted image 20230322021406.png]]

------------------------------------

[[MAQUINA CYBERSPLOIT (Decodificar base64, Inspeccionar código fuente de la página, convertir archivo en binario, escalada de privilegios en Ubuntu 12.04 con exploit de exploitdb overlayfs y compilar exploit en .c con el comando gcc)]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
