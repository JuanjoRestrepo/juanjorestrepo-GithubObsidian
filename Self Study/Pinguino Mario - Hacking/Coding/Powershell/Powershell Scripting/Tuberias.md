---
title: "Tuberias"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Funcionan igual que en bash, por ejemplo ordenando los procesos del sistema por orden alfabético:
![[Pasted image 20221217104150.png]]
Por ejemplo, si quiero visualizar el contenido de un archivo y aplicar una tubería para que me busque algo, lo haría de esta forma:
```powershell
Get-Content direcciones_ip.txt | Select-String -Pattern "192"
```
![[Pasted image 20230509151233.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
