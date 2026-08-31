---
title: "5 - Obtener Información del Sistema - systeminfo"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# Obtener el nombre de usuario
Usaremos el comando hostname:
![[Pasted image 20230731132954.png]]
# OBTENER INFORMACIÓN DEL SISTEMA
Para obtener información del sistema, usamos el comando systeminfo:
![[Pasted image 20230731133022.png]]
# OBTENER INFORMACIÓN SOBRE ACTUALIZACIONES DEL SISTEMA
Podemos también obtener información sobre las actualizaciones del sistema con el siguiente comando:
```powershell
wmic qfe get Caption,Description,HotFixID,InstalledOn
```
![[Pasted image 20230731133118.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
