
# 1. El resultado principal: EXCELENTE

La normalización funcionó correctamente.

Lograste transformar:

```
3 hojas Excel orientadas a reporting visual
```

en:

```
2 datasets analíticos unificados
```

Eso era exactamente el objetivo de la Section 8.

---
# 2. categories_df — Evaluación Profesional

El dataset quedó MUY bien estructurado.

## Estructura final

|Column|Correcto|
|---|---|
|handling_channel|✅|
|contact_reason|✅|
|volume|✅|
|percentage|✅|

Excelente schema.

Muy limpio para:

- Power BI,
- Plotly,
- KPIs,
- agregaciones,
- joins futuros.

----

# 3. El `handling_channel` fue una decisión MUY importante

Esto es probablemente una de las mejores decisiones estructurales hasta ahora.

Porque ahora puedes hacer:

|Análisis|Posible|
|---|---|
|agent vs bot|✅|
|hybrid leakage|✅|
|containment|✅|
|stacked bars|✅|
|funnel analysis|✅|
|Power BI slicers|✅|

Sin esta columna:  
todo se volvería mucho más difícil.

---

# 4. Las proporciones tienen sentido operacional

Esto es MUY importante.

Los números “huelen bien”.

Eso es una habilidad muy importante en analytics:

- detectar datos absurdos,
- inconsistencias,
- volúmenes sospechosos.

Aquí NO veo nada sospechoso estructuralmente.
## Ejemplo

## Agent Only

```
Returns & Refunds → 29%Existing Order → 26%
```

Totalmente lógico.

Porque:

- devoluciones,
- tracking,
- problemas post-compra

son normalmente los mayores drivers de CX en retail e-commerce.


## Hybrid

```
Existing Order → 41%
```

MUY interesante.

Esto refuerza fuertemente la hipótesis de:

```
transactional escalation leakage
```

Porque:

- el bot probablemente inicia,
- PERO no logra cerrar.

## Bot Only

```
Returns & Refunds → 44%Existing Order → 40%
```

Esto es MUY interesante estratégicamente.

Porque significa:

```
sí existe automatización parcial exitosa
```

El bot NO está completamente fallando.

Eso es importante.


---
# 5. Lo MÁS importante del categories_df

Ahora podemos medir:
## “Automation Distribution”

Por ejemplo:

|Intent|Bot|Hybrid|Agent|
|---|---|---|---|
|Returns|X|Y|Z|

Y eso desbloquea:
- opportunity scoring,
- automation roadmap,
- prioritization matrix.

Este dataset es oro para analytics.

---

# 6. Observación MUY importante

Mira esto:

## Agent Only

```
Customer Feedback → 18%
```

## Bot Only

```
Customer Feedback → ~0%
```

Esto es extremadamente importante.


## ¿Qué podría indicar?

Posibles hipótesis:

|Hipótesis|Significado|
|---|---|
|El bot evita feedback|routing directo a humano|
|Feedback requiere empatía|baja automatización|
|Mala clasificación|feedback no reconocido|
|Decisión operacional|feedback nunca automatizado|

MUY buen insight para presentación.

---
# 7. “Not defined by Bot”

Esto es probablemente uno de los KPIs MÁS importantes del caso.

## Mira esto

## Hybrid

```
Not defined by Bot → 1022
```

## Bot Only

```
Not defined by Bot → 4833
```

Esto es MUY serio operacionalmente.


## ¿Por qué?

Porque implica:

```
el sistema no logró mapear correctamentela intención del usuario
```

Y aun así algunas terminaron:

- escaladas,
- o “resueltas”.

## Esto merece visualización propia

En Power BI:  
- yo haría una tarjeta/KPI específica:

## Undefined Intent Rate
Muy importante.


---
# 8. subcategories_df — Excelente también

Esto quedó MUY bien.
## Estructura

|Column|Correcto|
|---|---|
|handling_channel|✅|
|contact_reason|✅|
|sub_category|✅|
|volume|✅|
|percentage|✅|

---

# 9. Aquí es donde realmente vive el valor analítico

Porque:  
las macro categorías ayudan a storytelling ejecutivo.

Pero:
- las subcategorías revelan las oportunidades accionables reales


## Ejemplo

“Returns & Refunds” es demasiado amplio.

Pero:

| sub_category  |
| ------------- |
| Return status |
| label Request |
| How to return |

ya permite:
- automatización,
- integración,
- diseño de flows.


---

# 10. “Left Blank” es MUY importante

Esto es uno de los hallazgos más relevantes hasta ahora.

## Mira esto

```
Customer Feedback → Left Blank → 70,731
```

Eso es ENORME.

## ¿Qué puede significar?

Posibles interpretaciones:

|Interpretación|Riesgo|
|---|---|
|Falta taxonomía|mala observabilidad|
|Intent fallback|mala clasificación|
|Data loss|pérdida analítica|
|Mala instrumentación|tracking insuficiente|

## Esto NO debe ignorarse

Muchos analistas lo ignorarían. Pero esto probablemente indica:

```
uno de los mayores problemasde observabilidad conversacional
```


---

# 11. Otro insight MUY fuerte

## Mira esto:

```
Explain how to order
```

aparece MUY alto en:

- agent_only.

Eso es muy interesante.

## ¿Por qué?

Porque ese intent DEBERÍA ser altamente automatizable.

Entonces si termina mucho en humanos, posiblemente indica:

|Posible problema|Significado|
|---|---|
|UX mala|usuarios confundidos|
|flujo roto|bot no explica bien|
|discoverability|usuarios no encuentran ayuda|
|language issue|intent classification pobre|

Muy buen insight ejecutivo.

---

# 12. La cardinalidad se ve lógica

## categories_df

50 filas aprox.

Correcto.

---

## subcategories_df

469 filas.

También lógico.

Eso refleja:

- granularidad operacional,
- diversidad de intents,
- taxonomía más rica.

Nada raro ahí.

---

# 13. La normalización quedó BI-ready

Esto es MUY importante.

Tus datasets ya están listos para:

|Uso|Estado|
|---|---|
|Power BI|✅|
|Plotly|✅|
|React Dashboard|✅|
|KPI engineering|✅|
|Pareto analysis|✅|
|Opportunity scoring|✅|

Excelente.