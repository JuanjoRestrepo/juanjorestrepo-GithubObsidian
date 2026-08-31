---
title: "Iniciar Sesión con Credenciales SMB con psexec en Metasploit"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Utilizamos un ataque de fuerza bruta contra el protocolo smb y obtenemos las credenciales:
```bash
use auxiliary/scanner/smb/smb_login
```
![[Pasted image 20230730161556.png]]
Podemos usar el módulo de psexec para iniciar sesión con dichas credenciales:
```bash
use exploit/windows/smb/psexec
```
![[Pasted image 20230730161744.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
