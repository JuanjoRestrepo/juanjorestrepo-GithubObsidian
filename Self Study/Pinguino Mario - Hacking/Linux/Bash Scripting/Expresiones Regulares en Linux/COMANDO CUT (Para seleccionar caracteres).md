---
title: "COMANDO CUT (Para seleccionar caracteres)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Sirve para cortar determinados caracteres de una cadena de texto, por ejemplo podemos mostrar la primera letra, o hasta la segunda o la tercera:
![[Pasted image 20230216214547.png]]
O podemos mostrar solo la tercera letra por ejemplo:
![[Pasted image 20230216214606.png]]
También podemos mostrar un rango de caracteres, desde el primero al décimo:
![[Pasted image 20231125135105.png]]
O desde el dígito cuarto al décimo:
![[Pasted image 20231125135126.png]]
Aunque hay que entender que cut extrae los dígitos de todas las líneas, por ejemplo aquí tenemos la prueba en un archivo de dos líneas extrayendo los dígitos 4 al 10:
![[Pasted image 20231125135242.png]]
Aunque también podemos filtrar por columnas si marcamos un símbolo delimitador. Por ejemplo en este caso podemos hacer que utilice la coma como referencia y luego nos imprima la segunda columna:
![[Pasted image 20230515150754.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
