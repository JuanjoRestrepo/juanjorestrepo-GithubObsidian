---
title: "MAQUINA FRIENDLY 1 (Intrusión vía FTP login anonymous y escalada de privilegios sudo -l con VIM)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el reconocimiento de nmap:
![[Pasted image 20230708115833.png]]
Vemos el puerto FTP abierto y con anonymous FTP login allowed abierto, por lo que entramos y vemos un archivo index.html dentro:
![[Pasted image 20230708120006.png]]
Y si analizamos el contenido nos encontramos con que es una plantilla de apache:
![[Pasted image 20230708120101.png]]
La misma que hay en el puerto 80:
![[Pasted image 20230708120113.png]]
Adquirimos el php-reverse-shell.php de pentestmonkey, lo editamos y lo subimos a la máquina víctima vía FTP:
![[Pasted image 20230708120423.png]]
![[Pasted image 20230708120513.png]]
Y ahora si desde la web lo ejecutamos, habremos recibido una reverse shell:
![[Pasted image 20230708120541.png]]
![[Pasted image 20230708120548.png]]
Y si hacemos un sudo -l vemos que podemos ejecutar vim como root:
![[Pasted image 20230708120650.png]]
Por tanto ejecutamos VIM como root:
![[Pasted image 20230708120822.png]]
![[Pasted image 20230708120843.png]]
Y ahora a continuación si damos a enter se habrá guardado lo de antes; y si luego hacemos clic en escape y volvemos a hacer shift y dos puntos para escribir shell, ya nos lanzará una bash de root, por tanto damos a enter y lo tenemos:
![[Pasted image 20230128140352.png]]
Damos a enter y ya somos root:
![[Pasted image 20230708121009.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
