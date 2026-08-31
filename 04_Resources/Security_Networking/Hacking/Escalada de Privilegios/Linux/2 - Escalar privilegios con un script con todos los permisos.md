---
title: "2 - Escalar privilegios con un script con todos los permisos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Si queremos convertirnos en usuario root directamente, podemos ejecutar el comando su -, y podemos hacerlo dentro del fichero listusers ya que tiene permisos 777:
![[Pasted image 20230306214235.png]]
Lo ejecutamos y ya nos convertimos en usuario root:
![[Pasted image 20230306214257.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
