---
title: "9 - Escalar Privilegios Revisando las Variable de Entorno"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos escalar privilegios revisando las variables de entorno del sistema, ya que es posible que por aquí se guarden contraseñas, por lo que nos encontramos con la contraseña del usuario dylan:
![[Pasted image 20230722165747.png]]
```bash
dylan:bl4bl4Dyl4N
```
Y nos hemos convertido en Dylan:
![[Pasted image 20230722165823.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
