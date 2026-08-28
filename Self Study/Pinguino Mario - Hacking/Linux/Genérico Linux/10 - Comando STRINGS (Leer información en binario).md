---
title: "10 - Comando STRINGS (Leer información en binario)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El comando "strings" es una herramienta de línea de comandos en Linux que se utiliza para buscar y extraer cadenas de caracteres legibles en archivos binarios, lo que puede ser útil para analizar el contenido de un archivo en busca de información importante, como contraseñas, nombres de usuario, direcciones IP, etc.

--------------------------------------------------

Por ejemplo tenemos este archivo con información en binario:
![[Pasted image 20230312013526.png]]
Lo podemos leer con el comando strings:
![[Pasted image 20230312013748.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
