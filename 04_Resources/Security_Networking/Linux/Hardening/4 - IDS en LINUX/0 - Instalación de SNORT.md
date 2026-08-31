---
title: "0 - Instalación de SNORT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Snort es un sistema de detección de intrusiones (IDS, por sus siglas en inglés) de código abierto que se utiliza en sistemas Linux (y otros sistemas operativos) para monitorear y analizar el tráfico de red en tiempo real. Snort tiene la capacidad de detectar una amplia gama de ataques y actividades sospechosas, lo que lo convierte en una herramienta esencial para la seguridad informática.

----

Para instalarlo ejecutamos el comando `apt install snort` donde primero debemos consultar nuestra IP:
![[Pasted image 20240829233229.png]]
Y ahora podremos introducir el rango de red que queramos abarcar con snort:
![[Pasted image 20240829233251.png]]
Y ahora snort estará en funcionamiento, de tal forma que si ejecutamos el siguiente comando, vemos como snort se ha lanzado cogiendo nuestra interfaz de red enp0s3 y nuestro rango de red:
![[Pasted image 20240829233546.png]]
Podemos también consultar las reglas en total:
![[Pasted image 20240829233743.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
