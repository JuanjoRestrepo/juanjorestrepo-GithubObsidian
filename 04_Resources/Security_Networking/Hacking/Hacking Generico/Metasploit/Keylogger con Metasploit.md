---
title: "Keylogger con Metasploit"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Una vez establecida la sesión de meterpreter, migramos al proceso de explorer:
![[Pasted image 20230802102812.png]]
Y arrancamos el keyscan_start:
![[Pasted image 20230802102759.png]]
Ahora escribimos algo dentro de la máquina víctima:
![[Pasted image 20230802102857.png]]
Y si desde la máquina atacante iniciamos el keyscan_dump, habremos capturado el texto:
![[Pasted image 20230802102931.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
