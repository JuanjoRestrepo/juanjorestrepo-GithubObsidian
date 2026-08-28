---
title: "XML External Entity Injection - XXE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para practicar con esta vulnerabilidad vamos a practicar con este proyecto:
![[Pasted image 20230703135534.png]]
Nos lo clonamos:
![[Pasted image 20230703135759.png]]
Y ahora ejecutamos el dockerfile de la siguiente forma:
```bash
docker build -t xxelab .
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
