---
title: "5 - Inicio del sistema Linux. SysVinit"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Una vez cargado el gestor de arranque y todo listo, es cuando se inicia el demonio init, que se encargará de ejecutar todo lo demas y el resto de procesos para que el sistema pueda arrancar.

---------------------

Tenemos 3 tipos de procesos que se encargan de iniciar y gestonar los demonios en Linux:

SysVinit --> Utiliza scripts y niveles de ejecución para controlar el inicio, apagado y gestión de los procesos del sistema. (ya no se encuentra en sistemas modernos)
Systemd --> Desde el 2015 fue adoptado por parte de las distribuciones Linux como su sistema de inicio.
Upstar --> Utiliza eventos para gestionar el arranque o parada de los procesos.
![[Pasted image 20230819163830.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
