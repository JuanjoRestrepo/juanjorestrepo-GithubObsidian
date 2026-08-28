---
title: "MAQUINA EXPERIENCE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo con nmap:
![[Pasted image 20240123093622.png]]
Como vemos el puerto 445 abierto y que se trata de una máquina windows xp, vamos a ver mediante el script vuln de nmap si esta máquina es vulnerable o no:
```bash
nmap -p445 --script=vuln 192.168.0.54
```
![[Pasted image 20240123093714.png]]
Buscamos este exploit con metasploit:
![[Pasted image 20240123093834.png]]
Lo seleccionamos y lo lanzamos:
![[Pasted image 20240123094612.png]]
![[Pasted image 20240123094655.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
