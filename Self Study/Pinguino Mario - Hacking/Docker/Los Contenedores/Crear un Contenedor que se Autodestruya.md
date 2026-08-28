---
title: "Crear un Contenedor que se Autodestruya"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para ello, a la hora de ejecutar la imagen sólo debo escribir docker run –rm -ti ubuntu bash (por ejemplo) y de esta manera se me abrirá la ventana interactiva de bash pero al salir el contenedor se destruirá:
```bash
docker run --rm -ti ubuntu bash
```
![[Pasted image 20221217105507.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
