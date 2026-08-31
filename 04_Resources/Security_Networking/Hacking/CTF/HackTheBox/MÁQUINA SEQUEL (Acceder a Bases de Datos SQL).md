---
title: "MÁQUINA SEQUEL (Acceder a Bases de Datos SQL)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En esta máquina se está corriendo un servicio de MySQL dentro del puerto 3306:
![[Pasted image 20230509115021.png]]
INICIAR SESIÓN BASE DE DATOS SIN CREDENCIALES:
Para iniciar sesión en una base de datos usamos la opción -u y podemos usar el usuario root para iniciar sesión sin la contraseña, para ello voy a usar docker para ejecutar mysql y desde ahí lanzo el comando mysql -h 10.129.95.232 -u root para entrar dentro de la base de datos del host de destino:
![[Pasted image 20230509115037.png]]
Para ver las bases de datos:
![[Pasted image 20230509115047.png]]
Elegimos la base de datos que queramos extraer la información:
![[Pasted image 20230509115055.png]]
Para ver las tablas:
![[Pasted image 20230509115103.png]]
Y dentro de config tenemos la flag:
![[Pasted image 20230509115112.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
