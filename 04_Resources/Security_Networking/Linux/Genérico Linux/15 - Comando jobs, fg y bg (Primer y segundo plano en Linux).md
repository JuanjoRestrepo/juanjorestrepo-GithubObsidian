---
title: "15 - Comando jobs, fg y bg (Primer y segundo plano en Linux)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Linux, los comandos `fg` (foreground) y `bg` (background) se utilizan para controlar la ejecución de procesos en una terminal.

-------------------------

# FG

Ejecutamos un comando en primer plano, lo suspendemos con control +x y luego con el cmoando fg lo volvemos a reanudar y pasarlo al primer plano:

![[Pasted image 20230709113922.png]]
# BG

Si queremos pasar al segundo plano un proceso, podemos primero pausarlo con control + x y luego con el comando bg lo pasamos al segundo plano, de tal forma que podremos ir haciendo otras cosas mientras se ejecuta el comando:
![[Pasted image 20230709114111.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
