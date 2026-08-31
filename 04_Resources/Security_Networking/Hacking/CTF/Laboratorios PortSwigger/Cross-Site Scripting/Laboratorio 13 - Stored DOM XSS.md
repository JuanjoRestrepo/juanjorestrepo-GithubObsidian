---
title: "Laboratorio 13 - Stored DOM XSS"
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
![[Pasted image 20240530122505.png]]
Entramos en alguno de los artículos y podemos observar una sección de comentarios:
![[Pasted image 20240530122627.png]]
Rellenamos con datos random:
![[Pasted image 20240530122652.png]]
Revisamos como se ha almacenado nuestro comentario:
![[Pasted image 20240530122730.png]]
Revisando el código fuente, encontramos un archivo JavaScript llamado loadCommentsWithVulnerableEscapeHtml.js que procesa la información de la siguiente forma, donde sustituye los símbolos > y <, pero el problema está en que esto sustituye la primera coincidencia que encuentra, y a partir de ahí deja de aplicar la sustitución:
![[Pasted image 20240530123339.png]]
Podríamos usar este payload:
```bash
<img src="x" onerror="alert('XSS')">
```
Pero tenemos que adaptarlo teniendo en cuenta los remplazos que hace el código javascript:
```bash
<><img src="x" onerror="alert('XSS')">
```
![[Pasted image 20240530123549.png]]
Y ahora se ha inyectado el XSS:
![[Pasted image 20240530123607.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
