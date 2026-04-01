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
 
 **¿Lenguaje y entorno?**
- Python
- Jupyter / Colab inicialmente
- luego migramos a estructura `src/`

**¿Nivel de ingeniería desde el inicio?**
Opción A (más ágil):
- Notebook primero
- luego refactorizamos a pipeline

Opción B (más pro desde el día 1):
- estructura de proyecto
- scripts modulares
- logging

**¿Target inicial?**
Te recomiendo:
✔ Empezar con:
- clasificación (win/draw/loss)
Luego escalar a:
- modelo de goles (Poisson)

--- 

# Decisión Final

Para balancear velocidad + calidad:

1. Empezamos en **notebook (EDA + limpieza)**
2. Pero con mentalidad de pipeline
3. Luego migramos a `src/`


---

# Notebook done
# Qué acabamos de hacer (importante)

Sin escribir teoría, ya implementamos:

✔ Ingesta de datos  
✔ Limpieza inicial  
✔ Validación  
✔ Feature básica (target)  
✔ EDA  
✔ Primer dataset curado

Esto es exactamente la **Fase 1 — Data Foundation**.


