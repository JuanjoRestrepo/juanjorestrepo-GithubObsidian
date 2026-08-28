---
title: "Librería Hashlib"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## GENERAR HASH EN MD5 CON PYTHON
```python
import hashlib

with open("pruebas.py", "rb") as f:
    file_hash = hashlib.md5(f.read()).hexdigest()

print(file_hash)
```
![[Pasted image 20230403145639.png]]
## GENERAR HASH EN SHA1 CON PYTHON
```python
import hashlib

with open("pruebas.py", "rb") as f:
    file_hash = hashlib.sha1(f.read()).hexdigest()

print(file_hash)
```
![[Pasted image 20230403145755.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
