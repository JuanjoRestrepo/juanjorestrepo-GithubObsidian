---
title: "Opción B - Módulo de Heurística de Consultas Rappi"
date: 2026-08-27
tags:
  - caso-estudio
  - rpa
  - python
  - heuristica
  - codigo-referencia
status: evergreen
---

# 🛠️ Módulo de Heurística de Consultas: `build_heuristic_query`

Implementación de referencia con tipado estático estricto (`mypy --strict`) y docstrings estilo Google para la construcción determinista de términos de búsqueda.

---

## 💻 Código de Referencia Documental

```python
"""Módulo de heurística para la construcción de consultas de búsqueda.

Author: Juan José Restrepo Rosero
Standards: PEP8, mypy --strict, Google Docstrings.
"""

from typing import Final

# Constantes de dominio con inmutabilidad explícita
DEFAULT_BRAND: Final[str] = "McDonald's"


def build_heuristic_query(user_search: str | None, addr_label: str) -> str:
    """Construye una consulta de búsqueda heurística optimizada para Rappi.

    Args:
        user_search: Consulta de búsqueda opcional proporcionada por el usuario.
        addr_label: Etiqueta de dirección o barrio base para la localización.

    Returns:
        str: La cadena de consulta optimizada y enriquecida.

    Raises:
        ValueError: Si tanto user_search como addr_label están vacíos o contienen solo espacios.
    """
    clean_search = (user_search or "").strip()
    clean_addr = addr_label.strip()

    if not clean_search and not clean_addr:
        raise ValueError(
            "Se requiere al menos una consulta de búsqueda o una dirección base."
        )

    # Caso 1: Si la búsqueda ya contiene la marca de interés, se respeta la intención
    if clean_search and "mcdonald" in clean_search.lower():
        return clean_search

    # Caso 2: Enriquecimiento heurístico usando la base de la dirección o búsqueda
    base = clean_search if clean_search else clean_addr
    return f"{DEFAULT_BRAND} {base}".strip()
```

---

## 🔍 Análisis de Diseño y Robustez

1. **Inmutabilidad y Tipado Estricto:**
   - Uso de `Final[str]` para la constante `DEFAULT_BRAND`.
   - Soporte de unión de tipos moderna (`str | None`) compatible con Python 3.10+.
2. **Defensividad ante Datos Sucios:**
   - Validación explícita de entradas vacías con levantamiento de `ValueError`.
   - Limpieza de espacios en blanco mediante `.strip()`.
3. **Determinismo Heurístico:**
   - Garantiza que cualquier combinación de dirección y búsqueda genere una cadena normalizada, minimizando la dispersión en los resultados del motor de búsqueda de Rappi.
