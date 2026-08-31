---
title: "HERRAMIENTA BASH PARA BUSCAR ARCHIVOS EN TODO EL SISTEMA LINUX"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vamos a crear un buscador de archivos en bash, que nos pida el nombre del archivo que queramos buscar y nos los busque:
Incluso con el comando find también podemos indicar que nos haga una búsqueda desde un directorio en concreto, por ejemplo un find desdeel directorio raíz buscando en todo el sistema la palabra password:
```bash
find / | grep "password"
```
![[Pasted image 20230210015416.png]]
Y nos encuentra muchos patrones con esta palabra:
![[Pasted image 20230210015440.png]]
Por tanto vamos a hacer que el script nos pida la palabra que queramos buscar de esta forma:
![[Pasted image 20230212195517.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
