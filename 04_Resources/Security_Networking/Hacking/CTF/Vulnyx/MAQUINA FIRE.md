---
title: "MAQUINA FIRE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el reconocimento con nmap:
![[Pasted image 20231002124609.png]]
Podemos iniciar sesión por FTP como anonymous, y nos encontramos con un archivo llamado backup.zip:
![[Pasted image 20231002124707.png]]
Y esto es lo que hay dentro (carpeta llamada firefox y con más archivos dentro):
![[Pasted image 20231002124758.png]]
Utilizamos el comando tree . y vemos un archivo llamado logins.json:
![[Pasted image 20231002125120.png]]
Y esto es lo que tenemos dentro de este archivo logins.json:
![[Pasted image 20231002125156.png]]
Pasamos todos estos archivos al directorio de firefox de mi máquina atacante:
```bash
mv archivos.zip /home/kali/.mozilla/firefox/
```
![[Pasted image 20231002130814.png]]
Borramos todos estos archivos y descomprimimos la carpeta:

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
