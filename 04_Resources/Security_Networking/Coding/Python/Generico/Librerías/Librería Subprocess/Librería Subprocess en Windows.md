---
title: "Librería Subprocess en Windows"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para ejecutar un comando utilizando la biblioteca `subprocess` de Python en Windows, se puede utilizar la siguiente sintaxis:
### EJECUTAR UN COMANDO
```python
import subprocess

# Ejecutar el comando "dir" en la consola de Windows
subprocess.run("dir", shell=True)
```
### EJECUTAR UN COMANDO CON PARÁMETROS
Si queremos ejecutar un comando con parámetros, lo haríamos de la siguiente manera (por ejemplo el comando ipconfig all):
```python
import subprocess

# Ejecutar el comando "ipconfig /all" en la consola de Windows
subprocess.run(["ipconfig", "/all"], shell=True)
```
### CAPTURAR EN UNA VARIABLE EL OUTPUT DE UN COMANDO
También es posible capturar la salida del comando utilizando el parámetro `capture_output`. Por ejemplo:
```python
import subprocess

# Ejecutar el comando "dir" en la consola de Windows y capturar la salida
result = subprocess.run("dir", shell=True, capture_output=True, text=True)

# Obtener la salida del comando
output = result.stdout

# Imprimir la salida del comando
print(output)
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
