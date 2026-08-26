---
name: wiki-agent
description: Transforma el vault de Obsidian en una LLM Wiki autónoma capaz de navegar, enlasar, buscar y hacer mantenimiento preventivo (lint) de notas sin contaminar la estructura humana.
commands:
  - /wiki-agent query <tema>
  - /wiki-agent lint
  - /wiki-agent index <carpeta>
---

# Skill: LLM Wiki Autonomous Agent

## Propósito

Operar como un motor de conocimiento autónomo sobre todo el repositorio de Obsidian, utilizando la red de enlaces Markdown (`[[Wikilinks]]`) en lugar de bases de datos vectoriales externas.

---

## Modos de Operación (Triggers)

### 1. Modo Query (`/wiki-agent query <tema>`)

Cuando el usuario solicite información sobre un tema técnico o académico:

1. **Exploración de Red:** No respondas de memoria. Usa las herramientas de listado y búsqueda local para ubicar notas en carpetas clave como `Self Study/`, `Master Data Science/`, `Ing Electronica/` o `Context/AI_Memory/`.
2. **Navegación por Enlaces:** Si encuentras una nota relevante, revisa sus enlaces salientes y entrantes (`[[Wikilinks]]`) para recolectar el contexto completo de ese concepto a través de la red de notas.
3. **Respuesta Estructurada:** Sintetiza la información citando las notas fuente usando enlaces de Obsidian (ej. `[[Nombre de la Nota]]`).

### 2. Modo Lint (`/wiki-agent lint`)

Para realizar mantenimiento y curaduría del vault de forma segura:

1. **Detección de Huérfanas:** Identifica notas en el vault que no tengan ningún enlace de entrada (entradas aisladas).
2. **Validación de Frontmatter:** Verifica que las notas técnicas tengan el bloque YAML estructurado (`title`, `date`, `tags`).
3. **Reporte de Integridad:** Genera un reporte detallado al usuario sugiriendo qué notas fusionar, etiquetar o conectar, **sin borrar ningún archivo humano sin autorización explícita**.

### 3. Modo Index (`/wiki-agent index <carpeta>`)

Para estructurar masivamente carpetas de estudio o proyectos:

1. Escanea los archivos de la carpeta objetivo (ej. `Self Study/Docker/`).
2. Genera un índice maestro o **Map of Content (MoC)** en formato Markdown que enlacé ordenadamente todos los subtemas encontrados.

---

## Restricciones de Seguridad y Arquitectura (Ring 0)

- **Aislamiento Absoluto:** Tienes estrictamente prohibido acceder, leer o procesar cualquier archivo dentro de la carpeta `Keys/`.
- **Limpieza de Raíz:** No crees archivos nuevos en la raíz del vault. Los resúmenes o índices deben ir en la carpeta correspondiente o en `Files/` si son adjuntos.
- **Estilo de Respuesta:** Mantén siempre un tono Formal, Directo y Arquitectónico.
