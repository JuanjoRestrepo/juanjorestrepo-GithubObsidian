---
title: "Módulo Copy"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

**COPIAR DESDE EQUIPO LOCAL A REMOTO**
Para copiar un fichero desde nuestra máquina local a otra máquina remota, debemos hacer este código y muy importante poner la variable $HOME para que se vaya sustituyendo por el nombre de usuario correspondiente:
![[Pasted image 20230108174340.png]]
**COPIAR UN ARCHIVO DE UNA UBICACIÓN A OTRA DENTRO DEL EQUIPO REMOTO**

Aquí vamos a copiar un archivo de una ubicación a otra dentro de la misma máquina remota:
![[Pasted image 20230108174925.png]]

**PARA ESCRIBIR DENTRO DE UN DOCUMENTO CON ANSIBLE**
Lo haremos de esta manera, utilizando content para indicar el testo y en destino la ruta de dicho documento:
![[Pasted image 20230108175707.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
