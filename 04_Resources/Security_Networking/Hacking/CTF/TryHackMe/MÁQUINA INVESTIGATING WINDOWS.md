---
title: "MÁQUINA INVESTIGATING WINDOWS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Nos encuentra estos puertos abiertos:
![[Pasted image 20240416114426.png]]
![[Pasted image 20240416114444.png]]
![[Pasted image 20240416114453.png]]
Para conectarnos por RDP tenemos que ejecutar el siguiente comando usando la herramienta xfreerdp:
```bash
xfreerdp /u:Administrator /p:letmein123! /v:10.10.142.238:3389
```
![[Pasted image 20240416114636.png]]
![[Pasted image 20240416114643.png]]
Si vamos a configuración y a la parte de about, vemos la versión de windows:
![[Pasted image 20240416114852.png]]
Ahora para saber qué usuarios se han logueado previamente, tenemos que abrir el event viewer, yendo a la parte de windows logs y viendo que el usuario administrator fue el último en loguearse:
![[Pasted image 20240416115129.png]]
Si nos preguntan información de un usuario, por ejemplo cuando fue la última vez que inició sesión, debemos de usar el comando net user john:
![[Pasted image 20240416115430.png]]
Para enumerar más cuentas, usamos el comando net user:
![[Pasted image 20240416115637.png]]
Si nos preguntan por las cuentas con permisos de administrador, usamos el comando net localgroup Administrators:
![[Pasted image 20240416115919.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
