---
title: "Iniciar, Reiniciar y Detener Contenedores"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

**RENOMBRAR**
Para renombrar un contenedor, escribo docker rename nombre_actual nombre_nuevo:
```bash
docker rename quirky_khayyam linux
```
![[Pasted image 20221217105215.png]]
**DETENER SIN ELIMINAR**
Escribimos docker stop id_contenedor:
![[Pasted image 20221217105221.png]]
**PARA REANUDAR EL CONTENEDOR**
Ponemos docker start id_contenedor:
![[Pasted image 20221217105228.png]]
**PARA REINICIAR EL CONTENEDOR**
Ponemos docker restart id_contenedor:
![[Pasted image 20221217105234.png]]
**COMO INGRESAR A UN CONTENEDOR**
Ponemos docker exec -ti nombre_contenedor bash (para entrar dentro del contenedor usando una terminal bash):
![[Pasted image 20221217105246.png]]
Para acceder con permisos root:
![[Pasted image 20221217105253.png]]
**Eliminar todos los contenedores de Docker a la vez**
Para eliminar todos los contenedores de docker a la vez, ejecutaremos este comando:
```bash
docker rm $(docker ps -a)
```
![[Pasted image 20230108200952.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
