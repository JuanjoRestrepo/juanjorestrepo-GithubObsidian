---
title: "Concatenar o Pipear Comandos con Tuberías"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esto sirve para que el primer comando sea la entrada del segundo, de tal forma que dos comandos están relacionados entre sí, primero ejecutándose el primero después su salida se convierte en la entrada del segundo:
![[Pasted image 20230128165449.png]]
Podemos hacerlo sobre cualquier comando, por ejemplo sobre un ls para filtrar determinados archivos por el nombre prueba:
![[Pasted image 20230128165550.png]]
Otro ejemplo para listar archivos y luego pipear que sobre ese resultado me lo ordene con sort, para ordenar nombres por orden alfabético en bash:
![[Pasted image 20230128165639.png]]
Otro ejemplo con el fichero /etc/passwd:
![[Pasted image 20230128165711.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
