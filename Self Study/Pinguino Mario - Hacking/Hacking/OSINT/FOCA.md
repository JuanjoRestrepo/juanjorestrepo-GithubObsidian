---
title: "FOCA"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vamos a descargar un documento aleatorio:
![[Pasted image 20231220111211.png]]
Lo descargamos y dejamos FOCA preparado para su uso:
![[Pasted image 20231220111240.png]]
Y en la parte de Document Analysis podemos añadir el fichero a analizar:
![[Pasted image 20231220111335.png]]
Y en la misma parte ya lo tenemos localizable:
![[Pasted image 20231220111419.png]]
Y ahora hacemos clic derecho sobre el fichero y le damos a extract metadata:
![[Pasted image 20231220111509.png]]
Y obtenemos los metadatos:
![[Pasted image 20231220111608.png]]
También podemos automatizar la descarga de muchos archivos de un target en específico creando un proyecto:
![[Pasted image 20231220111714.png]]
Y por aquí le pedimos a FOCA que nos busque por archivos:
![[Pasted image 20231220111801.png]]
Y nos encuentra los distintos documentos:
![[Pasted image 20231220111836.png]]
Podemos bajarnos documentos a la vez seleccionándolos y dando en descargar:
![[Pasted image 20231220111938.png]]
Los que están con el puntito verde es que están descargados:
![[Pasted image 20231220112036.png]]
Y sacamos los metadatos:
![[Pasted image 20231220112101.png]]
Y vemos los resultados, donde obtenemos usuarios y más cosas:
![[Pasted image 20231220112138.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
