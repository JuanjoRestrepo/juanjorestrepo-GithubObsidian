---
title: "1 - Evasión Básica"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## Impedir Ejecucion de scripts
![[Pasted image 20240114162317.png]]
De tal forma que ahora si intentamos ejecutar cualquier script no vamos a poder:
![[Pasted image 20240114163233.png]]
![[Pasted image 20240114163046.png]]
Si queremos bypassear esta protección, podemos usar iex de la siguiente forma con el mismo script de antes:
```powershell
cat .\script.ps1|iex
```
![[Pasted image 20240114163215.png]]
También podemos bypassear esto cambiando el modo de ejecución de powershell de la siguiente forma:
```powershell
powershell -ExecutionPolicy Bypass
```
![[Pasted image 20240114163454.png]]
## Habilitar modo restringido de lenguaje
Creamos dentro del registro el siguiente archivo:
![[Pasted image 20240114162744.png]]
Y desde powershell comprobamos que esté activado con el siguiente comando:
```powershell
$ExecutionContext.SessionState.LanguageMode
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
