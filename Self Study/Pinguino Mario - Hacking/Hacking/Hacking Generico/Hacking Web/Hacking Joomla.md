---
title: "Hacking Joomla"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este repositorio de github para montarnos un joomla vulnerable:
![[Pasted image 20230421232906.png]]
Y si nos clonamos el repositorio y levantamos el contenedor, ya tenemos el joomla corriendo por el puerto 8080:
![[Pasted image 20230421233058.png]]
Y ya lo tenemos operativo:
![[Pasted image 20230421233321.png]]
Si queremos enumerar el joomla, tenemos una herramienta que se llama joomscan y podemos acceder a ella desde este repositorio:
![[Pasted image 20230421233507.png]]
Nos lo clonamos:
![[Pasted image 20230421233600.png]]
Y con este comando lanzamos la herramienta para que nos enumere y nos muestre las vulnerabilidades de este joomla:
![[Pasted image 20230421233653.png]]
Y aquí nos encuentra las distintas vulnerabilidades:
![[Pasted image 20230421233743.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
