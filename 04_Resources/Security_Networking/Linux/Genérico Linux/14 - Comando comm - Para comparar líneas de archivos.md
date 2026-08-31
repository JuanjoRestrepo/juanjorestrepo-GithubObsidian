---
title: "14 - Comando comm - Para comparar líneas de archivos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El comando `comm` en Linux se utiliza para comparar dos archivos de texto línea por línea.

Por ejemplo vamos a trabajar sobre estos dos archivos:
![[Pasted image 20230628124737.png]]

---------------------------

Este comando muestra las líneas que están presentes únicamente en `archivo1.txt`, pero no en `archivo2.txt`.
```bash
comm -23 archivo1.txt archivo2.txt
```
Y este sería el resultado:
![[Pasted image 20230628124830.png]]
Este comando muestra las líneas que están presentes tanto en `archivo1.txt` como en `archivo2.txt`.
```bash
comm -12 archivo1.txt archivo2.txt
```
Y este sería el resultado:
![[Pasted image 20230628124916.png]]
Este comando muestra las líneas que están presentes únicamente en `archivo2.txt`, pero no en `archivo1.txt`, y las líneas comunes se omiten.
```bash
comm -13 archivo1.txt archivo2.txt
```
Y este sería el resultado:
![[Pasted image 20230628125111.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
