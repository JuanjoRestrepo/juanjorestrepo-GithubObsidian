---
title: "1 - Proceso Lsass"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

LSASS mantiene una base de datos de cuentas de usuario locales y de dominio y gestiona su acceso y permisos. También administra la creación y eliminación de cuentas y contraseñas de usuario. Por ejemplo podemos obtener hashes de los usuarios:
![[Pasted image 20230731090942.png]]
![[Pasted image 20230731090952.png]]
Si quisiéramos crackear estos hashes, podemos poner el metasploit en segundo plano y ejecutar el siguiente módulo:
```bash
use exploit/windows/http/badblue_passthru
```
![[Pasted image 20230801130130.png]]
Establecemos un diccionario:
```bash
set CUSTOM_WORDLIST /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt
```
Y lo ejecutamos:
![[Pasted image 20230801130227.png]]
![[Pasted image 20230801130238.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
