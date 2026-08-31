---
title: "Persistencia con Metasploit en Windows"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será estar dentro de una máquina windows con un meterpreter y siendo usuario administrador:
![[Pasted image 20230801122738.png]]
Una vez hecho esto, usaremos el siguiente módulo, poniendo la sesión en segundo plano y luego volviendo a cargarla:
```bash
use exploit/windows/local/persistence_service
```
![[Pasted image 20230801122857.png]]
Ahora, por otra parte, nos ponemos a la escucha con metasploit para recibir una nueva conexión en caso de reiniciar la máquina:
![[Pasted image 20230801123340.png]]
Apagamos la máquina víctima:
![[Pasted image 20230801123445.png]]
Pero en la otra ventana de metasploit habremos recibido la conexión una vez que la máquina víctima se haya reiniciado:
![[Pasted image 20230801123520.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
