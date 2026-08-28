---
title: "Opción B - Módulo de Utilidades Transversales y Sanitización"
date: 2026-08-27
tags:
  - caso-estudio
  - rpa
  - utilidades
  - data-cleaning
  - python
status: evergreen
---

# 🛠️ Módulo de Utilidades Transversales: `utils.py`

Centraliza funciones auxiliares reutilizables diseñadas para garantizar la limpieza de datos numéricos, el manejo de reintentos con tolerancia a fallos, pausas estocásticas anti-bloqueo y persistencia estructurada.

---

## 💻 Funciones Principales y Especificación

### 1. Generación de Timestamp Estándar (`now_utc_iso`)
Genera la marca temporal en formato ISO 8601 UTC para etiquetar cada registro y garantizar trazabilidad histórica.

```python
def now_utc_iso() -> str:
    """Retorna la fecha y hora actual en formato ISO 8601 UTC."""
    return datetime.now(timezone.utc).isoformat()
```

---

### 2. Sanitización Numérica de Precios y Fees (`sanitize_number`)
Transforma cadenas de texto heterogéneas con símbolos de moneda, espacios y convenciones de comas/puntos en valores de punto flotante (`float`) válidos.

```python
def sanitize_number(num_str: Optional[str]) -> Optional[float]:
    """Limpia y convierte representaciones textuales de precios a float.

    Maneja convenciones internacionales de separadores decimales y de miles.
    """
    if not num_str:
        return None

    s = str(num_str).strip()
    s = re.sub(r"[^\d\.,\-]", "", s)

    # Manejo de presencia simultánea de coma y punto
    if s.count(",") and s.count("."):
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        # Caso de coma como separador decimal estándar
        if s.count(",") == 1 and len(s.split(",")[-1]) == 2:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")

    try:
        return float(s)
    except Exception:
        return None
```

#### 📊 Tabla de Casos de Prueba de Sanitización

| Cadena de Entrada | Salida (`float`) | Convención / Regla Aplicada |
| :--- | :---: | :--- |
| `"$ 89,90"` | `89.90` | Eliminación de símbolo y conversión de coma decimal. |
| `"1.200,50 MXN"` | `1200.50` | Limpieza de separador de miles (`.`) y conversión de coma decimal (`,`). |
| `"$199"` | `199.00` | Extracción de entero simple. |
| `"Gratis / $0.00"` | `0.00` | Filtrado de texto alfanumérico. |
| `None` / `""` | `None` | Manejo seguro de nulos. |

---

### 3. Delays Estocásticos Anti-Detección (`random_delay`)
Introduce pausas aleatorias no deterministas entre peticiones para simular el comportamiento humano y prevenir bloqueos por WAF.

```python
def random_delay(min_s: float = 1.2, max_s: float = 3.5) -> None:
    """Introduce una pausa aleatoria uniforme entre min_s y max_s segundos."""
    time.sleep(random.uniform(min_s, max_s))
```

---

### 4. Persistencia JSON Segura (`dump_json_to`)
Crea directorios intermedios automáticamente y persiste objetos en formato JSON con indentación y preservación de caracteres Unicode.

```python
def dump_json_to(path: str, obj: Any) -> None:
    """Guarda un objeto serializable en disco en formato JSON formateado."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
```

---

## 📋 Resumen de Utilidades del Sistema

| Función | Responsabilidad Técnica | Módulos Consumidores |
| :--- | :--- | :--- |
| `now_utc_iso()` | Trazabilidad temporal estandarizada UTC. | `multi_platform_scraper.py`, `rappi_scraper.py` |
| `sanitize_number()` | Normalización y conversión de precios y fees a `float`. | `rappi_scraper.py`, `ubereats_scraper.py` |
| `random_delay()` | Prevención de detección anti-bot mediante pausas estocásticas. | `multi_platform_scraper.py`, `resolver.py` |
| `dump_json_to()` | Exportación atómica y segura de resultados y payloads debug. | `multi_platform_scraper.py`, `utils.py` |
| `setup_logging()` | Instanciación de loggers estructurados con formato unificado. | Todos los submódulos |
| `save_screenshot()` | Captura de pantallas de evidencia visual en fallos o éxito. | `rappi_scraper.py`, `ubereats_scraper.py` |
