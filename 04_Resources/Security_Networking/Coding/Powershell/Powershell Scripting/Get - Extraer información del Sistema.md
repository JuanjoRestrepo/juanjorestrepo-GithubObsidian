---
title: "Get - Extraer información del Sistema"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hay varios comandos con get que nos sirven para extraer distinto tipo de información.

PARA CONOCER EL HOST:

![[Pasted image 20221217104021.png]]

PARA CONOCER EL PATH ACTUAL DE TRABAJO:

![[Pasted image 20221217104028.png]]
PARA VER LOS PROCESOS QUE SE ESTÁN EJECUTANDO EN EL SISTEMA:

![[Pasted image 20221217104036.png]]
PARA VER LA FECHA ACTUAL:

![[Pasted image 20221217104043.png]]

### EXTRAER CONTENIDO DE UN ARCHIVO

Por ejemplo, si quiero visualizar el contenido de un archivo y aplicar una tubería para que me busque algo, lo haría de esta forma:
```powershell
Get-Content direcciones_ip.txt | Select-String -Pattern "192"
```
![[Pasted image 20230509151233.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
