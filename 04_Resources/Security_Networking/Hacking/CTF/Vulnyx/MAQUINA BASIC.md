---
title: "MAQUINA BASIC"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el reconocimiento con nmap:
![[Pasted image 20231102101526.png]]
Y esto corre por el puerto 80:
![[Pasted image 20231102101618.png]]
Y esto por el puerto 631:
![[Pasted image 20231102101641.png]]
Y en la parte de las impresoras encontramos al usuario dimitri:
![[Pasted image 20231102101727.png]]
Por lo que hacemos un ataque de fuerza bruta por el puerto 22 con el usuario dimitri:
```bash
hydra -l dimitri -P /usr/share/wordlists/rockyou.txt ssh://192.168.0.47
```
La encuentra:
![[Pasted image 20231223122258.png]]
Y accedemos vía ssh:
![[Pasted image 20231102102124.png]]
Hacemos una búsqueda de binarios y vemos el de /env:
![[Pasted image 20231102102328.png]]
Por tanto miramos en gtfobins y tenemos unas instrucciones:
![[Pasted image 20231102102352.png]]
Lo ejecutamos y ya somos root:
![[Pasted image 20231102102405.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
