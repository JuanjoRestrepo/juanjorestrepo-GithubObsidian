---
title: "1 - Instalación de SQL Server"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vamos a la página de Microsoft y nos descargamos la edición express:
![[Pasted image 20230119112325.png]]
Hacemos instalación básica:
![[Pasted image 20230119112439.png]]
Esperamos a que descargue:
![[Pasted image 20230119112511.png]]
Cuando termine la instalación, tendremos una instancia que es la que debemos tener apuntada en caso de querer administrar esta base de datos con algún lenguaje de programación:
![[Pasted image 20230119191053.png]]
No obstante ahora deberíamos instalar también el cliente, para poder controlar la base de datos con interfaz gráfica:
![[Pasted image 20230119191332.png]]
Hacemos un clic y se nos descargará dicho cliente:
![[Pasted image 20230119191358.png]]
Lo instalamos:
![[Pasted image 20230123151253.png]]
Y una vez instalado veremos esta nueva herramienta, en la cual entraremos:
![[Pasted image 20230123151743.png]]
Y ya tenemos todo condigurado por defecto; daremos en connect:
![[Pasted image 20230123151840.png]]
Y ya podemos acceder a las bases de datos, que en este caso son unas del sistema, pero ya podríamos crear las nuestras:
![[Pasted image 20230123151952.png]]
Ahora por último vamos a ver cómo crear un usuario y contraseña en SQL Server, por tanto

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
