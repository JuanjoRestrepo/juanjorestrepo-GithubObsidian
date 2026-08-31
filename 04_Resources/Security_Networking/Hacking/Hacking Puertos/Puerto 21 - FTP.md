---
title: "Puerto 21 - FTP"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

### Modo Activo (Active Mode)

En el modo activo, el cliente inicia la conexión al servidor en el puerto 21 (puerto de comandos). Cuando se necesita transferir datos (por ejemplo, al listar un directorio o transferir un archivo), el servidor abre una conexión desde su puerto 20 (puerto de datos) al puerto especificado por el cliente. Los pasos son:

1. El cliente se conecta al servidor en el puerto 21 y envía el comando `PORT` junto con el número de puerto en el que está escuchando.
2. El servidor se conecta al cliente desde el puerto 20 al puerto especificado por el cliente para transferir datos.

### Modo Pasivo (Passive Mode)

En el modo pasivo, el cliente inicia tanto la conexión de comandos como la de datos. Esto es útil cuando el cliente está detrás de un firewall o NAT que bloquea conexiones entrantes. Los pasos son:

1. El cliente se conecta al servidor en el puerto 21 y envía el comando `PASV`.
2. El servidor responde con una dirección IP y un puerto en el que está listo para recibir la conexión de datos.
3. El cliente se conecta a ese puerto para transferir datos.

### Comando `passive off`

Cuando usas el comando `passive off` en un cliente FTP, estás instruyendo al cliente que use el modo activo para las conexiones de datos. Es decir, el cliente enviará el comando `PORT` en lugar de `PASV` y esperará que el servidor se conecte de vuelta a su puerto de datos.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
