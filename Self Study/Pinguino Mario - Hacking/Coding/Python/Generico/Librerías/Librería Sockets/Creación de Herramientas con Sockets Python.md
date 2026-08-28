---
title: "Creación de Herramientas con Sockets Python"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# ESCANER DE PUERTOS CON SOCKET

Un escaner de los puertos internos de mi máquina:

```python
import socket

ip = '192.168.0.3'
puertos_lista = [21,22,80,443]
  

for puerto in puertos_lista:

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    resultado = sock.connect_ex((ip, puerto))

    print(puerto, ":", resultado)
    sock.close()
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
