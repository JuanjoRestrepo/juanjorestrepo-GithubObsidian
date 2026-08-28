---
title: "MAQUINA WAVE"
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
![[Pasted image 20230925085221.png]]
Y esta sería la página web:
![[Pasted image 20230925085249.png]]
Hacemos fuzzing para descubrir directorios ocultos y vemos un robots.txt:
![[Pasted image 20230925085425.png]]
Donde nos vuelve a llevar al mismo directorio backup:
![[Pasted image 20230925085449.png]]
![[Pasted image 20230925085506.png]]
Y nos los descargamos todos:
![[Pasted image 20230925085729.png]]
Convertimos este archivo a formato phar y extraemos su contenido con el comando phar:
```bash
phar extract -f weevely.phar
```
![[Pasted image 20230925090319.png]]
Y aquí vemos el contenido:
![[Pasted image 20230925090342.png]]
Con crackstation podemos probar en crackear estos hashes:
![[Pasted image 20230925090620.png]]
Y vemos que nos saca una contraseña:
![[Pasted image 20230925090636.png]]
```bash
aaazz
```
Una vez en este punto, hay que tener en cuenta que weevely se trata de una herramienta en kali para generar una backdoor en php:
![[Pasted image 20230925090856.png]]
Por tanto, viendo esto, es posible que dentro de esta máquina exista alguna backdoor en php llamada weevely, pero para ello tendremos que ir probando distintas extensiones:
![[Pasted image 20230925091224.png]]
![[Pasted image 20230925091346.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
