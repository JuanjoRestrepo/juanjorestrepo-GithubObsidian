---
title: "12 - Comprimir y Descomprimir en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para comprimir un fichero en formato .zip, lo haremos de esta forma:
```bash
zip -r archivos.zip documento.txt
```
![[Pasted image 20230323032724.png]]
Si queremoms descomprimir el archivo usaremos el comando unzip:
```bash
unzip archivos.zip
```
![[Pasted image 20230323032735.png]]
Con este comando también podemos comprimir directorios:
![[Pasted image 20230323032743.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
