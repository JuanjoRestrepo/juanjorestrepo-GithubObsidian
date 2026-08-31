---
title: "Laboratorio 2 - Blind OS command injection with time delays"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Supongamos que tenemos este panel de rellenar información:
![[Pasted image 20230317190936.png]]
Lo que hay que hacer es interceptar esta petición con burp suite y fijarnos en la parte donde se está enviando la información:
![[Pasted image 20230317191029.png]]
En este punto podemos concatenar un operador lógico para insertar un comando, por ejemplo en el campo de email podemos poner ||, ya que es el operador lógico or; y ahí concatenar un comando, por ejemplo el comando ping, por lo que lo url encodeamos:
![[Pasted image 20230317191538.png]]
Y lo pegamos en la parte donde se transmite la información y con los operadores lógicos:
![[Pasted image 20230317191218.png]]
Ahora esperamos los 10 segundos y vemos que es lo que tarda la página en enviar los datos, porque se está ejecutando primero las 10 trazas ICMP, por lo que tenemos ejecución remota de comandos.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
