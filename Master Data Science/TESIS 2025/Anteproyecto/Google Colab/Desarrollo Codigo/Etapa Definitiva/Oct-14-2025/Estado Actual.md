
# 1) Evaluación rápida — ¿vas bien?
Sí — tu trabajo está en buen camino. Puntos fuertes:
- El anteproyecto está completo: objetivos, preguntas de investigación, entregables y cronograma están bien definidos.
    
- Elegiste un dataset público apropiado (SICAPv2) y documentaste cantidad de WSI/patches y la necesidad de particionado por paciente.
    
- El notebook ya automatiza descarga, extracción y construcción de un `dataset_manifest.csv`, y analiza máscaras — eso es exactamente lo que necesitas para reproducibilidad de datos.
    
- Adoptaste criterios de reproducibilidad (splits por paciente, seeds, versionado) en el documento — muy importante.
    

Conclusión: estructura y acercamiento metodológico correctos; lo que sigue es afinar implementación, robustecer experimentos y formalizar reproducibilidad / reportes.



---

# 2) Errores / riesgos detectados y prioridades de corrección

Ordenados por prioridad (alto → bajo):

1. **Verificar mapping slide ↔ mask ↔ labels y el `dataset_manifest.csv`**
    
    - Riego: máscaras faltantes o nombres mal parseados pueden producir bags incompletos o labels incorrectas. En el notebook creas manifest (buena práctica), confirma que _todo_ slide_id del `wsi_labels.xlsx` tenga las mascarillas esperadas y que el `dominant_mask_label` coincide con `Gleason_primary` cuando corresponda; si hay discordancias documentarlas y decidir reglas.
        
    - Acción: revisar `slide_mask_vs_wsi_labels.csv`, contar slides con máscaras faltantes y documentar. (Tu notebook ya exporta esto; valida las discrepancias).
        
2. **Asegurar particionado estratificado por paciente y evitar data leakage**
    
    - Riego: mezclar parches de un mismo paciente en train/test. En el anteproyecto está claro que usarás particionado por paciente; implementarlo cuidadosamente en tus scripts (no por parche).
        
    - Acción: crear función `getStratifiedPatientFolds(labels_df, n_folds, seed)` que devuelva listas de patient_ids por fold y que genere CSVs con splits (train/val/test) por slide.
        
3. **Caching de embeddings / pipeline por etapas** (urgente si tienes GPU/tiempo limitado)
    
    - Riego: entrenar MIL desde imágenes brutas es muy costoso. Mejor extraer embeddings con una CNN una vez, guardarlos y usarlos para experimentar con varios agregadores MIL (rápido y reproducible). Tu metodología lo contempla, pero prioriza el caching.
        
    - Acción: script `extractEmbeddings.py` que: lee patches, aplica transform, pasa por CNN (ResNet50/EfficientNet), guarda `.npy` por patch y un index (manifest) con ruta y vector.
        
4. **Normalización de tinción y filtrado por tejido**
    
    - Mejora: aplicar Macenko o Reinhard para normalizar H&E entre WSI; usar filtrado de patches por % tejido (tu notebook tiene `quick_has_tissue`) — formaliza umbrales y registralos en metadatos.
        
5. **Estrategia de muestreo dentro de cada bag (submuestreo, top-K, hard-mining)**
    
    - Mejora: define y compara al menos 3 estrategias (aleatorio, top-k por atención previa, equilibrio por clase). Documenta cómo afectan tiempo y métricas.
        
6. **Reproducibilidad del entorno y registro de experimentos**
    
    - Mejora: entrega `requirements.txt`/`environment.yml`, `seed` global, `git` + tags para versiones y logs con W&B o TensorBoard. Lo mencionas en el plan; hay que implementarlo.
        
7. **Evaluación estadística y estimación de incertidumbre**
    
    - Mejora: reportar métricas con IC (bootstrap) y tests estadísticos entre modelos; para incertidumbre usa MC Dropout o VGPMIL-PR (mencionado en tu marco).


---

