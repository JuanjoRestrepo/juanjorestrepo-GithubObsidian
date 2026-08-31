---
title: "MAQUINA SAUNA"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este es el reporte de nmap:
![[Pasted image 20240118163703.png]]
![[Pasted image 20240118163822.png]]
Encontramos el dominio EGOTISTICAL-BANK.LOCAL, que podemos añadirlo al /etc/hosts:
![[Pasted image 20240118165043.png]]
En cuanto al puerto 445, no podemos enumerar nada:
![[Pasted image 20240118165244.png]]



Vemos que tiene abierto el puerto 80, por lo que accedemos:
![[Pasted image 20240118163923.png]]
Y vemos un apartado de about con varios usuarios, los cuales los apuntaremos:
![[Pasted image 20240118164158.png]]
![[Pasted image 20240118164249.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
