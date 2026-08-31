---
title: "4 - Comando test -f para comprobar existencia de ficheros"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos comprobar si un fichero existe o no utilizando el comando test -f de esta forma:
```bash
#!/bin/bash

# Verificar si el archivo script_bellisimo.py existe y es un archivo regular

if test -f script_bellisimo.py; then
  echo "El archivo existe"
else
  echo "El archivo no existe"
fi
```
Y este es el resultado:
![[Pasted image 20230211021925.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
