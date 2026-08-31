---
title: "trap finish SIGINT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta sentencia establece una acción que se debe tomar cuando el script recibe la señal SIGINT, que se produce cuando el usuario presiona la combinación de teclas "Ctrl + C" en la terminal:
```bash
#!/bin/bash

function finish {
    echo "Finalizando el script"
    exit
}

trap finish SIGINT

echo "Presiona Ctrl + C para interrumpir el script"

while true; do
    sleep 1
done
```
Y este sería el resultado:
![[Pasted image 20230414120320.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
