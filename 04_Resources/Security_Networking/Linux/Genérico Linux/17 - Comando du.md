---
title: "17 - Comando du"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este comando sirve para obtener información de un archivo, así como lo que ocupa; y esta es su sintaxis básica:
```bash
du -h user.txt
```
![[Pasted image 20230922125502.png]]
Podemos formatear con regex el tamaño de un archivo de esta forma:
```bash
tamaño=$(du -h user.txt | awk '{print $1}')
echo "El archivo user.txt ocupa $tamaño"
```
![[Pasted image 20230922125737.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
