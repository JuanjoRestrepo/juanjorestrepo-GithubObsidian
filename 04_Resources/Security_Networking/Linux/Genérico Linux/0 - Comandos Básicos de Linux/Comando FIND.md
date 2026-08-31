---
title: "Comando FIND"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este comando sirve para encontrar tipos de archivos, por ejemplo vamos a buscar todos los archivos de forma recursiva en mi actual directorio (sólo archivos):
![[Pasted image 20230127070953.png]]
![[Pasted image 20230127071022.png]]
Para buscar un determinado archivo en mi actual directorio con bash lo haría de esta forma:
![[Pasted image 20230127071206.png]]
Incluso con el comando find también podemos indicar que nos haga una búsqueda desde un directorio en concreto, por ejemplo un find desde el directorio raíz buscando en todo el sistema la palabra password:
![[Pasted image 20230210015416.png]]
Y nos encuentra muchos patrones con esta palabra:
![[Pasted image 20230210015440.png]]
También puedo buscar un archivo con un determinado nombre desde la raíz, por ejemplo uno que se llame user.txt:
![[Pasted image 20230507114726.png]]
## SCRIPT PARA AUTOMATIZAR LA BÚSQUEDA DE ARCHIVOS
```bash
#!/bin/bash

# Verificar que se proporcionaron los parámetros adecuados
if [ $# -ne 2 ]; then
    echo "Uso: $0 <ruta> <nombre_archivo>"
    exit 1
fi

# Recoger los parámetros
ruta="$1"
nombre_archivo="$2"

# Buscar el archivo en la ruta especificada
echo "Buscando el archivo '$nombre_archivo' en la ruta '$ruta'..."

# Utilizar el comando 'find' para buscar el archivo
resultado=$(find "$ruta" -name "$nombre_archivo")

# Verificar si se encontraron resultados
if [ -n "$resultado" ]; then
    echo "Se encontraron los siguientes archivos:"
    echo "$resultado"
else
    echo "No se encontraron archivos con el nombre '$nombre_archivo' en la ruta '$ruta'."
fi
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
