---
title: "MAQUINA APPOINTMENT (GOBUSTER y CREDENCIALES SQL EN WEB)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Es posible que dentro del puerto 80 de una máquina esté corriendo un servicio SQL, tal y como podemos ver este caso si usamos nmap:
![[Pasted image 20221218150508.png]]
Ahora para acceder a los directorios de una web, debo utilizar gobuster. Por ejemplo, si accedo a la IP de la máquina objetivo a través del navegador, voy a acceder a esta pantalla:
![[Pasted image 20221218150515.png]]
Pero con gobuster puedo navegar por los distintos directorios dentro de esta web insertando este comando seguido de la IP de la máquina:
![[Pasted image 20221218150523.png]]
Y nos encuentra estos directorios dentro de la web, entre los que tenemos el directorio de htpasswd. En este caso no es relevante usar gobuster porque podemos acceder a la flag de otras maneras, pero es interesante ver en este ejemplo el funcionamiento de gobuster:
![[Pasted image 20221218150530.png]]
## ELUDIR LOGIN SQL EN SERVIDOR WEB:
Para eludir muchos tipos de login de sql podemos usar la táctica de poner ese usuario y la contraseña root:
![[Pasted image 20221218150543.png]]
![[Pasted image 20230328133358.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
