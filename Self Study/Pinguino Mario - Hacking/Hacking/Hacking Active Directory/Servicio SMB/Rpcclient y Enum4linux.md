---
title: "Rpcclient y Enum4linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos conectarnos a recursos compartidos de una máquina windows con esta herramienta, por ejemplo de la siguiente forma:
```bash
rpcclient -U "" 192.168.0.136
```
![[Pasted image 20230729131319.png]]
Y aquí tenemos una serie de comando útiles para extraer información:
## COMANDO HELP
![[Pasted image 20230729131354.png]]
# COMANDO SRVINFO
Nos muestra información del sistema:
![[Pasted image 20230729131514.png]]
# ENUMERAR GRUPOS Y USUARIOS
![[Pasted image 20230729131539.png]]
![[Pasted image 20230729131612.png]]
# ENUM4LINUX
Podemos también hacer un análisis de la máquina windows a través del puerto 445 con esta herramienta, por lo que usamos el siguiente comando:
```
enum4linux 192.168.171.136 -A
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
