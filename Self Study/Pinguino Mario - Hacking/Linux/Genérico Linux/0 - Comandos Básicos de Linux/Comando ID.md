---
title: "Comando ID"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El comando "id" es una herramienta de línea de comandos en Linux que se utiliza para mostrar información de identidad de usuario y grupo, como en este caso, que podemos ver los grupos a donde pertenece el usuario que somos:
![[Pasted image 20230312014537.png]]
En este caso se puede ver que pertenecemos al usuario sudo, por lo que podemos ejecutar este comando y elevar nuestros privilegios:

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
