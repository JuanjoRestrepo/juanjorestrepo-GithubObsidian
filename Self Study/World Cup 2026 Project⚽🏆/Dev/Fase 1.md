# 🚀 Fase 1 — Data Foundation (AHORA)

## Objetivo

Construir un dataset limpio, confiable y listo para modelar.

---

## Paso 1: Seleccionar fuente base

**Dataset principal:**
- `international_results` (histórico completo de partidos)
**Razón:**
- Cobertura amplia (más de 100 años)
- Formato estructurado
- Ideal para entrenamiento

## Paso 2: Definir esquema de datos

**Variables mínimas necesarias**
- date
- homeTeam
- awayTeam
- homeScore
- awayScore
- tournament
- city
- country
- neutral

## Paso 3: Pipeline inicial
Vamos a construir esto:
```
RAW DATA → CLEAN DATA → MODEL DATASET
```

## Paso 4: Primera implementación

1. Descargar dataset
2. Cargarlo en pandas
3. Estandarizar nombres (camelCase, como prefieres)
4. Crear variable target
5. Validar calidad básica
 
 ¿Lenguaje y entorno?
- Python
- Jupyter / Colab inicialmente
- luego migramos a estructura `src/`

