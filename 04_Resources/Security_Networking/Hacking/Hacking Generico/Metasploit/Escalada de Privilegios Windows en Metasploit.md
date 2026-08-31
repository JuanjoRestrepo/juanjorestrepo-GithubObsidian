---
title: "Escalada de Privilegios Windows en Metasploit"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El primer paso será conseguir una sesión de meterpreter dentro de una máquina windows, por ejemplo en mi caso desde una máquina windows 7:
![[Pasted image 20231118111504.png]]
Pasamos la sesión al segundo plano y utilizamos el siguiente exploit:
![[Pasted image 20231118111557.png]]
Y este exploit se encargará de recolectar distintos exploits para escalar privilegios:
![[Pasted image 20231118111639.png]]
Y nos encuentra exploits válidos y otros que no:
![[Pasted image 20231118111747.png]]
Por ejemplo en nuestro caso vamos a utilizar el siguiente exploit (el último de los que aparecen en color verde):
```
use exploit/windows/local/tokenmagic
```
![[Pasted image 20231118112128.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
