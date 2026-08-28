---
title: "Librería Argparse"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con argparse podemos establecer parámetros en nuestros scripts de python y recibirlos con instrucciones incluidas; por ejemplo de la siguiente forma:
```python
import argparse

# Crea un objeto ArgumentParser
parser = argparse.ArgumentParser(description='Script de prueba')

# Agrega argumentos
parser.add_argument('-nombre', help='Introduce tu nombre')  # Argumento posicional
parser.add_argument('-edad', type=int, help='Introduce tu edad')  # Argumento opcional

# Analiza los argumentos de la línea de comandos
args = parser.parse_args()

# Accede a los valores de los argumentos
nombre = args.nombre
edad = args.edad

# Realiza alguna operación con los argumentos
saludo = f'Hola {nombre}'

if edad:
    saludo += f', tienes {edad} años'

print(saludo)
```
Y este sería el resultado:
![[Pasted image 20230702210450.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
