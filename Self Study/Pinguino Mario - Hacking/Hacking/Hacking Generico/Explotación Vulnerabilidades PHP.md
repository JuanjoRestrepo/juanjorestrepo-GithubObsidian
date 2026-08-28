---
title: "Explotación Vulnerabilidades PHP"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos intentar acceder al fichero de phpinfo.php para buscar información sobre la versión de php:
![[Pasted image 20230730152658.png]]
O también un whatweb:
![[Pasted image 20230730152724.png]]
Y encontramos el exploit:
![[Pasted image 20230730153124.png]]
Lo ejecutamos y estamos dentro:
![[Pasted image 20230730153204.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
