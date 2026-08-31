---
title: "HERRAMIENTA BASH PARA MOSTRAR TAMAÑO EN BYTES DE ARCHIVOS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```bash
#!/bin/bash

# Obtener la lista de archivos en el directorio actual
archivos=$(ls)

# Recorrer la lista de archivos y mostrar su tamaño en bytes
for archivo in $archivos
do
  # Verificar si es un archivo (no un directorio)
  if [ -f "$archivo" ]; then
    espacio=$(du -b "$archivo" | awk '{print $1}')
    echo "El archivo $archivo ocupa $espacio bytes"
  fi
done
```
![[Pasted image 20230924184218.png]]
Podemos adaptar este script para que se encargue de elimnar aquellos archivos que ocupen más de 1 mb:
```bash
#!/bin/bash

# Obtener la lista de archivos en el directorio actual
archivos=$(ls)

# Recorrer la lista de archivos y mostrar su tamaño en bytes
for archivo in $archivos
do
  # Verificar si es un archivo (no un directorio)
  if [ -f "$archivo" ]; then
    espacio=$(du -b "$archivo" | awk '{print $1}')
    if [ $espacio -gt 1000000 ]; then
        echo "Eliminamos el archivo $archivo, ocupa más de 1 MB"
        rm "$archivo"
    fi
  fi
done
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
