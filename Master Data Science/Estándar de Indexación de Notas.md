---
title: "Estándar de Indexación de Notas"
date: 2026-08-27
tags:
  - maestria
  - gestion-del-conocimiento
  - obsidian
  - referencia
status: reference
---

# Estándar de Indexación de Notas

[[Master Data Science/MOC - Master Data Science|← MOC Maestro]]

## Contrato de una nota académica

Cada apunte Markdown de un semestre debe comenzar con este frontmatter, ajustando únicamente el título y las etiquetas específicas:

```yaml
---
title: "<Título descriptivo>"
date: YYYY-MM-DD
tags:
  - maestria
  - semestre-n
  - curso
  - tema
status: reference
---
```

Los MOC usan además las etiquetas `moc` e `indice` y el estado `evergreen`. Los adjuntos (imágenes y PDF) se conservan en `Files/`; no se convierten en código ni se colocan en la raíz de la bóveda.

## Taxonomía por ruta

| Prefijo de ruta | Etiquetas mínimas |
| --- | --- |
| `Semestre 1/Gestion Datos` | `maestria`, `semestre-1`, `gestion-datos`, `apuntes` |
| `Semestre 1/Metodos y Simulacion Estadistica` | `maestria`, `semestre-1`, `estadistica`, `apuntes` |
| `Semestre 2/400ITA010` | `maestria`, `semestre-2`, `aprendizaje-automatico`, `apuntes` |
| `Semestre 2/400MEA009` | `maestria`, `semestre-2`, `modelos-estadisticos`, `apuntes` |
| `Semestre 2/Deep Learning` | `maestria`, `semestre-2`, `deep-learning`, `apuntes` |
| `Semestre 3/Visualizacion de Datos` | `maestria`, `semestre-3`, `visualizacion-datos`, `apuntes` |
| `Semestre 3/Gerencia de Proyectos` | `maestria`, `semestre-3`, `gerencia-proyectos`, `apuntes` |

## Lógica de indexación

1. Crear la nota dentro del curso, módulo y unidad correctos; no mover adjuntos ni convertir la nota a un archivo ejecutable.
2. Declarar el frontmatter antes del contenido.
3. Añadir la nota en la sección y unidad correspondiente del MOC semestral.
4. Enlazar, como mínimo, un prerrequisito y una aplicación mediante enlaces internos de Obsidian. Los backlinks harán visible la relación en sentido inverso.
5. Para definiciones, modelos, restricciones, métricas y funciones de pérdida, usar LaTeX: `$...$` para expresiones breves y `$$...$$` para ecuaciones centrales.
6. Añadir una conexión al MOC Maestro cuando el concepto sea transversal a más de un curso o proyecto.

## Auditoría no destructiva

Ejecute estas comprobaciones desde la raíz de la bóveda. Solo detectan desviaciones; no modifican contenidos.

```zsh
find "Master Data Science/Semestre 1" "Master Data Science/Semestre 2" "Master Data Science/Semestre 3" -name "*.md" -print0 | while IFS= read -r -d "" note; do
  [ "$(head -n 1 "$note")" = "---" ] || print -r -- "$note"
done

rg -n --glob "*.md" "\[\[|\$\$|\$[^$]+\$" "Master Data Science"
```

La primera consulta lista notas sin frontmatter inicial. La segunda permite revisar, respectivamente, enlaces internos y fórmulas LaTeX antes de cerrar una sesión de estudio.
