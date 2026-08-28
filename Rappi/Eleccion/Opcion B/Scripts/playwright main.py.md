---
title: "Opción B - Heurística de Consultas y Mecanismos de Extracción"
date: 2026-08-27
tags:
  - caso-estudio
  - rpa
  - heuristica
  - playwright
  - data-engineering
status: evergreen
---

# 🔍 Heurística de Consultas y Estrategias de Extracción en Playwright

Documentación de la lógica utilizada para la construcción automática de consultas de búsqueda geográfica y los métodos de captura de datos en aplicaciones web dinámicas.

---

## 🧩 Lógica de Construcción de la Consulta Heurística

Para garantizar que el buscador de la plataforma localice la sucursal correcta en ausencia de una URL explícita, se aplica el siguiente algoritmo condicional:

```python
# Algoritmo de resolución heurística de texto de búsqueda
user_search: str = (entry.get("searchQuery") or "").strip()
addr_label: str = (entry.get("addressLabel") or "").strip()

if user_search and ("mcdonald" in user_search.lower()):
    heuristic_query = user_search
else:
    base = user_search if user_search else addr_label
    heuristic_query = f"McDonald's {base}".strip()
```

---

## 🔄 Desglose Paso a Paso de los Casos

1. **Caso 1 — Consulta Explícita de Marca:**
   - Si `searchQuery` ya contiene la palabra clave objetivo (`"mcdonald"`), la consulta se respeta sin alteraciones para no introducir sesgos.
   - *Ejemplo:* `"McDonald's Polanco"` $\longrightarrow$ `heuristic_query = "McDonald's Polanco"`.

2. **Caso 2 — Enriquecimiento Automático de Ubicación:**
   - Si la consulta solo contiene la zona o el barrio (`addressLabel`), el sistema antepone automáticamente la marca de interés.
   - *Ejemplo:* `addressLabel = "Condesa"`, `searchQuery = ""` $\longrightarrow$ `heuristic_query = "McDonald's Condesa"`.

---

## 📊 Comparativa de Mecanismos de Extracción

| Mecanismo de Extracción | Fuente y Naturaleza de Datos | Método en Playwright | Confiabilidad y Uso |
| :--- | :--- | :--- | :--- |
| **`__NEXT_DATA__`** | Objeto JSON embebido en el HTML por frameworks como Next.js. | `page.evaluate("() => window.__NEXT_DATA__")` | **Muy Alta**: Extrae el estado estructurado del servidor sin depender de la UI. |
| **Interceptación XHR / Fetch** | Respuestas de red asincrónicas emitidas por el backend. | `page.on("response", callback)` | **Alta**: Captura APIs internas con datos no visibles directamente en el DOM. |
| **Parsing del DOM** | Estructura jerárquica de elementos HTML visibles. | `page.inner_text()` / `page.query_selector()` | **Media**: Propenso a romperse ante cambios visuales de clases o maquetación. |
| **Simulación Add-to-Cart** | Interacción de usuario simulada (clic en botón "Agregar"). | `page.click()` + inspección del *drawer* de pedido | **Alta**: Revela tarifas dinámicas que el servidor solo calcula en el carrito. |
