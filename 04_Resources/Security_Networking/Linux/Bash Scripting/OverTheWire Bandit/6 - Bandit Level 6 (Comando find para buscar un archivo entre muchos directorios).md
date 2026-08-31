---
title: "6 - Bandit Level 6 (Comando find para buscar un archivo entre muchos directorios)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este reto:
![[Pasted image 20230411035859.png]]
Y dentro de la máquina nos encontramos con todos estos directorios:
![[Pasted image 20230411035503.png]]
Por tanto para buscar un archivo que cumpla con estos requisitos, podemos basarnos en el tamaño en bytes de 1033 con el comando find:
![[Pasted image 20230411154809.png]]
Y si ahora hacemos un cat de este documento vemos que ya obtenemos la password P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
![[Pasted image 20230411154844.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
