---
title: "2 - Bind Mount"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Primero creamos un directorio en nuestro host:
![[Pasted image 20240301160723.png]]
Y ahora al desplegar el contenedor podemos cargarle esta carpeta:
```bash
docker run -it -v /home/mario/Escritorio/data_host:/home 3d
```
Y le creamos un archivo al directorio /home:
![[Pasted image 20240301160809.png]]
Y este archivo se habrá creado en la carpeta también:
![[Pasted image 20240301160825.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
