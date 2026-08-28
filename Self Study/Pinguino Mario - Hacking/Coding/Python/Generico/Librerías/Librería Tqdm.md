---
title: "Librería Tqdm"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta librería de python sirve para establecer una barra de progreso dentro de un script, de la siguiente manera:
```python
from tqdm import tqdm
import time

# Crear una barra de progreso para un bucle for
for i in tqdm(range(10)):
    time.sleep(0.1)
```
![[Pasted image 20230917121851.png]]
Vamos a ver otro ejemplo:
```python
from tqdm import tqdm
import time

# Supongamos que tienes una lista de elementos con la que quieres trabajar.
elementos = range(100)

# Crea una barra de progreso con tqdm.
for elemento in tqdm(elementos, desc="Procesando", unit="elemento"):
    # Simula alguna tarea que lleva tiempo.
    time.sleep(0.1)

print("Proceso completado")
```
![[Pasted image 20231025164448.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
