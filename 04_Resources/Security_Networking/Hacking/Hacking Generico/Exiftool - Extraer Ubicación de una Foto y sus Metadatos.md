---
title: "Exiftool - Extraer Ubicación de una Foto y sus Metadatos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con la herramienta exitfool podemos extraer muchos metadatos de una fotografía, por tanto para instalar esta herramienta ejecutamos el siguiente comando:
![[Pasted image 20230130215407.png]]
Y ahora tan solo debemos de pasarle la imagen que queramos de esta forma:
![[Pasted image 20230130215438.png]]
Y ahora en la parte de abajo, entre toda la información tenemos las coordenadas de donde se hizo esta fotografía:
![[Pasted image 20230130215523.png]]
Por tanto si queremos conseguir esta ubicación en Google Maps simplemente debemos hacer una sencilla conversión, donde eliminaremos todos los espacios y además donde se encuentre la palabra deg habrá el signo de grados º:
![[Pasted image 20230130215617.png]]
Ahora esto lo pegamos en maps y habremos obtenido la ubicación:
![[Pasted image 20230130215657.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
