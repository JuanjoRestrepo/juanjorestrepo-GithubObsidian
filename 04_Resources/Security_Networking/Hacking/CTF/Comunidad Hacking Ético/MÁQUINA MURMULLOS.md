---
title: "MÁQUINA MURMULLOS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo con nmap:
![[Pasted image 20231002082556.png]]
Tenemos una plantilla de apache en el puerto 80:
![[Pasted image 20231002082828.png]]
Si hacemos fuzzing web nos encontramos con los siguientes directorios (además de ver que se trata de un wordpress):
![[Pasted image 20231002083037.png]]
Esto hay en el directorio freedom:
![[Pasted image 20231002083106.png]]
Y esto en wp-admin:
![[Pasted image 20231002083130.png]]
Y esto otro por el puerto 6969 (un servicio de telnet):
![[Pasted image 20231002084543.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
