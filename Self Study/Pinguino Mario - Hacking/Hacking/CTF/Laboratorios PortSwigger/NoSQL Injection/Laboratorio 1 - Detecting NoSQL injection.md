---
title: "Laboratorio 1 - Detecting NoSQL injection"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240325134910.png]]
Si vamos a la categoría de gifts, vemos que en la url se establece un category=gifts:
![[Pasted image 20240325135327.png]]
Y si colamos una comilla, se nos muestra el siguiente mensaje de error donde vemos que estamos ante una base de datos MondoDB:
![[Pasted image 20240325135402.png]]
Viendo esto, podemos establecer un operador lógico OR con Gifts'||1||' y se nos muestra todo el contenido de la base de datos:
![[Pasted image 20240325135554.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
