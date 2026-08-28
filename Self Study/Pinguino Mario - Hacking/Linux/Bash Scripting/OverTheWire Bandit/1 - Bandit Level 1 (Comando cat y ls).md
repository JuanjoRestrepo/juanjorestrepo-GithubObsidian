---
title: "1 - Bandit Level 1 (Comando cat y ls)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este reto:
![[Pasted image 20230409214640.png]]
Y dentro de la máquina tenemos un archivo llamado readme donde nos obliga a usar el comando ls para localizarlo y el comando cat para leer su contenido, el cual es la contraseña NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL:
![[Pasted image 20230409214732.png]]
Ahora nos conectamos por ssh poniendo esta contraseña pero con el usuario bandit1:
```bash
ssh -p 2220 bandit1@bandit.labs.overthewire.org
```
Y ya estamos dentro:
![[Pasted image 20230409214930.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
