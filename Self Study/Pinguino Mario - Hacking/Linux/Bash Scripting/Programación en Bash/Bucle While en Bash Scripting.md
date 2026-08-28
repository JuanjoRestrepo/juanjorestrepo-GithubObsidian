---
title: "Bucle While en Bash Scripting"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Iterar por líneas en un bucle while:
```bash
while read -r linea; do
    echo $linea
done < "archivo.txt"
```
![[Pasted image 20230927125812.png]]
También podemos recibir un documento como parámetro y leer línea por línea su contenido:
```bash
#!/bin/bash

documento="$1"

while read -r linea; do
    echo $linea
done < "$documento"
```
![[Pasted image 20230927125759.png]]
También podemos automatizar muchas cosas usando un bucle while, como por ejemplo filtrar por códigos de estado de distintas peticiones http con curl:
```bash
while read -r url; do
    respuesta=$(curl -s -o /dev/null -w "%{http_code}" "$url")
 
    if [ "$respuesta" == "200" ]; then
        echo "En $url hay respuesta con código de estado $respuesta"
    fi
done < "texto.txt"

```
![[Pasted image 20230927131003.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
