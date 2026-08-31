---
title: "Funciones Asíncronas"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Funciona de esta forma:
```python
import asyncio

async def tarea1():
    print("Tarea 1 comenzando...")
    await asyncio.sleep(1) # Espera 1 segundo
    print("Tarea 1 terminada!")

async def tarea2():
    print("Tarea 2 comenzando...")
    await asyncio.sleep(2) # Espera 2 segundos
    print("Tarea 2 terminada!")


# Llamamos ambas tareas de forma asíncrona
tarea_1 = asyncio.create_task(tarea1())
tarea_2 = asyncio.create_task(tarea2())
```
Si lo ejecutamos ocurre lo siguiente:
![[Pasted image 20230529131100.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
