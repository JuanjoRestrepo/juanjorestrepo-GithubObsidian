---
title: "2 - Port Forwarding con Docker Compose"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos establecer el reenvío de puertos de la siguiente forma, donde decimos que el puerto 9000 sea el puerto 8000 del contenedor en la parte de ports:
```bash
version: '3.8'

services: # Aquí incluimos los contenedores.
  
  jenkins_contenedor:
    image: jenkins/jenkins
    ports:
     - "9000:8080"

  fedora_container:
    image: fedora:latest
    command: ["bash", "-c", "sleep 60"]
```
![[Pasted image 20240318110039.png]]
Ejecutamos el comando docker-compose up -d y tenemos los dos contenedores funcionando y el de jenkins con el port forwarding:
![[Pasted image 20240318110117.png]]
Y ahora vemos que el port forwarding del jenkins funciona bien y lo tenemos corriendo por el puerto 9000:
![[Pasted image 20240318110142.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
