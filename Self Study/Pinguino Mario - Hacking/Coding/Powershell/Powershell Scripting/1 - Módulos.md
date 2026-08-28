---
title: "1 - Módulos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para verificar qué módulos están actualmente importados, puedes usar:
```powershell
Get-Module
```
![[Pasted image 20240921103930.png]]
Para importar módulos, primero tenemos que cambiar la política de ejecución a `RemoteSigned` o `Unrestricted`. Para cambiarla, ejecuta PowerShell como administrador y usa uno de los siguientes comandos:
```powershell
Set-ExecutionPolicy RemoteSigned # Para permitir scripts locales no firmados.

Set-ExecutionPolicy Unrestricted # Para permitir todos los scripts (menos seguro).
```
Y luego ya podemos importar un módulo en concreto:
```powershell
Import-Module .\ps2exe.psm1
```
![[Pasted image 20240921104352.png]]
Y ahora podremos ejecutar el módulo correspondiente:
```powershell
Invoke-PS2EXE
```
![[Pasted image 20240921104843.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
