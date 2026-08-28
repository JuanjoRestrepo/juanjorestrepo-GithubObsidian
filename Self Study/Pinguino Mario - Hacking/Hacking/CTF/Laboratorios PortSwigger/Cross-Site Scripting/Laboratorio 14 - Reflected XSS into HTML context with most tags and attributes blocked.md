---
title: "Laboratorio 14 - Reflected XSS into HTML context with most tags and attributes blocked"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Este es el laboratorio:
![[Pasted image 20240530124904.png]]
Probamos en inyectar algo:
![[Pasted image 20240530125017.png]]
Pero si probamos en inyectar algo payload, vemos que hay un limitador que no lo permite:
```bash
<script>alert()</script>
```
![[Pasted image 20240530125105.png]]
![[Pasted image 20240530125116.png]]
También, si probamos con la etiqueta img, sigue dando error:
![[Pasted image 20240530130422.png]]
![[Pasted image 20240530130430.png]]
Vamos a fuzzear la etiqueta con el intruder:
![[Pasted image 20240530130512.png]]
Y ahora vamos a recurrir al siguiente recurso donde tendremos un listado de etiquetas que podemos probar:
```bash
https://portswigger.net/web-security/cross-site-scripting/cheat-sheet?source=post_page-----54a7cfe109aa--------------------------------
```
![[Pasted image 20240530130602.png]]
Y lo pegamos aquí:
![[Pasted image 20240530130633.png]]
Lo ejecutamos y vemos que la etiqueta body está permitida:
![[Pasted image 20240530130722.png]]
Lo comprobamos y efectivamente se puede:
![[Pasted image 20240530130756.png]]
Por lo que vamos formando nuestro payload:
```bash
<body onerror="alert('XSS')">
```
Pero si mandamos este payload, ahora nos marca error de atributo:
![[Pasted image 20240530130927.png]]
![[Pasted image 20240530130936.png]]
Por lo que ahora haremos fuzzing al atributo:
![[Pasted image 20240530131027.png]]
Copiamos todos los eventos:
![[Pasted image 20240530131100.png]]
Y los pegamos en burp suite:
![[Pasted image 20240530131114.png]]
Y vemos los siguiente eventos aceptados:
![[Pasted image 20240530131508.png]]
Preparamos nuestro nuevo payload:
```bash
<body onbeforetoggle="alert('XSS')">
```
![[Pasted image 20240530131618.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
