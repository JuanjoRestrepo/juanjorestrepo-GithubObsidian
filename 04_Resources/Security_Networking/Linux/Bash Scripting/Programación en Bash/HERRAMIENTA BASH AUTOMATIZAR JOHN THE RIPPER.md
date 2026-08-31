---
title: "HERRAMIENTA BASH AUTOMATIZAR JOHN THE RIPPER"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos automatizar ataques con john the ripper desde un script de bash:
```bash
#!/bin/bash

# Comprobar si se proporciona el archivo como argumento
if [ $# -ne 2 ]; then
    echo "Uso: $0 <diccionario> <archivo>"
    exit 1
fi

diccionario=$1
archivo=$2

# Comprobar si el archivo es un .rar
if [[ $archivo == *.rar ]]; then
    echo "Auditoría de archivo .rar con John the Ripper"
    rar2john $archivo > hash
    john --wordlist=$diccionario hash

# Comprobar si el archivo es un .zip
elif [[ $archivo == *.zip ]]; then
    zip2john $archivo > hash
    john --wordlist=$diccionario hash

# Archivo no compatible
else
    echo "El formato del archivo no es compatible"
    exit 1
fi

# Mostrar contraseñas encontradas
echo "Contraseñas encontradas:"
john --show $archivo

rm hash
```
![[Pasted image 20231206113007.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
