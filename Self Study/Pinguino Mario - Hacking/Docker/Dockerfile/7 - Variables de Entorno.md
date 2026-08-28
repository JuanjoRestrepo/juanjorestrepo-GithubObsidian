---
title: "7 - Variables de Entorno"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Las variables de entorno son aquellas variables que podemos acceder desde cualquier parte del contenedor, (por ejemplo la variable prueba sería una variable de entorno:

![[Pasted image 20221217110647.png]]

Después, si construyo la imagen y entro a ella, existirá una variable de entorno que será $prueba, que contendrá 1234, ya que lo he definido dentro del Dockerfile:

![[Pasted image 20221217110654.png]]

También puedo crear una variable de entorno directamente cuando ejecuto el contenedor, sin necesidad de modificar el Dockerfile, lo haría de esta manera:

![[Pasted image 20221217110701.png]]

Y si entro dentro de este contenedor y miro el valor de la variable2 que acabamos de crear, veremos que existe y con el valor que le hemos asignado:

![[Pasted image 20221217110707.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
