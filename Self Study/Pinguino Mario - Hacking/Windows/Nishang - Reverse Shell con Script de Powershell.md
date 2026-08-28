---
title: "Nishang - Reverse Shell con Script de Powershell"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Nishang es un conjunto de scripts de PowerShell diseñados para pruebas de penetración y operaciones de hacking ético en entornos Windows. Uno de los scripts incluidos en Nishang es `Invoke-PowerShellTcp.ps1`, que permite establecer una conexión de shell inversa a través de PowerShell en Windows:
![[Pasted image 20230313020159.png]]
Vamos a analizar el código del Invoke-PowerShellTcp.ps1, donde vemos en la parte de example una demostración de cómo ejecutar la reverse shell hacia la máquina atacante:
![[Pasted image 20230313020307.png]]
Por tanto copiamos justo esta línea y la pegamos al final del todo para que se pueda ejecutar:
![[Pasted image 20230313020404.png]]
Nos ponemos en escucha con netcat desde la máquina atacante:
![[Pasted image 20230313020431.png]]
Y ejecutamos este código y recibimos la reverse shell:
![[Pasted image 20230313020508.png]]
![[Pasted image 20230313020524.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
