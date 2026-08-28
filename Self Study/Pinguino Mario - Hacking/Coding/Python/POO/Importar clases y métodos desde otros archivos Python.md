---
title: "Importar clases y métodos desde otros archivos Python"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Supongamos que tenemos dos archivos: `clase.py` y `main.py`.

En `clase.py`, definimos una clase llamada `MiClase`:
```python
# clase.py

class MiClase:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        print(f"Hola, soy {self.nombre}")
```
En `main.py`, importamos la clase `MiClase` desde `clase.py` y la utilizamos:
```python
# main.py

from clase import MiClase

# Creamos una instancia de MiClase
objeto = MiClase("ChatGPT")

# Llamamos al método saludar de la instancia
objeto.saludar()
```
Al ejecutar `main.py`, obtendrás la salida:
```python
Hola, soy ChatGPT
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
