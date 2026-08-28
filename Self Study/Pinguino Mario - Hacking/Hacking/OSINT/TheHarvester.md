---
title: "TheHarvester"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta es la herramienta:
![[Pasted image 20231218183557.png]]
Por ejemplo, podemos hacer una búsqueda sencilla de la siguiente forma:
```bash
theHarvester -d microsoft.com -b bing -l 100
```
Donde:
1. **-d:** Este parámetro especifica el dominio objetivo sobre el cual se realizará la recopilación de información. theHarvester buscará información asociada con este dominio.
    
2. **-b bing:** Este parámetro especifica el motor de búsqueda que theHarvester utilizará para realizar la búsqueda de información. En este caso, se ha seleccionado "bing" como el motor de búsqueda. theHarvester puede utilizar diferentes motores de búsqueda, como Google, Bing, PGP, LinkedIn, etc. Cada motor de búsqueda tiene su propia base de datos y métodos de búsqueda, por lo que el resultado puede variar según el motor seleccionado.
    
3. **-l 100:** Este parámetro indica el límite de resultados que se deben recuperar. En este caso, se ha establecido en 100, lo que significa que theHarvester intentará recuperar hasta 100 resultados.

![[Pasted image 20231218184204.png]]
Podemos probar con otro dominio, como udemy, y vemos que nos encuentra un correo:
![[Pasted image 20231218184343.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
