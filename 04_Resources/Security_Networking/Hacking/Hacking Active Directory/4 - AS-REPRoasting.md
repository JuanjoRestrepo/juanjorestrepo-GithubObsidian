---
title: "4 - AS-REPRoasting"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Es una técnica que consiste en encontrar usuarios que no requieren pre-autenticación de Kerberos. Lo cual significa que cualquiera puede enviar una petición AS_REQ en nombre de uno de esos usuarios y recibir un mensaje AS_REP correcto. Esta respuesta contiene un pedazo del mensaje cifrado con la clave del usuario, que se obtiene de su contraseña. Para ello podemos usar una herramienta que se llama GetNPUsers.py usándola de la siguiente forma:

Por ejemplo podríamos encontrar este tipo de usuarios utilizando [[Kerbrute]]
![[Pasted image 20230425154919.png]]

----------------------------------------

**OPCIÓN 1 ->** Proporcionando un diccionario de usuarios, por ejemplo dentro del diccionario users:
![[Pasted image 20230126114019.png]]
**OPCIÓN 2 ->** Proporcionando un único usuario que hayamos podido encontrar anteriormente:
![[Pasted image 20230425155219.png]]

[[MAQUINA ATTACKTIVE DIRECTORY (enum4linux, kerbrute enumerar usuarios, ASREPRoasting obtener TGT, john the ripper, smbclient para listar recursos compartidos, secredump dumpear hashes y pass the hash)]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
