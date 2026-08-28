---
title: "HERRAMIENTA BASH PARA ELIMINAR ARCHIVOS DUPLICADOS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para poder eliminar archivos duplicados en linux, tenemos una herramienta llamada fdupes, mediante la cual podemos detectar archivos que sean iguales, por ejemplo de la siguiente forma:
![[Pasted image 20231103153809.png]]
Y ahora podemos usar la herramienta fdupes dentro del script:
```bash
#!/bin/bash

# Comprobar si fdupes está instalado
if ! command -v fdupes &> /dev/null
then
    echo "fdupes no está instalado. Por favor, instálalo para usar este script."
    exit 1
fi

# Buscar y mostrar los archivos duplicados en el directorio actual
archivos=$(fdupes -r . | sed 's/^..//')

# Eliminar los archivos duplicados de manera interactiva
echo "$archivos" | while read -r line; do
    rm "$line"
done
```
Por ejemplo tenemos estos archivos repetidos:
![[Pasted image 20231103154614.png]]
Y ahora ya no lo hay:
![[Pasted image 20231103160043.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
