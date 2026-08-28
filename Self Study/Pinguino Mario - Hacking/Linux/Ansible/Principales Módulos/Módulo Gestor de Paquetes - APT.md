---
title: "Módulo Gestor de Paquetes - APT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con este módulo podemos ejecutar el comando APT para instalar paquetes sobre los equipos que queramos administrar. Esto lo haremos realizando la siguiente configuración dentro del playbook y teniendo en cuenta el fichero de configuración de ansible para que no haya errores (utilizamos become: true para ejecutar el comando con permisos de root)
![[Pasted image 20230107134735.png]]
Y para eliminar un programa, lo haríamos de esta forma:
![[Pasted image 20230108113358.png]]
Ahora para aplicar un apt autoremove, haríamos esto:
![[Pasted image 20230108113601.png]]
Para actualizar todos los repositorios, sería de esta forma:
![[Pasted image 20230108113926.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
