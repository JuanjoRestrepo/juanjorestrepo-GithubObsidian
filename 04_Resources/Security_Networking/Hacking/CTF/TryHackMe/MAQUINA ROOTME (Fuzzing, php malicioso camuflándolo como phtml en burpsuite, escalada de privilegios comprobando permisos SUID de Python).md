---
title: "MAQUINA ROOTME (Fuzzing, php malicioso camuflándolo como phtml en burpsuite, escalada de privilegios comprobando permisos SUID de Python)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Haremos los reconococimientos de nmap y vemos el puerto 80 y 22 abiertos:
![[Pasted image 20230401011056.png]]
Si vemos la web es esta:
![[Pasted image 20230401011433.png]]
Si hacemos fuzzing nos encontramos con un directorio de panel y otro de uploads:
![[Pasted image 20230401011851.png]]
En el directorio de panel tenemos un lugar donde subir archivos:
![[Pasted image 20230401011932.png]]
Si subimos un fichero .php malicioso nos va a dar error, pero el truco será en interceptar la petición web y así poder cambiar la extensión del fichero php por un phtml:
```python
<?php
        echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
?>
```
![[Pasted image 20230401013139.png]]
Y entonces ahora podremos subirlo y llamar a este archivo para obtener ejecución remota de comandos:
![[Pasted image 20230401013213.png]]
![[Pasted image 20230401013225.png]]
Ahora nos creamos un servidor web con python que aloje el código para enviarnos una reverse shell y después lo llamamos y pipeamos con curl:
![[Pasted image 20230401014657.png]]
![[Pasted image 20230401014615.png]]
![[Pasted image 20230401014628.png]]
![[Pasted image 20230401014638.png]]
Si hacemos una búsqueda de los permisos SUID, vemos que Python se encuentra entre ellos:
![[Pasted image 20230401015128.png]]
Y también vemos estos permisos para Python:
![[Pasted image 20230401015233.png]]
Por tanto nos creamos un fichero de Python con un código que nos permita escalar privilegios:
![[Pasted image 20230401015723.png]]
Lo compartimos con la máquina víctima:
![[Pasted image 20230401015746.png]]
Y lo ejecutamos para convertirnos en root:
![[Pasted image 20230401015812.png]]
![[Pasted image 20230401015823.png]]
[[13 - Escalada de Privilegios con Python]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
