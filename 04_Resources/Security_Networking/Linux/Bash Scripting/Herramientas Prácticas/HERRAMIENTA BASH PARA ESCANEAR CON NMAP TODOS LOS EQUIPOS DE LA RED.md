---
title: "HERRAMIENTA BASH PARA ESCANEAR CON NMAP TODOS LOS EQUIPOS DE LA RED"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo hacemos con el siguiente script:
```bash
#!/bin/bash

arp-scan -I eth0 --localnet | grep -v "ip" |  grep -v "Starting" | grep -v "pa" | grep -v "Interface" | grep -v "Ending" | awk '{print $1}' | tr -d ' ' > ip.txt

while read -r linea; do
    echo -e "\e[38;5;11mEscaneando con nmap la dirección $linea\e[0m"

    nmap -p- -sS -sC -sV --min-rate=5000 -n -Pn $linea -oN "escaneo_$linea.txt"

done < ips.txt
rm ips.txt
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
