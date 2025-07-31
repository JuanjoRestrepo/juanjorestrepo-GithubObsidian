
# 1. ¿Qué es un _Data Pipeline_?
- Cadena de procesos desde un sitio objetivo hasta un lago (`Data Lake`) o `“data pool” `que alimenta decisiones o modelos de IA:
    1. **Collection**
    2. **Ingestion**
    3. **Preparation**
    4. **Computation**
    5. **Presentation**

- Etapas pueden ocurrir simultáneamente, con múltiples orígenes/destinos; algunos pipelines pueden ser parciales (ej. solo etapas 1-3).


# 2. ¿Qué distingue a un _Big Data Pipeline_?

- Diseñado para **manejo a gran escala**: **captura masiva de datos** mejora precisión y reduce margen de error en decisiones estratégicas.
- Aplicaciones principales:
    - **Analítica predictiva** (p. ej., demanda o mercados)
    - **Captura de mercado en tiempo real** mediante correlación de datos desde redes sociales, e‑commerce, anuncios, etc.
- Requisitos:
    - **Escalabilidad**: activar/desactivar recursos según volumen.
    - **Fluidez**: procesar múltiples formatos (JSON, CSV, HTML) limpiándolos, unificándolos y estructurándolos.
    - **Gestión concurrente de peticiones**: simultaneidad rápida y eficiente.

# 3. Beneficios para las empresas

1. **Consolidación de datos**: múltiples fuentes convergen a un solo depósito centralizado.
2. **Reducción de fricción / time‑to‑insight**: disminuye el esfuerzo en limpieza y preparación inicial. 
3. **Compartimentación**: sólo stakeholders relevantes acceden a datos específicos según roles. 
4. **Uniformidad**: estandariza formatos y facilita movimiento entre sistemas/depositarios.

# 4. Tipos de arquitectura de Data Pipeline

| Tipo de Pipeline | Características clave                                              | Ejemplo de uso                                                                      |
| ---------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Streaming**    | Procesamiento en tiempo real; baja latencia, respuesta inmediata   | OTA repricing dinámico (vuelos, hotelería)                                          |
| **Batch-based**  | Procesos periódicos de grandes volúmenes; mayor latencia aceptable | Institución financiera analizando datos de mercado Nasdaq                           |
| **Híbrido**      | Combina batch y streaming para flexibilidad y escalabilidad        | Corporaciones grandes que retienen datos en formato bruto para futura adaptabilidad |


