---
title: "3 - Crear Volúmenes con Docker Compose - Instrucción COPY"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Si queremos vincular un directorio de mi máquina host con un directorio del contenedor utilizando docker compose, tenemos que utilizar la siguiente instrucción (y así también se hace para copiar archivos dentro del contenedor. Con Docker Compose no se usa la instrucción COPY):
```bash
version: '3.8'

services: # Aquí incluimos los contenedores.
  
  fedora_container:
    image: fedora:latest
    command: ["bash", "-c", "sleep 60"]
    volumes:
      - /home/kali/Desktop/volumen_fedora:/home
```
![[Pasted image 20240318110621.png]]
De esta forma, si dentro del directorio /home del contenedor de fedora creamos un archivo, veremos como también se habrá creado dentro de la máquina anfitrión:
![[Pasted image 20240318110650.png]]
![[Pasted image 20240318110659.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
