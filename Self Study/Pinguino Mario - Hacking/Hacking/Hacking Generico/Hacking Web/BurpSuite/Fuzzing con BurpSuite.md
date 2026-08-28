---
title: "Fuzzing con BurpSuite"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos hacer fuzzing con burpsuite de la misma forma que lo haríamos con gobuster, wfuzz, etc, lo haríamos de esta forma; yendo al intruder:
![[Pasted image 20230728114128.png]]
Añadimos donde queremos hacer el ataque:
![[Pasted image 20230728114349.png]]
Y en la ventana de payloads añadimos los términos para hacer el fuzzing o cargar un diccionario dentro de load:
![[Pasted image 20230728114422.png]]
Y si damos en start attack, empezará el ataque:
![[Pasted image 20230728114549.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
