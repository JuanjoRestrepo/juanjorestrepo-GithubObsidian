---
title: "Nikto"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta herramienta sirve para hacer escaneos web automáticos:
```bash
nikto -h http://192.8.241.3
```
![[Pasted image 20230728115055.png]]
También podemos pasarle la URL de un target donde pensemos que pueda ser vulnerable a LFI:
![[Pasted image 20230728115326.png]]
Por tanto hacemos la prueba:
```bash
nikto -h http://192.8.241.3/index.php?page=arbitrary-file-inclusion.php -Tuning 5 -Display V
```
Y nos lo encuentra:
![[Pasted image 20230728115554.png]]
También podemos guardar este reporte en formato html:
```bash
nikto -h http://192.8.241.3/index.php?page=arbitrary-file-inclusion.php -Tuning 5 -Display V -o nikto.html -Format htm
```
![[Pasted image 20230728115759.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
