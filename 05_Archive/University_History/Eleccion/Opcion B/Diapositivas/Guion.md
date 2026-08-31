---
title: "Opción B - Guion Oficial de la Presentación por Diapositivas"
date: 2026-08-27
tags:
  - caso-estudio
  - presentacion
  - guion
  - insights
status: evergreen
---

# 📑 Guion Oficial de la Presentación por Diapositivas

Script palabra por palabra estructurado para guiar la exposición formal de 10 a 12 minutos ante el comité evaluador.

---

## 🎞️ Diapositiva 1: Portada (0:00 – 0:40)
> *"Buen día. Mi nombre es Juan José Restrepo. Hoy presento el caso técnico: **‘Sistema de Competitive Intelligence y Análisis de Tarifas para Rappi’**."*

---

## 🎞️ Diapositiva 2: Contexto y Objetivo (0:40 – 1:30)
> *"Las plataformas de delivery compiten en tiempo real mediante esquemas de tarifas dinámicas y subsidios cruzados. El objetivo de este proyecto fue diseñar e implementar un pipeline automatizado para extraer, validar y comparar precios y tarifas entre Rappi y Uber Eats, derivando recomendaciones estratégicas de negocio."*

---

## 🎞️ Diapositiva 3: Arquitectura Técnica (1:30 – 2:30)
> *"Partiendo de un archivo de direcciones de muestreo geográfico, un orquestador ejecuta scrapers modulares por plataforma con Playwright y consolida los registros en JSON y CSV. Esta arquitectura garantiza trazabilidad total mediante capturas de pantalla, intercepción de red y ejecución reproducible."*

---

## 🎞️ Diapositiva 4: Estrategia de Scraping en Cascada (2:30 – 3:30)
> *"Para maximizar la resiliencia del sistema, implementamos una cascada en cuatro niveles: extracción directa desde `window.__NEXT_DATA__`, intercepción de respuestas de red XHR, parseo del DOM visible y un mecanismo de fallback mediante simulación Add-to-Cart para revelar tarifas ocultas en el carrito."*

---

## 🎞️ Diapositiva 5: Normalización y Control de Calidad (3:30 – 4:30)
> *"Los datos crudos pasan por un proceso de sanitización numérica (`sanitize_number`), validación de umbrales máximos razonables y verificación de completitud de campos. Cada registro conserva su origen de extracción (`feeSource`) para facilitar la auditoría de datos."*

---

## 💡 Bloque de Insights Estratégicos de Negocio

### 🍔 Insight 1: Ventaja en Producto Individual (4:30 – 5:40)
- **Métrica:** Big Mac — Rappi ($\$154.40\text{ MXN}$) vs. Uber Eats ($\$181.87\text{ MXN}$).
- **Diagnóstico:** Rappi es un **$15.1\%$ más económico** en el ítem individual de referencia.
- **Acción Recomendada:** Capitalizar esta brecha en campañas de marketing digital enfocadas en la percepción de valor para pedidos unitarios.

---

### 🍟 Insights 2 y 3: El Ataque en la Canasta Completa (5:40 – 7:20)
- **Métrica:** Combo Mediano ($+24.7\%$ en Rappi) y Coca-Cola 500ml ($+20.1\%$ en Rappi).
- **Diagnóstico:** Uber Eats subsidia agresivamente el producto de mayor ticket promedio (combos) y el de mayor frecuencia (retail/bebidas).
- **Acción Recomendada:** Reestructurar la política de precios en combos y categorías complementarias para no perder margen en el valor promedio del pedido (*Average Order Value*).

---

### ⚠️ Insight 4: Detección de Anomalías en Delivery Fees (7:20 – 8:20)
- **Diagnóstico:** Identificación de tarifas atípicas en Uber Eats ($\$137.00\text{ MXN}$) asociadas a bloqueos o tarifas de contingencia.
- **Corrección Técnica:** Implementación de validaciones basadas en el Costo Total de Entrega ($\text{Delivery Fee} + \text{Service Fee}$) con soporte visual en capturas.

---

### 📍 Insight 5: Subsidios Agresivos por Zona Geográfica (8:20 – 10:00)
- **Diagnóstico:** La diferencia en el precio final total no proviene del precio base del producto, sino del costo de envío: Uber Eats subsidia casi el $100\%$ del *Delivery Fee* en zonas de expansión (Zona 1 y Zona 2).
- **Acción Recomendada:** Diseñar un esquema de **Delivery Fee dinámico por zona**, implementando un piloto que subsidie el envío en tres zonas estratégicas durante 4 semanas para medir la recuperación de cuota de mercado.

---

### 🗺️ Insight 6: Estrategia Bimodal y Riesgo de Crecimiento (10:00 – 11:30)
- **Diagnóstico:** Comportamiento bimodal: Rappi domina en zonas de alto poder adquisitivo (Condesa, Polanco); Uber Eats lidera en zonas de crecimiento demográfico (Tlalpan Centro).
- **Acción Recomendada:** En zonas consolidadas, competir en velocidad y calidad operativa; en zonas de expansión, neutralizar precios mediante subsidios focalizados.

---

## 🎞️ Diapositiva 6: Conclusiones y Cierre (11:30 – 12:00)
> *"En conclusión: el sistema proporciona una ventaja informativa decisiva. Pasamos de una visión intuitiva a un diagnóstico basado en datos duros. Agradezco su atención y quedo a su disposición para resolver cualquier pregunta técnica o de negocio."*