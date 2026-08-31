---
title: "Maltego"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta es la interfaz gráfica de maltego, y se compone de transformadores, que son los módulos que se utilizan para realizar las distintas operaciones:
![[Pasted image 20231218190122.png]]
Por ejemplo vamos a buscar por have i been pwned:
![[Pasted image 20231218190211.png]]
Y también este es interesante, el de social links:
![[Pasted image 20231218190302.png]]
El siguiente paso es crear un grafo para ir arrastrando las entidades:
![[Pasted image 20231218190356.png]]
Y podemos arrastrar cualquiera de estas entidades para luego ir aplicándole los transformadores:
![[Pasted image 20231218190521.png]]
Y podemos establecer que el determinado objetivo trabaja en una determinada compañía, o cualquier otra asociación:

![[Pasted image 20231218190719.png]]
Si hacemos clic derecho sobre el usuario, podemos ejecutar los transformadores:
![[Pasted image 20231218191253.png]]
También podemos hacer que un usuario tenga un determinado alias:
![[Pasted image 20231218191423.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
