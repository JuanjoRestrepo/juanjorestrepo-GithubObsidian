

## Cómo hacemos que la Opción A sea **fácil de defender** (estrategia)

1. **Combina pruebas objetivas + lenguaje natural**
    - Primero: cálculos reproducibles (estadísticas, tests, anomalías, cambios porcentuales, segmentaciones).
    - Segundo: LLM **consume resultados** (resúmenes tabulares, top-N anomalies) y genera insights explicables.
    - Resultado: siempre puedes mostrar evidencia numérica detrás de cada afirmación del LLM.
        
2. **Salida estructurada del LLM (JSON)**
    - Exigir al LLM que devuelva un JSON con campos claros: `summary`, `top_drivers`, `confidence_score`, `supporting_evidence_ids`.
    - Eso facilita evaluar y cuantificar (automatizar checks).
        
3. **Grounding / RAG / Verificación**
    
    - Alimentar al LLM con passages sintetizados (resumen de tablas o chunks) o with embeddings.
        
    - Si una afirmación no tiene evidencia suficiente, la respuesta debe declarar “sin evidencia suficiente”.
        
4. **Métricas concretas para la defensa**
    
    - **Coverage**: % de afirmaciones del LLM respaldadas por datos.
        
    - **Precision (facts)**: ratio de afirmaciones correctas en una muestra (human eval, n=30).
        
    - **Latency / Cost**: tokens promedio por query y coste estimado (útil para preguntas de producción).
        
    - **Quality**: utilidad promedio (human rating 1–5).
        
5. **Demo muy dirigido** (lo que debes mostrar en 3 minutos):
    
    - Slide: objetivo y arquitectura (1 min).
        
    - Notebook/Streamlit: 2 queries — 1) “¿Por qué bajaron orders en Zone X la semana L0?” (mostrar cifras + JSON del LLM + evidencias), 2) “Top 3 zonas con riesgo de caída en next 2 semanas” (métrica + recomendación).
        
    - Mostrar la comprobación automática para la afirmación crítica.