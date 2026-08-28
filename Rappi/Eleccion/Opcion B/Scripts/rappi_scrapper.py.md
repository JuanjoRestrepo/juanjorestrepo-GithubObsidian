```python
"""Módulo de heurística para la construcción de consultas de búsqueda.

Author: Juan José Restrepo Rosero
Standards: PEP8, mypy --strict, Google Docstrings.
"""

from typing import Final

# Constantes con unidades y dominios explícitos
DEFAULT_BRAND: Final[str] = "McDonald's"


def build_heuristic_query(user_search: str | None, addr_label: str) -> str:
    """Construye una consulta de búsqueda heurística optimizada para Rappi.

    Args:
        user_search: Consulta de búsqueda opcional proporcionada por el usuario.
        addr_label: Etiqueta de dirección o barrio base para la localización.

    Returns:
        str: La cadena de consulta optimizada y enriquecida.

    Raises:
        ValueError: Si tanto user_search como addr_label están vacíos.
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
