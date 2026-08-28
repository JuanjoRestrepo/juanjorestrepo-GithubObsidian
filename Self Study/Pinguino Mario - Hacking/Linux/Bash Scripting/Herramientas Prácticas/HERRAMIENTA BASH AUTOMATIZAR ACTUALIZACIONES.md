---
title: "HERRAMIENTA BASH AUTOMATIZAR ACTUALIZACIONES"
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

read -p "Escribe 'actualizar' si quieres actualizar, y 'salir' si quieres salir: " decision

if [ "$decision" = "actualizar" ]; then
    apt update
    apt upgrade -y
    apt autoremove -y
    apt autoclean
    echo "¡Actualización completada!"
elif [ "$decision" = "salir" ]; then
    exit
else
    echo "Opción no válida"
fi
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
