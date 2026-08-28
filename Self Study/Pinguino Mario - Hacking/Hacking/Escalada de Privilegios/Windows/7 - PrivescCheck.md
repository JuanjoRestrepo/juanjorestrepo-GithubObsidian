---
title: "7 - PrivescCheck"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Windows PrivescCheck escanea el sistema en busca de diferentes configuraciones, permisos, vulnerabilidades o servicios inseguros que podrían ser explotados para lograr una escalada de privilegios.

```bash
https://github.com/itm4n/PrivescCheck
```

-------------------------

Somos el usuario student:
![[Pasted image 20230801084619.png]]
Y lo ejecutamos con este parámetro:
```bash
powershell -ep bypass -c ". .\PrivescCheck.ps1; Invoke-PrivescCheck"
```
Y en este caso nos encuentra unas credenciales:
![[Pasted image 20230801085233.png]]
Ahora para autenticarnos como el usuario administrador, ejecutaremos el comando runas.exe /user:administrator cmd:
![[Pasted image 20230801085456.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
