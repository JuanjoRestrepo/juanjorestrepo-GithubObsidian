---
title: "2- Contenedores con Direccionamientos Diferentes"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos crear una red y hacer que dos contenedores tengan un direccionamiento distinto de tal forma que no tengan conexión entre sí:
```bash
docker network create --subnet 192.168.1.0/24 --gateway 192.168.1.1 red_nueva
```
![[Pasted image 20240302103242.png]]
Y a continuación lanzamos un contenedor asignándole esta red:
```bash
docker run --network=b6 -it 3d
```
De tal forma que podremos ver como se le asigna una IP dentro de rango de la red creado anteriormente:
![[Pasted image 20240302103345.png]]
Ahora vamos a crear otra red distinta que sea 192.168.30.0/24:
```bash
docker network create --subnet 192.168.30.0/24 --gateway 192.168.30.1 otra_red
```
![[Pasted image 20240302103618.png]]
Entonces vamos a crear un nuevo contenedor y le vamos a asignar esta otra red:
```bash
docker run --network=b6 -it 3d
```
![[Pasted image 20240302103721.png]]
Y si miramos la IP de este otro contenedor, será una dentro del redireccionamiento 192.168.30.0/24:
![[Pasted image 20240302103811.png]]
Y si hacemos un ping desde este contenedor a alguna de las otras IPs del contenedor, no debería de haber conexión:
![[Pasted image 20240302103906.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
