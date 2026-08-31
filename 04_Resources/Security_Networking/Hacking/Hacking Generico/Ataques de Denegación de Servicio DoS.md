---
title: "Ataques de Denegación de Servicio DoS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Utilizaremos la web de DVWA de la máquina metasploitable 2:
![[Pasted image 20231207193803.png]]
Y usaremos el módulo de slowloris de metasploit:
![[Pasted image 20231207193844.png]]
Y le cargamos la IP objetivo y el puerto que queramos tirar:
![[Pasted image 20231207193934.png]]
Lanzamos el ataque y vemos que no carga la web:
![[Pasted image 20231207194121.png]]
![[Pasted image 20231207194132.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
