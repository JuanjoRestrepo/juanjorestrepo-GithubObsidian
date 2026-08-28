---
title: "1 - Restringir Acceso a un Archivo"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Es posible que queramos destringir el acceso a algún archivo que contenga información delicada, por ejemplo el archivo secreto.txt de mi servidor:
![[Pasted image 20240909171916.png]]
![[Pasted image 20240909171923.png]]
Para conseguir que nadie pueda ver este archivo, tenemos que añadir las siguientes líneas dentro del archivo de configuración de default.conf:
```bash
<Files "/var/www/html/public/secreto.txt">
    Require all denied
</Files>
```
![[Pasted image 20240909172246.png]]
Y ahora no tenemos acceso a dicho archivo:
![[Pasted image 20240909172327.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
