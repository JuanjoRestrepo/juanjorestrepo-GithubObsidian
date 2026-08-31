---
title: "0 - Bandit Level 0 (Conectarse por SSH en otro puerto diferente al predeterminado)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En este nivel nos encontramos con esta indicación:
![[Pasted image 20230409214403.png]]
Y así es cómo nos conectamos por ssh en otro puerto diferente al 22, proporcionando el usuario bandit0 y contraseña bandit0 como nos indican en la web:
```bash
 ssh -p 2220 bandit0@bandit.labs.overthewire.org
```
Y ya estamos dentro:
![[Pasted image 20230409214522.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
