---
title: "7 - Bandit Level 7 (Comando find para buscar archivos por un determinado dueño de usuario y grupo)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este enunciado:
![[Pasted image 20230411155036.png]]
Entonces dentro de la máquina podemos usar el comando find para buscar archivos que tengan como dueño al usuario bandit7 y de grupo a bandit 6 con el siguiente comando:
![[Pasted image 20230411155933.png]]
Y ahí nos encontró el fichero, por lo que vamos a visualizarlo y vemos la contraseña z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
![[Pasted image 20230411160121.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
