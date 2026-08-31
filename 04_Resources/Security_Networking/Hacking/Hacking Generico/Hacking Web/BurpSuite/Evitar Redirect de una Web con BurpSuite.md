---
title: "Evitar Redirect de una Web con BurpSuite"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para impedir un redirect, podemos usar burpsuite:
![[Pasted image 20230327072152.png]]
Entonces lo que vamos a hacer es indicar de interceptar la respuesta con burpsuite, y de esta forma podremos ver y manipular ese redirect:
![[Pasted image 20230327072342.png]]
Hacemos clic en forward y nos encontramos con el redirect, el cual podemos manipular y poner /admin:
![[Pasted image 20230327072436.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
