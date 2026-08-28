---
title: "Opción B - Guía de Ejecución del Pipeline CLI"
date: 2026-08-27
tags:
  - caso-estudio
  - rpa
  - cli
  - ejecucion
status: evergreen
---

# 🚀 Guía de Ejecución por Línea de Comandos (CLI)

Instrucciones y parámetros para invocar el pipeline de scraping multi-plataforma desde la terminal.

---

## 💻 Comando de Ejecución Principal

```bash
python scrapers/multi_platform_scraper.py \
  --addresses data/addresses.csv \
  --out data/output/multi_platform_results.json \
  --platforms rappi ubereats \
  --headless
```

---

## ⚙️ Explicación de Argumentos y Parámetros

| Parámetro | Tipo | Descripción y Propósito |
| :--- | :--- | :--- |
| `--addresses` | `str` (Ruta) | Ruta al archivo CSV con las direcciones y etiquetas de muestreo geográfico (`data/addresses.csv`). |
| `--out` | `str` (Ruta) | Destino del archivo JSON estructurado donde se compilarán los resultados consolidados (`data/output/multi_platform_results.json`). |
| `--platforms` | `list[str]` | Lista de plataformas a evaluar en la ejecución (ej. `rappi`, `ubereats`, `didifood`). |
| `--headless` | `flag` (Booleano) | Ejecuta el navegador Chromium en segundo plano sin interfaz gráfica (recomendado para producción y entornos CI/CD). |

---

## 📁 Estructura de Salida Generada

Tras completar la ejecución, el sistema produce los siguientes artefactos en disco:
1. `data/output/multi_platform_results.json`: Dataset con precios, fees y metadatos de resolución.
2. `data/mapping.csv`: Tabla de correspondencia entre direcciones y URLs resueltas.
3. `data/screenshots/`: Capturas de pantalla con timestamp de cada producto evaluado.
4. `data/debug_responses/`: Dumps JSON de respuestas de red y payloads de `__NEXT_DATA__`.
