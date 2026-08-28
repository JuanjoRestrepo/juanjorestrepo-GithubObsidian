---
title: "Laboratorio 2 - Basic SSRF against another back-end system"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240404105901.png]]
Interceptamos alguna petición:
![[Pasted image 20240404110152.png]]
Y estamos viendo que se nos está mostrando que la petición se realiza sobre una dirección IP:
![[Pasted image 20240404110232.png]]
Pero podemos intentar llegar a la petición de admin y fuzear el parámetro de la parte de host de la dirección IP:
![[Pasted image 20240404110324.png]]
Vamos al intruduer y fuzzeamos eso:
![[Pasted image 20240404111520.png]]
Y ponemos el listado de números desde el 1 al 255:
![[Pasted image 20240404110458.png]]
Y vemos que nos encuentra la dirección IP 50:
![[Pasted image 20240404112036.png]]
Si enviamos esta petición, vemos el listado de todos los usuarios:
![[Pasted image 20240404112141.png]]
Analizamos el código fuente y vemos la instrucción para eliminar al usuario carlos:
![[Pasted image 20240404112210.png]]
Y usaremos la siguiente instrucción para eliminar a este usuario:
```bash
stockApi=http%3A%2F%2F192.168.0.50%3A8080%2Fadmin%2Fdelete?username=carlos
```
![[Pasted image 20240404112324.png]]
Y habremos resuelto el laboratorio:
![[Pasted image 20240404112359.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
