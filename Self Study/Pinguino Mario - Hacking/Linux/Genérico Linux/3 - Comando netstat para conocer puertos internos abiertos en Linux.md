---
title: "3 - Comando netstat para conocer puertos internos abiertos en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para ver qué servicios están corriendo detrás de un puerto específico en Linux, puedes utilizar el comando netstat y su opción -tulpn. El uso del comando es el siguiente:
```bash
sudo netstat -tulpn
```
Este comando mostrará una lista de todas las conexiones activas en el sistema, incluyendo el protocolo de red (TCP o UDP), la dirección IP local y remota, el puerto local y remoto, y el nombre del programa o proceso que está escuchando en ese puerto:
![[Pasted image 20230211011227.png]]
Para filtrar los resultados y ver solo los servicios corriendo en un puerto específico, puedes utilizar el comando grep junto con netstat:
```bash
sudo netstat -tln | grep :80
```
Y nos encuentra el servicio que está corriendo sobre el puerto 80:
![[Pasted image 20230218141725.png]]
## SERVICIO CORRIENDO EN PUERTO INTERNO
Vamos a ver cómo podemos hacer que un servicio esté corriendo por un puerto interno pero que no esté expuesto.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
