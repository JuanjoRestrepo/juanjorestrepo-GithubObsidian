---
title: "COMANDO AWK (Para filtrar por columnas en bash)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Sirve para filtrar por columnas en una cadena de texto:
![[Pasted image 20230515150335.png]]
## IMPRIMIR ÚLTIMA COLUMNA
Si queremos imprimir la última columna con awk, utilizaríamos $NF:
![[Pasted image 20230724134645.png]]
Otro ejemplo de cómo imprimir la última columna con awk:
![[Pasted image 20231125134835.png]]
**CONECTAR COLUMNAS**
También podemos conectar unas columnas con otras de la siguiente forma, por ejemplo agregando flechas:
![[Pasted image 20231125134109.png]]

## ESTABLECER UN DELIMITADOR
También podemos establecer un delimitador para que nos cuente a partir de un determinado patrón, por ejemplo de un punto:
![[Pasted image 20230724134758.png]]
Otro ejemplo:
![[Pasted image 20230724135217.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
