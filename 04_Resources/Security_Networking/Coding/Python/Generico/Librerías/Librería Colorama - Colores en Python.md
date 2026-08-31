---
title: "Librería Colorama - Colores en Python"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta librería sirve para aplicar colores al texto de nuestro código Python, donde podemos definir primero los colores dentro de variables y después utilizarlos cuando queramos de esta forma:
```python
from colorama import Fore, Style

red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
purple = Fore.MAGENTA
reset = Style.RESET_ALL


colors = {'red': red, 'green': green, 'blue': blue, 'yellow': yellow, 'purple': purple, 'reset': reset}


print(colors['red'] + "This text is red." + colors['reset'])
print(colors['green'] + "This text is green." + colors['reset'])
print(colors['blue'] + "This text is blue." + colors['reset'])
print(colors['yellow'] + "This text is yellow." + colors['reset'])
print(colors['purple'] + "This text is purple." + colors['reset'])
```
Y el resultado se vería así:
![[Pasted image 20230201140245.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
