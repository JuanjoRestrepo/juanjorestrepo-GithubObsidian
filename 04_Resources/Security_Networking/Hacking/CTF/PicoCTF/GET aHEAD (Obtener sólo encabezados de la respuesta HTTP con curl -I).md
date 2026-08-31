---
title: "GET aHEAD (Obtener sólo encabezados de la respuesta HTTP con curl -I)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos esta web:
![[Pasted image 20230307081841.png]]
Donde si hacemos un curl nos proporciona su contenido HTML:
![[Pasted image 20230307081911.png]]
Pero podemos utilizar el parámetro -I de curl para obtener sólo los encabezados de la respuesta HTTP para una URL determinada. En otras palabras, el parámetro -I solicita solo la información de encabezado de una respuesta HTTP y no el cuerpo de la respuesta; y aquí obtenemos la flag:
![[Pasted image 20230307081957.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
