---
title: "HERRAMIENTA BASH AUTOMATIZAR CRACKING CON JOHN THE RIPPER"
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

if [ $# -ne 2 ]; then
    echo "Uso: <archivo> <wordlist>"
    exit 1
fi

input_file=$1
wordlist=$2

# Determinar el formato y generar el hash
case "$input_file" in
    *.kdbx)
        keepass2john "$input_file" > hash
        ;;
    *.rar)
        rar2john "$input_file" > hash
        ;;
    *.zip)
        zip2john "$input_file" > hash
        ;;
    *)
        echo "Formato no compatible"
        exit 1
        ;;
esac

# Intentar crackear la contraseña
john --wordlist="$wordlist" hash

# Mostrar resultados
john --show hash

# Limpieza: Eliminar archivos temporales
rm hash
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
