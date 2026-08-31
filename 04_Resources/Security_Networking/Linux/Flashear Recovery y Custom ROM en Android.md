---
title: "Flashear Recovery y Custom ROM en Android"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero tenemos que tener fastboot instalado:
```bash
apt install fastboot
```
![[Pasted image 20240524144750.png]]
El siguiente paso será tener un recovery y una ROM:
![[Pasted image 20240524144825.png]]
Entramos en modo fastboot en el Android y lo conectamos al PC, donde ejecutamos el siguiente comando:
```bash
fastboot flash recovery recovery.img
fastboot boot recovery.img
```
![[Pasted image 20240524165923.png]]
Y ahora instalamos la ROM:
![[Pasted image 20240524165941.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
