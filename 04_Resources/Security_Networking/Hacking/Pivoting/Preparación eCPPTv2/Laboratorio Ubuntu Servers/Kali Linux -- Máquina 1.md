---
title: "Kali Linux -- Máquina 1"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Desde la máquina Kali nos conectamos por ssh a la máquina 1 ya que tenemos conectividad:
![[Pasted image 20230823163339.png]]
Y en cada máquina tenemos que ejecutar el comando dhclient para que pueda reconocer la segunda interfaz:
![[Pasted image 20230823163400.png]]
Y ya estamos en la máquina 1, donde tenemos visibilidad con la máquina 2 que tiene la IP 20.20.20.11:
![[Pasted image 20230824095843.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
