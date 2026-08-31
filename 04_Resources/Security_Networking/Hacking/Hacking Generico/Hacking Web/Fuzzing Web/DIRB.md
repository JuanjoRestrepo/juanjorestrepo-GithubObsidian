---
title: "DIRB"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos utilizar dirb si queremos encontrar también extensiones de rutas. Es una herramienta de enumeración de directorios para identificar archivos y directorios ocultos en un sitio web. Funciona enviando solicitudes HTTP a un servidor web e dentificando posibles rutas de acceso:
![[Pasted image 20230210132531.png]]
Ahora otro ejemplo pero con un dominio, y vemos que funciona igual y nos encuentra varios directorios:
![[Pasted image 20230218082716.png]]
Y vemos que la ruta assets existe:
![[Pasted image 20230218082751.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
