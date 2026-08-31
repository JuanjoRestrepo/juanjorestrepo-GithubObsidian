---
title: "3 - Comando chown para Asignar Propietarios de Archivos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con este comando podremos cambiar el dueño de un archivo o directorio. Por ejemplo, anteriormente habíamos creado el grupo de empleados, por lo que ahora vamos a hacer que un directorio sea propiedad de dicho grupo:
```
sudo chown :empleados /home/mario/Escritorio/administracion/
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
