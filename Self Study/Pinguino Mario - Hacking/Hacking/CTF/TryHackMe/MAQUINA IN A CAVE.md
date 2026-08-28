---
title: "MAQUINA IN A CAVE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el reconocimiento con nmap:
![[Pasted image 20230717192747.png]]
Y esto es lo que tenemos en la web:
![[Pasted image 20230717192806.png]]
Y esto por el puerto 3333:
![[Pasted image 20230717192857.png]]
Vamos a hacer fuzzing al puerto 80 en busca de directorios web con gobuster:
![[Pasted image 20230717193236.png]]
Y si hacemos fuzzing de extensiones de archivos, vemos un action.php:
![[Pasted image 20230717194522.png]]
Y vemos que si accedemos al action.php se encuentra en blanco:
![[Pasted image 20230717194645.png]]
Por otra parte, si buscamos estos directorios y cada uno de ellos tiene un código codificado en base64:
![[Pasted image 20230717193426.png]]
Si decodificamos cada uno de los textos, vemos lo siguiente:
![[Pasted image 20230717193652.png]]
Y si establecemos conexiones sobre cada una de estos directorios por el puerto 3333, veremos que si escribo lamp, me saca una serie de archivos:
![[Pasted image 20230717194124.png]]
Vamos a interceptar una petición desde el cuadro inicial con burp suite:
![[Pasted image 20230717195357.png]]
Y esta es la petición interceptada:
![[Pasted image 20230717195422.png]]
Y tenemos que cambiar el content-type y añadir abajo el payload del XXE, por tanto lo modificamos de esta forma:
![[Pasted image 20230717195624.png]]
Y buscamos el payload en la web de payloadsallthethings:
```bash
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection
```
![[Pasted image 20230717195609.png]]
Y este es el resultado, donde podemos explotar un XXE y ver el archivo /etc/hosts:
![[Pasted image 20230717195711.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
