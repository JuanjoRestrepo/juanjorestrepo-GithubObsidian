---
title: "HERRAMIENTA BASH PARA DETECTAR PUERTOS ABIERTOS DE UNA IP"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos crear un script para detectar puertos abiertos de un hos, utilizando la herramienta de netcat para ir haciendo ping a un determinado puerto:

```bash
#!/bin/bash

finish() {
    echo -e "\n[*] Cerrando el script..."
    exit 0
}

trap finish SIGINT

read -p "Introduce la IP: " ip_address

if [ "$ip_address" ]; then
    for port in $(seq 1 65535); do
        (echo > /dev/tcp/$ip_address/$port) 2>/dev/null && echo "[*] Puerto $port - Abierto" &
    done
    wait
fi
```
Y este sería el resultado:
![[Pasted image 20230414120042.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
