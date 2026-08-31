---
title: "MD5SUM - Generar Hash md5 de un Archivo"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El comando "md5sum" es una herramienta de línea de comando que se utiliza para generar el valor hash MD5 de un archivo. Se utiliza de la siguiente forma:
![[Pasted image 20230316213042.png]]
También podríamos automatizar esta labor y crear un script de bash que recorra cada uno de los archivos de un directorio y reporte el hash de cada uno de ellos:
```bash
#!/bin/bash

# Obtener la lista de archivos en el directorio actual
files=$(ls)

# Recorrer cada archivo utilizando un bucle for
for file in $files; do
  md5sum $file
done
```
![[Pasted image 20230523153112.png]]
Aunque esto mismo también se podía haber hecho directamente desde la línea de comandos de la siguiente forma:
```bash
variable=$(ls); for file in $variable; do echo $file; done
```
![[Pasted image 20230523153344.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
