---
title: "6 - Extensión Kiwi"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Kiwi es una extensión de Metasploit que permite realizar operaciones orientadas a credenciales, como volcado de contraseñas y hashes, volcado de contraseñas en memoria, generación de golden tickets y mucho más.

------------------------------

Una vez dentro de una sesión de meterpreter y dentro del proceso lsass.exe con metasploit, podemos cargar la extensión Kiwi:
![[Pasted image 20230731190326.png]]
Y con el comando creds_all podemos cargar las credenciales del sistema:
![[Pasted image 20230731190432.png]]
Y con el comando lsa_dump_sam podremos obtener el hash del resto de usuarios:
![[Pasted image 20230731190520.png]]
Y con este otro comando obtenemos credenciales del sistema secretas:
![[Pasted image 20230731190613.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
