
```python
# scrapers/resolver.py

from playwright.sync_api import Page

from typing import Tuple, Optional, Dict

from .utils import random_delay

import random

  

USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",

]

  

def resolve_restaurant_url(page: Page, search_query: str) -> Tuple[Optional[str], Dict]:

    meta = {"candidates": [], "chosen_index": None, "chosen_score": -999, "chosen_name": None}

    if not search_query:

        return None, meta

    from urllib.parse import quote_plus

    search_url = f"https://www.rappi.com.mx/buscar?query={quote_plus(search_query)}"

    try:

        page.set_extra_http_headers({"User-Agent": random.choice(USER_AGENTS)})

    except Exception:

        pass

    try:

        page.goto(search_url, timeout=25*1000)

        try:

            page.wait_for_timeout(600)

        except:

            pass

        random_delay()

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

  

    for i, c in enumerate(candidates[:200]):

        name_norm = (c["name"] or "").lower()

        href_norm = (c["href"] or "").lower()

        score = 0

        if "mcdonald" in name_norm or "mcdonald" in href_norm:

            score += 50

        if search_query.lower() in name_norm:

            score += 10

        meta["candidates"].append({"index": i, "href": c["href"], "name": c["name"], "score": score})

        if score > meta["chosen_score"]:

            meta["chosen_score"] = score

            meta["chosen_index"] = i

            meta["chosen_name"] = c["name"]

  

    chosen = None

    if meta["chosen_index"] is not None and meta["candidates"]:

        if meta["chosen_index"] < len(meta["candidates"]):

            chosen = meta["candidates"][meta["chosen_index"]]["href"]

  

    conf = "low"

    if meta["chosen_score"] >= 35:

        conf = "high"

    elif meta["chosen_score"] >= 20:

        conf = "medium"

    meta["resolutionMethod"] = "search_page_heuristic"

    meta["confidence"] = conf

    meta["initial_choice"] = chosen

    return chosen, meta
```


# Explicación sencilla, clara y concisa de `resolver.py`

**Propósito (una línea)**  
`resolve_restaurant_url` busca en Rappi la mejor URL de restaurante para una `search_query` y devuelve la URL elegida junto con metadata sobre cómo se decidió.

---

## Entradas / Salidas

- Entrada: `page` (Playwright Page ya abierta) y `search_query` (texto, p. ej. `"McDonald's Condesa"`).
    
- Salida: `(chosen_url, meta)`
    - `chosen_url`: string con la URL del restaurante elegida, o `None` si no se resolvió.
    - `meta`: diccionario con detalles (candidatos, puntuaciones, método, confianza, posibles errores).



