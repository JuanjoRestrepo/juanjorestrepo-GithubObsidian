---
title: "MAQUINA ANUBIS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Haremos los escaneos de nmap de siempre:
![[Pasted image 20230318091055.png]]
Cuando estamos ante una máquina Active Directory, debemos obtener información a nivel de dominio; y para ello podemos utilizar enum4linux:
![[Pasted image 20230318091602.png]]
Y ya hemos encontrado el nombre del dominio, que se llama WINDCORP:
![[Pasted image 20230318091641.png]]
Por tanto vamos a añadir este dominio al fichero /etc/host, para que funcione la resolución DNS:
![[Pasted image 20230318091804.png]]
Dentro del puerto 593 pudimos ver en nmap que corría un servicio web HTTP, por lo que vamos a probar en acceder:

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
