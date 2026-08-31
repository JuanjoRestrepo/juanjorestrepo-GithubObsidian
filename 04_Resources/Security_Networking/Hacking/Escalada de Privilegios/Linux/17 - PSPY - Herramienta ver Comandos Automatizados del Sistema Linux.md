---
title: "17 - PSPY - Herramienta ver Comandos Automatizados del Sistema Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos una herramienta llamada pspy que sirve para ver todos los comandos que se ejecutan en segundo plano en el sistema, lo cual es muy útil por si encontramos alguno que nos pueda ayudar a elevar los privilegios:
![[Pasted image 20230426151045.png]]
![[Pasted image 20230426151529.png]]
![[Pasted image 20230426151540.png]]
Y vemos todo lo que nos reporta:
![[Pasted image 20230426151558.png]]
Aunque también podemos ejecutar el comando pc -eo user,command y veremos los comandos que se ejecutan:
![[Pasted image 20230426151827.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
