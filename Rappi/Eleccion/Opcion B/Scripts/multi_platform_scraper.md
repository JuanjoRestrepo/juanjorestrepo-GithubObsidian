

# Archivo: `scrapers/multi_platform_scraper.py` — explicación línea a línea (clara y sencilla)

`#!/usr/bin/env python3 # scrapers/multi_platform_scraper.py """ Multi-platform scraper for competitive intelligence Supports: Rappi, UberEats (and can be extended to DiDi Food) """`

- Shebang y docstring: indica que es el _main_ que orquesta scrapers multi-plataforma.
    

`import argparse, csv, json, os, sys, time, hashlib from pathlib import Path from typing import List, Dict, Any from datetime import datetime, timezone from playwright.sync_api import sync_playwright from dotenv import load_dotenv`

- Importa utilidades estándar, tipos y Playwright para controlar navegador. `dotenv` permite cargar variables de entorno.
    

`sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`

- Añade el directorio padre al `PYTHONPATH` para que los imports relativos funcionen cuando el script se ejecuta desde `scrapers/`.
    

`try:     from scrapers.rappi_scraper import scrapeRappi     from scrapers.ubereats_scraper import scrapeUberEats     from scrapers.didi_scraper import scrape_didi_food     from scrapers.resolver import resolve_restaurant_url     from scrapers.utils import random_delay except ImportError:     from rappi_scraper import scrapeRappi     from ubereats_scraper import scrapeUberEats     from didi_scraper import scrape_didi_food     from resolver import resolve_restaurant_url     from utils import random_delay`

- Importa las funciones modulares de cada scraper + resolver + util. Fallback para distintos contextos (ej. ejecutar desde carpeta).
    

`load_dotenv() REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "25")) DELAY_MIN = float(os.getenv("DELAY_MIN", "1.2")) DELAY_MAX = float(os.getenv("DELAY_MAX", "3.5")) SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "data/screenshots") Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True) Path("data/output").mkdir(parents=True, exist_ok=True) Path("data/debug_responses").mkdir(parents=True, exist_ok=True)`

- Carga configuración y crea carpetas necesarias para screenshots, outputs y debug.
    

`USER_AGENTS = [ ... ] SCRAPER_VERSION = "v1.2-multi-platform"`

- Lista de user-agents para rotación; versión del scraper para metadata.
    

---

## `load_addresses(csv_path)`

`def load_addresses(csv_path: str) -> List[Dict[str,str]]:     rows = []     with open(csv_path, newline="", encoding="utf-8-sig") as f:         rdr = csv.DictReader(f)         for r in rdr:             rows.append({                 "addressLabel": r.get("addressLabel") or r.get("address") or "",                 "searchQuery": (r.get("searchQuery") or r.get("addressLabel") or "").strip(),                 "restaurantUrl": (r.get("restaurantUrl") or "").strip()             })     return rows`

- Lee el CSV de direcciones y normaliza tres campos por fila: `addressLabel` (para logs), `searchQuery` (si el usuario especificó búsqueda) y `restaurantUrl` (override opcional).
    

---

## `scrape_platform(platform, page, address_entry, product_targets, selector_hash)`

Función que ejecuta el scraper para una sola plataforma y un único address.

`addr_label = address_entry.get("addressLabel", "") print(f"[{datetime.now(timezone.utc).isoformat()}] Scraping {platform.upper()}: {addr_label}")`

- Info de log: qué plataforma y qué dirección estamos procesando.
    

`opts = {...}`

- Construye `opts` base con metadatos que luego pasan a scrapers (safe_name, selector hash, tag, versión).
    

### Rama `if platform == "rappi":`

- Construye `heuristic_query`: si el CSV trae `searchQuery` y ya contiene "mcdonald" lo respeta; si no, arma `"McDonald's {base}"`.
    
    - Esto es la _heurística de búsqueda_: si no hay una URL explícita, buscamos en el buscador de la plataforma usando esa query.
        
- Si la fila contiene `restaurantUrl` (override) lo usa directamente con `resolution_meta` marcado como `override`.
    
- Si no hay override, llama a `resolve_restaurant_url(page, heuristic_query)` (ese resolver es el que viste antes: abre la página de búsqueda en Rappi y elige el candidato con la mejor puntuación).
    
- Si `restaurant_url` no se resolvió, devuelve inmediatamente una lista de resultados con `scrapeStatus: "no_restaurant"` (uno por product_target) — evita seguir.
    
- Si hay URL, actualiza `opts` y llama `scrapeRappi(page, restaurant_url, product_targets, opts)` y retorna lo que devuelva el scraper de Rappi.
    

### Rama `elif platform == "ubereats":`

- Para UberEats simplemente arma un `query` y llama `scrapeUberEats(page, query, product_targets, opts)`. (Impl. específica dentro del scraper de UberEats).
    

### Rama `elif platform == "didifood":`

- Para DiDi Food el flujo es distinto: llama a `scrape_didi_food([addr_label])` que hace un análisis de mercado.
    
- Normaliza/estandariza la salida de DiDi al formato común y la devuelve.
    

### Excepciones

- Si ocurre un error dentro de `scrape_platform`, atrapa la excepción y devuelve registros con `scrapeStatus: "error_platform"` para cada product_target.
    

---

## `main(address_csv, out_file, platforms, headless)`

Función que orquesta todo el proceso:

`if platforms is None:     platforms = ["rappi", "ubereats", "didifood"] addresses = load_addresses(address_csv) product_targets = ["Big Mac", "Combo Mediano", "Coca-Cola 500ml"] all_results: List[Dict[str,Any]] = [] selector_json = json.dumps({}, sort_keys=True).encode("utf-8") selector_hash = hashlib.sha256(selector_json).hexdigest()`

- Por defecto scrappea 3 plataformas y 3 productos objetivo.
    
- `selector_hash` hoy es un hash vacío pero está preparado para versionar configuraciones de selectores si se agregan (permite cache / reproducibilidad).
    

`with sync_playwright() as pw:     browser = pw.chromium.launch(headless=bool(headless))     context = browser.new_context()     page = context.new_page()          for address_entry in addresses:         for platform in platforms:             # capture responses             responses_captured = []             def _on_response(r): responses_captured.append(r)             page.on("response", _on_response)                          results = scrape_platform(platform, page, address_entry, product_targets, selector_hash)             for r in results:                 r.setdefault("timestampUtc", datetime.now(timezone.utc).isoformat())                 r.setdefault("platform", platform)                 all_results.append(r)                          page.off("response", _on_response)             random_delay(DELAY_MIN, DELAY_MAX)     browser.close()`

- Crea navegador Playwright y una sola `page` para todas las operaciones (más eficiente que abrir una por cada operación).
    
- Antes de llamar a `scrape_platform` instala un handler `page.on("response", ...)` para capturar respuestas XHR (esas se pasan a los scrapers si las necesitan).
    
- Agrega resultados a `all_results` y limpia el event handler.
    
- Añade un delay aleatorio entre cada scraping para reducir fingerprints y no sobrecargar sitios.
    

`with open(out_file, "w", encoding="utf-8") as f:     json.dump(all_results, f, ensure_ascii=False, indent=2)`

- Guarda todos los resultados en `out_file`.
    

Luego imprime un resumen con tasas de éxito global y por plataforma:

- cuenta totales, exitosos (`scrapeStatus == "success"`) y calcula %.
    

Finalmente el `if __name__ == "__main__":` define argumentos CLI (`--addresses`, `--out`, `--platforms`, `--headless`) y ejecuta `main()`.

---

# Resumen conceptual (qué hace y por qué) — listo para decir en la presentación

1. **Orquestador central:** `multi_platform_scraper.py` es el _main_ que coordina:
    
    - lectura de direcciones,
        
    - generación de consultas heurísticas,
        
    - resolución de URL (si no hay override),
        
    - ejecución del scraper específico por plataforma,
        
    - recolección y guardado de resultados y debug dumps.
        
2. **Modularidad:** cada plataforma tiene su scraper (`scrapeRappi`, `scrapeUberEats`, `scrape_didi_food`). El main sólo prepara `opts` y decide qué invocar — facilita añadir nuevas plataformas.
    
3. **Captura de XHR / respuestas:** antes de cada scrape se engancha un handler que captura las respuestas de red. Esas respuestas son una fuente valiosa (APIs internas) para extraer fees y precios sin depender del DOM visible.
    
4. **Heurística de resolución:** si no hay `restaurantUrl` en el CSV, el main construye una `heuristic_query` (p. ej. `"McDonald's Condesa"`) y llama al `resolver` para encontrar la URL más probable en la plataforma. Esto automatiza el mapeo `address -> restaurant URL`.
    
5. **Salida estandarizada:** todos los scrapers deben devolver registros normalizados para facilitar análisis posteriores (mismo shape: `timestampUtc`, `platform`, `productTarget`, `priceValue`, `deliveryFeeValue`, `serviceFeeValue`, `scrapeStatus`, `feeSource`).
    
6. **Auditoría y debugging:** screenshots y dumps JSON/XHR se guardan en `data/debug_responses/` para investigar fallos o cambios en la UI.
    

---

# Explicaciones de términos (corto y sencillo)

- **DOM (Document Object Model):** la representación interna que el navegador crea del HTML. Cuando hacemos `page.query_selector` o `page.inner_text("body")` estamos leyendo del DOM. Es lo visible y estructurado en HTML/CSS/JS.
    
- **XHR / fetch / network requests:** páginas modernas cargan datos dinámicamente vía solicitudes de red: XHR (XMLHttpRequest) o `fetch`. Estas respuestas suelen ser JSON y a veces contienen precios, fees o datos de producto. Capturar XHR es leer esas respuestas.
    
- **`__NEXT_DATA__`:** en apps Next.js (React) la página a menudo inyecta en `window.__NEXT_DATA__` un JSON con datos estructurados. Es una fuente de datos muy valiosa porque es más precisa que parsear texto visible.
    
- **Heurística / `heuristic_query`:** un método práctico y simple para construir la búsqueda cuando falta información exacta. Ejemplo: si la fila no trae `restaurantUrl`, armamos `"McDonald's {addressLabel}"`. Esa query se usa en la búsqueda y el `resolver` puntúa candidatos y elige el más probable. _Heurística_ = regla práctica (no perfecta) usada para tomar decisiones rápidas.
    

---

# Qué decir sobre la parte `resolution_meta` y `meta["chosen_score"]` (cómo funciona la decisión)

- El `resolver` extrae links a restaurantes de la página de búsquedas.
    
- Cada candidato recibe una **puntuación** (score) según reglas simples: por ejemplo `+50` si el nombre/URL contiene "mcdonald", `+10` si el nombre contiene la query exacta.
    
- Se guarda el mejor candidato (`chosen_index`) y su `chosen_score`.
    
- Según el score se etiqueta la confianza:
    
    - `>= 35` → `high` (muy probable)
        
    - `>= 20` → `medium`
        
    - `< 20` → `low`
        
- `resolution_meta` trae la lista de candidatos, puntuaciones, el elegido e información para auditoría (por qué se eligió).
    

---

# Puntos para las diapositivas (slide content ready) — 6 slides sugeridas

1. **Slide 1 — Resumen ejecutivo (1 min)**
    
    - Objetivo: comparar precios/fees de McDonald's en Rappi, UberEats, DiDi.
        
    - Entregable: `results.json` con métricas clave (price, delivery, service, finalPrice).
        
    - Estado actual: Rappi funcionando con 3 productos; cobertura parcial; DiDi y UberEats implementados en PoC.
        
2. **Slide 2 — Arquitectura (diagrama + explicación)**
    
    - Box: `addresses.csv` → `multi_platform_scraper.py` → per-platform scrapers → outputs (`results.json`, `mapping.csv`, screenshots`).
        
    - Explicar `resolver` y `scraper` roles.
        
3. **Slide 3 — Flujo de scraping (detalle de un restaurante)**
    
    - `heuristic_query` → resolver → page.goto(restaurant_url) → fees cascade (NEXT_DATA → XHR → DOM → add-to-cart) → blocks JS → matching productos → registros.
        
    - Mencionar `feeSource` (audit trail).
        
4. **Slide 4 — Heurísticas y matching (por qué fallan/ventajas)**
    
    - Sinónimos, reglas especiales (combos vs bebida).
        
    - Puntos fuertes: flexible ante nombres distintos.
        
    - Limitaciones: cambios UI, nombres raros, ofertas embebidas.
        
5. **Slide 5 — Métricas recogidas y calidad actual**
    
    - Lista de métricas: priceValue, deliveryFeeValue, serviceFeeValue, finalPriceValue, priceWasOffer, scrapeStatus.
        
    - Estado: serviceFee a menudo `null` (por eso usamos cascada), detection rate ~44% (ejemplo que viste).
        
    - Qué falta: tiempo estimado entrega, disponibilidad, ampliar addresses (20–50), más coverage por plataforma.
        
6. **Slide 6 — Próximos pasos y recomendaciones**
    
    - Mejoras inmediatas: mejorar synonyms, incrementar coverage, instrumentar tests E2E del add-to-cart, persistir `selector_config` (versionado).
        
    - Riesgos: cambios en HTML, rate limiting / bloqueos.
        
    - Métricas de éxito: aumentar success_rate a >80%, detectar serviceFee en +90% de scrapes.
        

---

# Frases concretas (script para que leas en la presentación)

- “El orquestador es `multi_platform_scraper.py`: lee direcciones, crea queries heurísticas, resuelve URL si hace falta y llama al scraper específico de la plataforma.”
    
- “Para Rappi usamos el `resolver` que puntúa candidatos: da +50 si aparece 'mcdonald' y +10 si el nombre contiene la query — con esto asignamos una confianza high/medium/low.”
    
- “Para extraer las tarifas seguimos una cascada: `__NEXT_DATA__` (mejor) → XHR JSON → texto del DOM → simular add-to-cart. Así maximizamos probabilidades de éxito.”
    
- “Guardamos `feeSource` y dumps de debug para cada operación, lo que nos permite auditar por qué un fee vino de XHR o de DOM.”


