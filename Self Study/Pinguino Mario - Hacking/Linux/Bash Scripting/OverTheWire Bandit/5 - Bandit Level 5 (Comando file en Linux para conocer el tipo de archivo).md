---
title: "5 - Bandit Level 5 (Comando file en Linux para conocer el tipo de archivo)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este reto:
![[Pasted image 20230410100325.png]]
Tenemos todos estos archivos dentro de la máquina:
![[Pasted image 20230410100811.png]]
Con el comando file podemos ver qué tipo de archivo es cada uno de ellos, además de usar un comodín para verlos todos:
![[Pasted image 20230410100914.png]]
Pero vemos que el file07 es de tipo ASCII, es decir, que está en formato de texto y podríamos visualizarlo sin problemas; y así es como obtenemos la contraseña lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
![[Pasted image 20230410101032.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
