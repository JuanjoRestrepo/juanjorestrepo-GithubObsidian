---
title: "3 - Secuencia de Arranque"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

**PASOS CUANDO ENCENDEMOS EL PC**

1 - Cuando encendemos el PC se ejecuta el firmware (BIOS o UEFI).
2 - El POST se encarga de comprobar que el hardware está bien.
3 - Se busca un cargador de arranque por orden en las unidades que hayamos indicado en la secuencia de arranque del setup.
4 - Si es BIOS se lee la unidad MBR  y aquí se encuentra el código que busca el gestor de arranque.
5 - Si es UEFI, se ejecuta el gestor de arranque que se encuentra en una partición especial (ESP)

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
