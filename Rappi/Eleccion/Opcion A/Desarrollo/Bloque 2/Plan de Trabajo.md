---
title: "Opción A - Bloque 2: Plan de Análisis y Generación de Insights"
date: 2026-08-27
tags:
  - caso-estudio
  - plan-trabajo
  - insights
  - analisis-datos
status: evergreen
---

# 📈 Bloque 2: Flujo de Trabajo para Análisis e Informe de Insights

Propuesta metodológica para transformar los datos crudos consolidados en hallazgos estratégicos accionables.

---

## 🔄 Fases del Flujo de Trabajo

```mermaid
flowchart LR
  F1["1. Exploración de Datos Crudos"] --> F2["2. Limpieza & Transformación"]
  F2 --> F3["3. Visualización & Detección"]
  F3 --> F4["4. Top 5 Insights Accionables"]
  F4 --> F5["5. Artefactos Entregables"]
```

### 1. Exploración de Datos Crudos
- Carga de datasets estructurados con Pandas.
- Verificación de tasas de integridad: conteo de registros exitosos vs. valores faltantes.
- Evaluación de dispersión de precios y tarifas (`deliveryFeeValue`, `serviceFeeValue`).

### 2. Limpieza y Transformación
- Imputación justificada o tratamiento de valores nulos.
- Normalización léxica de nombres de productos y marcas.
- Deduplicación de registros en combinaciones producto-zona.

### 3. Visualizaciones e Insights
- Comparativas de precios medios para productos de referencia (*Big Mac*, *Combo Mediano*, *Coca-Cola 500ml*).
- Proporción de productos bajo esquemas promocionales (`priceWasOffer = true`).
- Mapeo de tarifas de envío por zona geográfica para identificar brechas de competitividad.

### 4. Estructura de los Top 5 Insights Accionables
Cada insight presentado debe cumplir con la tríada:
1. **Hallazgo Cuantitativo:** Qué se descubrió con datos precisos.
2. **Impacto de Negocio:** Por qué es crítico para el margen o la cuota de mercado.
3. **Acción Recomendada:** Qué decisión táctica o técnica debe implementarse.

### 5. Formato de Entrega
- Notebook documentado con ejecución reproducible.
- Diapositivas ejecutivas en PDF con gráficos vectoriales y síntesis estratégica.
