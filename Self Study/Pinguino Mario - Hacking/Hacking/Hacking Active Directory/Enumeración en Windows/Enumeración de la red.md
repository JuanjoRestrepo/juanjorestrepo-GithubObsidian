---
title: "Enumeración de la red"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## Conocer adaptadores de red y las IPs
![[Pasted image 20230801095816.png]]
## Conocer la dirección mac y más información
```bash
ipconfig /all
```
![[Pasted image 20230801095856.png]]
## Conocer enrutamiento direcciones IP
```bash
route print
```
![[Pasted image 20230801095924.png]]
## Conocer equipos conectados a nuestra red
```bash
arp -a
```
![[Pasted image 20230801095952.png]]
## Conocer puertos abiertos
```bash
netstat -ano
```
![[Pasted image 20230801100023.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
