
El archivo `scrapers/utils.py` centraliza funciones **auxiliares** y **genéricas** que otros scripts (como `resolver.py`, `rappi_scraper.py`, `playwright_poc.py`) necesitan.  
Incluye utilidades para:

- Manejo de tiempo y retrasos aleatorios (anti-bloqueo de bots).
    
- Limpieza de cadenas numéricas (precios).
    
- Reintentos con backoff exponencial.
    
- Guardado de JSONs y logs.
    
- Capturas de pantalla seguras.
    

Estas funciones reducen duplicación


```python
def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()
```

Devuelve la hora actual en formato ISO 8601 UTC,
Ejemplo: "2025-10-16T21:04:30.123456+00:00".

Se usa para marcar cada registro del scraping con su timestamp exacto, útil para trazabilidad y auditoría.

---

```python
def sanitize_number(num_str: Optional[str]) -> Optional[float]:

    if not num_str:

        return None

    s = str(num_str).strip()

    s = re.sub(r"[^\d\.,\-]", "", s)

    # handle comma/point conventions

    if s.count(",") and s.count("."):

        if s.rfind(",") > s.rfind("."):

            s = s.replace(".", "").replace(",", ".")

        else:

            s = s.replace(",", "")

    else:

        if s.count(",") == 1 and len(s.split(",")[-1]) == 2:

            s = s.replace(",", ".")

        else:

            s = s.replace(",", "")

    try:

        return float(s)

    except Exception:

        return None
```

**Objetivo:** limpiar y convertir una cadena textual (ej. “$89,90” o “89.000,50”) en un número `float` usable.

**Explicación detallada:**

1. Si `num_str` es `None` o vacío → devuelve `None`.
    
2. Elimina cualquier carácter que **no sea dígito, coma o punto**:
→ `"Precio: $89,90"` → `"89,90"`.


- Maneja distintas **convenciones internacionales** de separadores:
    
    - Si hay **coma y punto**, detecta cuál se usa como decimal.
        
    - Si solo hay coma y parece decimal (dos dígitos después), reemplaza coma por punto.
        
    - Si solo hay comas como separadores de miles, las elimina.
        
        
**Ejemplos:**

|Entrada|Resultado|Comentario|
|---|---|---|
|`"89,90"`|89.9|formato europeo|
|`"1.200,50"`|1200.5|limpia miles y decimales|
|`"$199"`|199.0|elimina símbolo|
|`None`|None|inválido|

✅ **Uso:** se llama en `rappi_scraper.py` para transformar precios o tarifas en floats antes de guardarlos.

---

```python
def retry(func: Callable, attempts: int = 3, base_delay: float = 0.6):

```
**Propósito:** ejecutar una función con **reintentos automáticos** en caso de error (patrón de “retry with backoff”).

**Flujo:**

1. Intenta ejecutar `func()` hasta `attempts` veces.
2. Si falla, espera un tiempo antes de volver a intentar:


---

```python
def random_delay(min_s: float = 1.2, max_s: float = 3.5):
    time.sleep(random.uniform(min_s, max_s))
```
- Introduce una **pausa aleatoria** entre acciones del scraper.
    
- Ayuda a simular comportamiento humano y **evita bloqueos automáticos** por detección de bots.

---

```python
def dump_json_to(path: str, obj: Any):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
```

Guarda cualquier objeto Python como archivo JSON:

1. Crea directorios si no existen (`parents=True`).
    
2. Escribe el contenido de forma **formateada y legible** (`indent=2`).
    
3. Usa `ensure_ascii=False` para conservar acentos y caracteres especiales.
    

✅ **Usos:**

- Guardar respuestas XHR o estructuras capturadas (`debug_responses`).
- Registrar resultados parciales del scraping para análisis posterior.

---

```python
def setup_logging(name: str) -> logging.Logger:

```
- Configura un **logger estandarizado** con nombre personalizado.
- Solo se crea si no existe (evita duplicados).
- Define formato:

Centraliza cómo se imprimen los logs; mantiene consistencia en todo el pipeline.

---

```python
async def save_screenshot(page, path: str, description: str = ""):
```

Guarda una captura de pantalla de la página, con manejo de errores robusto.

Usa await page.screenshot(...) para capturar en modo asincrónico (compatible con Playwright async).

Si el directorio no existe, lo crea.

Imprime confirmación o error.

✅ Propósito: capturar evidencia visual del estado del scraping (errores, bloqueos, etc.).