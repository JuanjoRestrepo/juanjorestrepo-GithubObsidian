---
title: "Laboratorio 4 - Blind OS command injection with out-of-band interaction"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente panel donde debemos darle en submit feedback:
![[Pasted image 20240121214748.png]]
Rellenamos esta información e interceptamos la petición con burp suite:
![[Pasted image 20240121214838.png]]
Recibimos lo siguiente:
![[Pasted image 20240121215148.png]]
Una vez interceptada la petición debemos ir a burp y a esta opción:
![[Pasted image 20240121215622.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
