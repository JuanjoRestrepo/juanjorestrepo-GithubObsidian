---
title: "3 - MongoExport"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

MongoExport sirve para ejecutar instrucciones de mongo desde fuera de la mongosh, de tal forma que podremos extraer el output de las consultas a un fichero externo. Por tanto lo bajamos desde esta web:
![[Pasted image 20230607123639.png]]
Y pasamos todos los archivos a la carpeta de bin de la mongosh:
![[Pasted image 20230607123755.png]]
Y ahora abrimos aquí una ventana de powershell:
![[Pasted image 20230607123916.png]]
Una vez dentro ya podemos ejecutar la instrucción, por ejemplo esta:
```sql
./mongoexport --uri "mongodb://localhost:27017/canal" --collection suscriptores --out archivoDeSalida.json
```
![[Pasted image 20230607124741.png]]
Y ya lo tenemos exportado:
![[Pasted image 20230607124756.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
