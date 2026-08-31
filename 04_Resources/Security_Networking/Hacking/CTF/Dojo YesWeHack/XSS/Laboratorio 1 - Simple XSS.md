---
title: "Laboratorio 1 - Simple XSS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio, donde vemos un input para insertar un dato y se reflejará en la pantalla:
![[Pasted image 20240416122220.png]]
Si escribo Mario, se refleja:
![[Pasted image 20240416122238.png]]
Dando el siguiente resultado:
![[Pasted image 20240416122251.png]]
Pero si insertamos un script de alert, saldrá en la pantalla porque esto no está sanitizado:
```bash
<script>alert(name)</script>
```
![[Pasted image 20240416122330.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
