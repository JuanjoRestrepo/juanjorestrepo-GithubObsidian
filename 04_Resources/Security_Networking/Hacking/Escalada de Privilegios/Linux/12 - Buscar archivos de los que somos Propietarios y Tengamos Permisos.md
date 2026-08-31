---
title: "12 - Buscar archivos de los que somos Propietarios y Tengamos Permisos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos lanzar este comando que sirve para ver qué archivos con extensión .sh son propiedad del usuario que somos (en este caso svc_acc); y vemos que hay uno que se llama ssh-alert.sh:
![[Untitled 1 3.png]]
Y vemos que tenemos los permisos para ejecutar este script:
![[Untitled 2 3.png]]
## Ver si tenemos permisos de append sobre un script
Aunque sí tenemos el permiso de añadir algo, un append:
![[Untitled 3 1.png]]
Por tanto hacemos un append de esta manera, donde esto se añadirá al final del script:
![[Untitled 4 1.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
