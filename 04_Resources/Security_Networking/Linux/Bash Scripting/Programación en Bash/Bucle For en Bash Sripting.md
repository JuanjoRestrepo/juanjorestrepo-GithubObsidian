---
title: "Bucle For en Bash Sripting"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Ejemplo con números:
```bash
#!/bin/bash

for i in {1..5}
do
  echo -n "$i "
done
echo
```
Ahora ejemplo con cadenas de texto:
```bash
#!/bin/bash

frutas=("manzana" "naranja" "plátano" "pera" "uva")

for fruta in "${frutas[@]}"
do
  echo "Me gusta la $fruta"
done
```
Iterar sobre archivos de un directorio e imprimir sus nombres o hacer cualquier acción sobre cada uno de ellos:
```bash
#!/bin/bash

for archivo in /ruta/a/directorio/*
do
  echo "Nombre de archivo: $archivo"
done
```
Leer líneas de un archivo y mostrarlas en pantalla:
```bash
#!/bin/bash

archivo="ruta/al/archivo.txt"

for linea in $(cat "$archivo")
do
  echo "$linea"
done
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
