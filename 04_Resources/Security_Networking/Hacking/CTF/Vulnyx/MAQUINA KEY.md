---
title: "MAQUINA KEY"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo de nmap, pero vemos que nos encuentra 2 puertos y la intrusión debería ir por otro puerto que no está encontrando:
![[Pasted image 20240107201948.png]]
Esto ocurre porque debemos identificar la IPv6 de la máquina víctima; y para ello ejecutamos el siguiente comando para encontrar todos los equipos conectados dentro de mi red privada pero con su IPv6:
```bash
ping6 -c2 -n -I eth0 ff02::1
```
![[Pasted image 20240107202038.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
