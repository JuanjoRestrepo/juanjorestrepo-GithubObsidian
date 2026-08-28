---
title: "1 - Desplegar dos contenedores con Docker Compose"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para desplegar más de 1 contenedor a la vez con docker compose, lo hacemos de la siguiente forma:
```bash
version: '3.8'

services:
  
  ubuntu_container:
    image: ubuntu:latest
    command: ["bash", "-c", "sleep 60"]

  fedora_container:
    image: fedora:latest
    command: ["bash", "-c", "sleep 60"]
```
![[Pasted image 20240318103756.png]]
Y si queremos desplegar estos dos contenedores ejecutamos un docker-compose up -d:
```bash
docker-compose up -d
```
Y vemos los dos contenedores desplegados:
![[Pasted image 20240318103839.png]]
Si queremos entrar en alguno de ellos, usamos docker exec:
```bash
docker exec -it 5c /bin/bash
```
![[Pasted image 20240318110326.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
