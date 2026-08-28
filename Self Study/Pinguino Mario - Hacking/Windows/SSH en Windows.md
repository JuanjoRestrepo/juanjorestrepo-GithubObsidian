---
title: "SSH en Windows"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será habilitar esta característica dentro del menú de características opcionales, y una vez ahí añadir el servidor OpenSSH:

![[Pasted image 20221217104559.png]]

A continuación, hay que abrir la ventana de servicios y habilitar este servicio de openssh, además de comprobar que los otros dos servicios de ssh que están al lado que se encuentren también habilitados:

![[Pasted image 20221217104605.png]]

A continuación, el siguiente paso será abrir un terminal con permisos de administrador y ejecutar este comando:

_**`New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Service sshd -Enabled True -Direction Inbound -Protocol TCP -Action Allow -Profile Domain`**_

![[Pasted image 20221217104619.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
