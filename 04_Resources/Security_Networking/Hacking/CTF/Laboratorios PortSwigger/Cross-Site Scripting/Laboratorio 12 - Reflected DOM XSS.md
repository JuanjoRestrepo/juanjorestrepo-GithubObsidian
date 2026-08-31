---
title: "Laboratorio 12 - Reflected DOM XSS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este sería el laboratorio:
![[Pasted image 20240529193457.png]]
Y tenemos un buscador:
![[Pasted image 20240529193543.png]]
Ponemos algo en el buscador y lo interceptamos con burp suite:
![[Pasted image 20240529193702.png]]
Tras enviar esta petición, se nos viene la siguiente:
![[Pasted image 20240529193749.png]]
Si enviamos esta petición, vemos que el servidor nos devuelve un json:
![[Pasted image 20240529193828.png]]
Pero podemos ver lo que hemos escrito dentro de la respuesta:
![[Pasted image 20240529194120.png]]
Visto esto, lo que vamos a hacer es escapar el JSON para inyectar el XSS, donde usaremos el siguiente payload:
```bash
test\"-alert(1)}//
```
![[Pasted image 20240529194530.png]]
Enviamos la petición y ha funcionado:
![[Pasted image 20240529194553.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
