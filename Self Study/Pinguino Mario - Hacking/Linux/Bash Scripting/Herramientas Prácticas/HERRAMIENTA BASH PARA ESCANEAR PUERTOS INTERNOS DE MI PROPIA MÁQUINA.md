---
title: "HERRAMIENTA BASH PARA ESCANEAR PUERTOS INTERNOS DE MI PROPIA MÁQUINA"
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

# Ejecutar el comando netstat para obtener una lista de puertos abiertos
open_ports=$(netstat -tln | awk '{print $4}' | tr -d "Local" | tr -d "(ny" | sed 's/:/ /g' | awk '{print $2}')

# Mostrar los puertos abiertos
echo "Puertos abiertos: $open_ports"
```
Y por ejemplo si corremos dos servidores web con Python, podremos luego comprobar el buen funcionamiento de esta herramienta:
![[Pasted image 20230218142330.png]]
![[Pasted image 20230218142343.png]]
Y ahora si lanzamos el script, nos detecta estos dos puertos que están en uso:
![[Pasted image 20230218142406.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
