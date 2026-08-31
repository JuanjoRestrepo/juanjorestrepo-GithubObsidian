---
title: "MAQUINA IGNITE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo con nmap:
![[Pasted image 20230910110754.png]]
Y esta es la web:
![[Pasted image 20231103153039.png]]
Y en la parte de abajo de esta web vemos que hay unas credenciales por defecto dentro del directorio /fuel:
![[Pasted image 20231103153356.png]]
Y tenemos un panel de login, donde probamos con admin:admin:
![[Pasted image 20231103153459.png]]
Donde tenemos el siguiente entorno:
![[Pasted image 20231103153532.png]]
Hacemos fuzzing web y encontramos el directorio assets:

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
