---
title: "Bucles en Powershell"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

### BUCLE FOR
```powershell
$frutas = "Manzana", "Banana", "Naranja", "Pera", "Melón"

for ($i = 0; $i -lt $frutas.Count; $i++) {
    Write-Host $frutas[$i]
}
```
![[Pasted image 20230509150805.png]]
También podríamos recorrer todos los elementos de un documento de texto, de la siguiente forma:
```powershell
$archivo = Get-Content "direcciones_ip.txt"

for ($i = 0; $i -lt $archivo.Count; $i++) {
    Write-Host $archivo[$i]
}
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
