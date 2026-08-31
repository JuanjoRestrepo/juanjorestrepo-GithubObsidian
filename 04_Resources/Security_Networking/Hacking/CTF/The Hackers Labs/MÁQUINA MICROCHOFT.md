---
title: "MÁQUINA MICROCHOFT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este sería el escaneo de nmap:
![[Pasted image 20240404103835.png]]
Vemos abierto el puerto 445, por lo que vamos a utilizar el script vuln de nmap para ver si es vulnerable:
```bash
nmap -p445 -sS --script='vuln'  -vvv -Pn 192.168.0.25
```
Y vemos que sí:
![[Pasted image 20240404104050.png]]
Buscamos este exploit en metasploit y lo encontramos:
![[Pasted image 20240404104122.png]]
Utilizaremos el primero de ellos, donde obtenemos acceso:
```bash
use windows/smb/ms17_010_eternalblue
```
![[Pasted image 20240404104223.png]]
Y ya somos el usuario administrador:
![[Pasted image 20240404104502.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
