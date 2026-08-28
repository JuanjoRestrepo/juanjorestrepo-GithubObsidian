---
title: "2 - Bandit Level 2 (Leer archivo con nombre de guión en Linux)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Se nos presenta este reto:
![[Pasted image 20230409215603.png]]
Y dentro de la máquina nos encontramos con un archivo que es un guión:
![[Pasted image 20230409215629.png]]
Si lo intentamos leer con el comando cat no va a funcionar:
![[Pasted image 20230409215653.png]]
Por tanto si preguntamos a la inteligencia artificial, nos propone una solución, que sería utilizar el comando cat ./- de esta manera:
![[Pasted image 20230409215803.png]]
Lo probamos y funciona, ya tenemos la contraseña rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi:
![[Pasted image 20230409215821.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
