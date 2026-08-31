---
title: "7 - Entorno de Pivoting"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Creamos primero las 4 redes que nos harán falta:
```bash
docker network create --subnet=10.10.10.0/24 pivoting1
docker network create --subnet=20.20.20.0/24 pivoting2
docker network create --subnet=30.30.30.0/24 pivoting3
docker network create --subnet=40.40.40.0/24 pivoting4
```
![[Pasted image 20240329093742.png]]
Ahora vamos a importar las distintas máquinas en forma de imágenes con el comando docker load -i:
![[Pasted image 20240410121105.png]]
Y verificamos que tenemos todas las máquinas importadas correctamente:
![[Pasted image 20240410121127.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
