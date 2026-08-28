---
title: "Librería Subprocess en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La librería `subprocess` de Python permite interactuar con procesos del sistema operativo, ejecutar comandos en la línea de comandos y obtener su salida. Aquí te dejo algunos ejemplos básicos de cómo usar esta librería:
### Ejecutar un comando en la línea de comandos y obtener su salida:
```python
import subprocess

# Ejecutar el comando "ls" y obtener su salida
output = subprocess.check_output(['ls'])
print(output)
```
### Ejecutar un comando con argumentos:
```python
import subprocess

# Ejecutar el comando "ls -l" y obtener su salida
output = subprocess.check_output(['ls', '-l'])
print(output)
```
### Ejecutar un comando en segundo plano:
```python
import subprocess

# Ejecutar el comando "sleep 10" en segundo plano
subprocess.Popen(['sleep', '10'])
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
