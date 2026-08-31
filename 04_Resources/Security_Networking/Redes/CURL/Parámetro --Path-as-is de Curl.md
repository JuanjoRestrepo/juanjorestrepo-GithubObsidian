---
title: "Parámetro --Path-as-is de Curl"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El parámetro --path-as-is evita que curl modifique la URL original y la utiliza tal como se especificó en la línea de comandos. Esto es útil cuando se necesita acceder a un recurso que tiene una URL compleja o no estándar como en el siguiente caso, donde estamos solicitando un archivo interno de la máquina: 
![[Pasted image 20230303024551.png]]
Por ejemplo, si se desea solicitar un recurso con la URL "[http://example.com/my%20path/?query=foo&bar=baz](http://example.com/my%20path/?query=foo&bar=baz)", pero curl modifica la URL automáticamente para que sea "[http://example.com/my%2520path/%3Fquery=foo&bar=baz](http://example.com/my%2520path/%3Fquery=foo&bar=baz)", el uso del parámetro --path-as-is asegura que la solicitud se realiza con la URL original sin modificar.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
