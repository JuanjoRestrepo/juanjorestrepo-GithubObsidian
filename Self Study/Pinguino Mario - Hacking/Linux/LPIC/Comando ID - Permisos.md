---
title: "Comando ID - Permisos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con este comando podré consultar los permisos que dispongo con el usuario que soy, por ejemplo si lo ejecuto siendo el usuario normal veremos esto:
![[Pasted image 20230111205405.png]]
Siendo este usuario por ejemplo no podremos ver el fichero /etc/shadow con las contraseñas cifradas:
![[Pasted image 20230111205518.png]]
Y si lo ejecuto siendo el usuario sudo, aquí veré que tengo permiso para hacer todo:
![[Pasted image 20230111205432.png]]
Ahora sin embargo ya sí podré leer el fichero /etc/shadow:
![[Pasted image 20230111205604.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
