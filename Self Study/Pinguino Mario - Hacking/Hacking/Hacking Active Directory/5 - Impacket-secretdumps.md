---
title: "5 - Impacket-secretdumps"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta herramienta sirve para dumpear los hashes de todos los usuarios del dominio utilizando las credenciales de un usuario y contraseña que tengan el permiso para ello:
![[Pasted image 20230425162401.png]]
[[MAQUINA ATTACKTIVE DIRECTORY (enum4linux, kerbrute enumerar usuarios, ASREPRoasting obtener TGT, john the ripper, smbclient para listar recursos compartidos, secredump dumpear hashes y pass the hash)]]

---------------------------

# OTRO EJEMPLO

En caso de tener unas credenciales válidas, podemos usar secretsdump de impacket para listas hashes de usuarios del sistema, y vemos que podemos listar varios de ellos, entre los que se encuentra el del administrador:
![[Pasted image 20230712112250.png]]
Y esta es la contraseña:
```php
c2597747aa5e43022a3a3049a3c3b09d
```
![[Pasted image 20230712112501.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
