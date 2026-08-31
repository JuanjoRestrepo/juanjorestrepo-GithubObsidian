---
title: "13 - Configurar Base de datos mongodb"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para que la información persista, debemos de crear la base de datos desde fuera y transferir el .json con la información a la máquina víctima, donde ejecutaremos el siguiente comando:
```bash
mongoimport --db accesos --collection usuarios --file accesos.usuarios.json --jsonArray
```
![[Pasted image 20240516135933.png]]
Y ya lo tendremos importado:
![[Pasted image 20240516135951.png]]
Si lo queremos configurar en docker, debemos de establecer así el dockerfile para que la información de la base de datos persista:
```Dockerfile
FROM mongo:latest

COPY accesos.usuarios.json /opt

CMD service ssh start && \
    service mariadb start && \
    service apache2 start && \
    mongod --bind_ip_all --quiet & \   
    sleep 10 && \    
    mongoimport --db accesos --collection usuarios --file /opt/accesos.usuarios.json --jsonArray && \
    rm /opt/accesos.usuarios.json && \
    tail -f /dev/null
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
