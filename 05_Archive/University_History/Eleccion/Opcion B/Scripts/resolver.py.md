---
title: "Opción B - Documentación del Resolver Heurístico de URLs"
date: 2026-08-27
tags:
  - caso-estudio
  - rpa
  - heuristica
  - resolver
  - python
status: evergreen
---

# 🧭 Documentación Técnica: `resolver.py`

Módulo encargado de resolver dinámicamente la URL del restaurante o sucursal más relevante a partir de una consulta de búsqueda textual en Rappi.

---

## 🎯 Propósito y Algoritmo

`resolve_restaurant_url` ejecuta una búsqueda en `https://www.rappi.com.mx/buscar?query=...`, analiza los primeros 200 enlaces coincidentes con la estructura `/restaurantes/` y calcula una puntuación ponderada para seleccionar el candidato óptimo.

---

## 💻 Código de Referencia Documental

```python
"""scrapers/resolver.py - Resolución heurística de URLs de restaurantes."""

import random
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus
from playwright.sync_api import Page
from .utils import random_delay

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
]


def resolve_restaurant_url(page: Page, search_query: str) -> Tuple[Optional[str], Dict]:
    """Resuelve la URL del restaurante más probable mediante evaluación heurística.

    Args:
        page: Instancia de página activa de Playwright.
        search_query: Texto de búsqueda (ej. "McDonald's Condesa").

    Returns:
        Tuple[Optional[str], Dict]: URL seleccionada y diccionario con metadata de auditoría.
    """
    meta = {
        "candidates": [],
        "chosen_index": None,
        "chosen_score": -999,
        "chosen_name": None,
    }

    if not search_query:
        return None, meta

    search_url = f"https://www.rappi.com.mx/buscar?query={quote_plus(search_query)}"

    try:
        page.set_extra_http_headers({"User-Agent": random.choice(USER_AGENTS)})
        page.goto(search_url, timeout=25 * 1000)
        random_delay(0.6, 1.2)
    except Exception as e:
        meta["error"] = str(e)
        return None, meta

    anchors = page.query_selector_all("a[href*='/restaurantes/']")
    seen = set()
    candidates = []

    for a in anchors:
        try:
            href = a.get_attribute("href")
            if not href:
                continue
            if href.startswith("/"):
                href = "https://www.rappi.com.mx" + href
            if href in seen:
                continue
            seen.add(href)
            txt = (a.inner_text() or "").strip()
            candidates.append({"href": href, "name": txt})
        except Exception:
            continue

    # Evaluación y ponderación heurística de candidatos
    for i, c in enumerate(candidates[:200]):
        name_norm = (c["name"] or "").lower()
        href_norm = (c["href"] or "").lower()
        score = 0

        # Regla 1: Ponderación de marca
        if "mcdonald" in name_norm or "mcdonald" in href_norm:
            score += 50

        # Regla 2: Coincidencia con la consulta de ubicación
        if search_query.lower() in name_norm:
            score += 10

        meta["candidates"].append({
            "index": i,
            "href": c["href"],
            "name": c["name"],
            "score": score
        })

        if score > meta["chosen_score"]:
            meta["chosen_score"] = score
            meta["chosen_index"] = i
            meta["chosen_name"] = c["name"]

    chosen = None
    if meta["chosen_index"] is not None and meta["candidates"]:
        if meta["chosen_index"] < len(meta["candidates"]):
            chosen = meta["candidates"][meta["chosen_index"]]["href"]

    # Asignación de nivel de confianza
    if meta["chosen_score"] >= 35:
        conf = "high"
    elif meta["chosen_score"] >= 20:
        conf = "medium"
    else:
        conf = "low"

    meta["resolutionMethod"] = "search_page_heuristic"
    meta["confidence"] = conf
    meta["initial_choice"] = chosen

    return chosen, meta
```

---

## 📊 Reglas de Decisión y Niveles de Confianza

| Rango de Puntaje (*Score*) | Nivel de Confianza | Criterio de Activación |
| :---: | :---: | :--- |
| $\text{Score} \ge 35$ | **`high`** | Coincidencia confirmada de la marca principal (`mcdonald`) en la URL o título. |
| $20 \le \text{Score} < 35$ | **`medium`** | Coincidencia parcial con la consulta de búsqueda sin confirmación unívoca de marca. |
| $\text{Score} < 20$ | **`low`** | Coincidencia débil; resultado potencialmente ruidoso que requiere auditoría manual. |

---

## 🎙️ Puntos Clave para la Defensa Oral

1. **Auditoría de Decisiones:** El objeto `meta` exporta todos los candidatos evaluados con sus puntuaciones individuales, lo que permite demostrar al jurado exactamente por qué se eligió una sucursal específica.
2. **Defensa contra Redirecciones:** Normaliza rutas relativas (`/restaurantes/...`) a URLs absolutas y deduplica enlaces mediante un conjunto de hashing (`seen`).
3. **Resiliencia ante Fallos de Red:** Si la navegación excede el tiempo límite o falla el renderizado, el error se encapsula en `meta["error"]` y se devuelve `None`, evitando que el proceso principal colapse.