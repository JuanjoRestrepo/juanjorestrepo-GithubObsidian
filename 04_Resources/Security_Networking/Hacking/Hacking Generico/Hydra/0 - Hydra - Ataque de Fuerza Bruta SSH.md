---
title: "0 - Hydra - Ataque de Fuerza Bruta SSH"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Por ejemplo vamos a hacer un ataque donde ya sepamos cual es el usuario (el usuario
se llama pi), pero no sabemos cual es la contraseña, por tanto para la contraseña
pondremos -P, entonces lo haremos de esta manera. Y ahora irá probando uno a uno
con el diccionario que le pasemos hasta haber acertado, donde la contraseña es
raspberry:
![[Pasted image 20230323030936.png]]
También puede darse el caso que de a medida que vaya probando intentos que nos lo vaya reportando, por tanto para esto utilizaremos la opción -vV:
![[Pasted image 20230323030943.png]]
![[Pasted image 20230323030946.png]]
También puede darse el caso de que no conozcamos el usuario pero sí la contraseña; y en estos casos pondremos la opción -L en el usuario y en la contraseña le ponemos la p minúscula; y le pasamos el diccionario:
![[Pasted image 20230323030953.png]]
Y ahora nos encontró el usuario:
![[Pasted image 20230323031000.png]]
También podemos quitar la opción de que se nos vaya reportando todo el rato cada intento quitando la opción -vV:
![[Pasted image 20230323031007.png]]
También podemos usar estos otros parámetros:
```bash
hydra -t 64 -l axel -P rockyou.txt ssh://192.168.0.39 -F -I
```
![[Pasted image 20230720160034.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
