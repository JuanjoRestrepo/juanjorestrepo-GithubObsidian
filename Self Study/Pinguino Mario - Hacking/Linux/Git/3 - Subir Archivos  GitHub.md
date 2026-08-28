---
title: "3 - Subir Archivos  GitHub"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

PASO 1:
```bash
git init
```
PASO 2:
```bash
git add archivo1 archivo2
```
PASO 3:
```bash
git commit -m 'Subiendo archivos a github o gitlab'
```
PASO 4:
```bash
git remote add origin url.git
```
PASO 5:
```bash
git push -u origin master
```
Aquí nos pedirá credenciales para iniciar sesión en github; y luego desde la web tenemos que hacer un merge para pasar estos cambios a la rama main.

-------------------------------------

PASO 6:
Si tenemos errores, hacemos un git reset y volvemos a probar:
```bash
git reset
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
