---
title: "5 - Comando CHOWN para Cambiar Propietarios de Ficheros en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Linux, el comando `chown` se utiliza para cambiar el propietario de un archivo o directorio. Para cambiar el propietario de un archivo, se hace de la siguiente forma:
```bash
sudo chown nuevo_propietario archivo
```
Por tanto, por ejemplo tenemos este archivo de python:
![[Pasted image 20230216164054.png]]
Y ahora vemos que el propietario de este archivo pasa a ser mario:
![[Pasted image 20230216164120.png]]
Hay que entender que el nombre de la izquierda es el usuario propietario y el nombre de la derecha el grupo:
```bash
-rw-r--r-- 1 usuario grupo  25 Feb 16 15:30 archivo.txt
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
