---
title: "ROT47 - Sistema para Ocultar Contenido de un Mensaje"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos utilizar ROT47 en la máquina de vulnhub [[MAQUINA CYBERSPLOIT 2 (Mensajes ocultos con ROT47, acceso por SSH y escalada de privilegios con Docker)]]Y si buscamos por internet esto de ROT47 nos encontramos con que se trata de un cifrado simple que se utiliza para ocultar el contenido de un mensaje; y tenemos herramientas online para descifrar estos mensajes:
![[Pasted image 20230322210657.png]]
Por tanto entramos en la página de rot47.net y podemos probar en poner uno de los textos que nos salía antes en la web:
![[Pasted image 20230322210740.png]]
Pegamos por ejemplo la parte de la derecha en la web:
![[Pasted image 20230322210806.png]]
Y si hacemos clic en ROT47 nos devuelve un usuario shailendra:
![[Pasted image 20230322210828.png]]
Y ahora hacemos lo mismo con el otro dato de la web cybersploit1:
![[Pasted image 20230322210856.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
