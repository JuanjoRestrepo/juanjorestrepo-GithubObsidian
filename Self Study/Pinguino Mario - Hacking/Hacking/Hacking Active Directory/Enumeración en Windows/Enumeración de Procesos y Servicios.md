---
title: "Enumeración de Procesos y Servicios"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# Como enumerar procesos de windows
```bash
ps
```
![[Pasted image 20230801101300.png]]
O también podemos enumerar procesos con el comando net start:
![[Pasted image 20230801101455.png]]
# Conocer PID de un proceso
```bash
pgrep explorer.exe
```
![[Pasted image 20230801101332.png]]
O también podemos ver los PID de todos los procesos con el siguiente comando:
```bash
wmic ervice list brief
```
![[Pasted image 20230801101552.png]]
# Migrar a un proceso
```bash
migrate 2176
```
![[Pasted image 20230801101356.png]]
# Enumerar tareas programadas
```bash
tasklist /SVC
```
![[Pasted image 20230801101626.png]]
O también tenemos este otro comando:
```bash
schtasks /query /fo LIST
```
![[Pasted image 20230801101703.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
