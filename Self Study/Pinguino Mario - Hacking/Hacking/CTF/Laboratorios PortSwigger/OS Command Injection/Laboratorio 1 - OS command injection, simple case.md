---
title: "Laboratorio 1 - OS command injection, simple case"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En algunas interceptaciones HTTP que hagamos con burp suite, es posible que tengamos algún campo para insertar comandos, sobre todo en aquellas webs donde podemos elegir varias opciones y se nos mostrará un dato diferente en función de lo que hagamos, como en este laboratorio de portswigger:
![[Pasted image 20230317185409.png]]
Si interceptamos con burp suite y damos en check stock, nos encontramos con una petición donde vemos que se hace una búsqueda en función del comando que vayamos a utilizar:
![[Pasted image 20230317185507.png]]
En este punto podemos concatenar un comando poniendo un punto y comando después del número que se nos muestra; y lo haríamos de la siguiente forma, donde ya habremos ejecutado un comando en la máquina remota:
![[Pasted image 20230317185626.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
