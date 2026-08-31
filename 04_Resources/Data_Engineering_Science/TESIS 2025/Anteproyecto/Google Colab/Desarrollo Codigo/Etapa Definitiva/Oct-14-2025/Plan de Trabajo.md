

# 4) Plan paso-a-paso (sprints) — entrega incremental

Propongo sprints de 1 a 2 semanas, fáciles de trackear. Si quieres, voy generando scripts y notebooks por sprint.

Sprint 0 — **Verificación de datos (ya parcialmente hecho)**

- Revisar `dataset_manifest.csv` y `slide_mask_vs_wsi_labels.csv`. Documentar discrepancias. (Tu notebook ya genera esto; revisa resultados y sube aquí si quieres que los analice).
    

Sprint 1 — **Preprocesamiento y extracción de patches reproducible**

- Implementar stain normalization, tissue filtering, guardar patches y manifest final versionado. Crear `makePatches.py` + README.
    

Sprint 2 — **Extractor de embeddings y caching**

- Script `extractEmbeddings.py` con opciones (model, layer, batchSize). Guardar `.npy` y manifest con vector path. Test rápido.
    

Sprint 3 — **Baseline MIL: ABMIL sobre embeddings**

- Implementar, validar con 5-fold CV estratificado por paciente; reportar métricas por fold y promedio + IC.
    

Sprint 4 — **Mejoras de pooling y muestreo**

- Probar top-k, hierarchical pooling, CLAM/DSMIL si implementable; comparar. Documentar costo computacional.
    

Sprint 5 — **Graph-MIL y probabilístico (VGPMIL-PR)**

- Implementar Graph-MIL (usar DGL o PyTorch Geometric) y probar en subset por tiempo. Implementar VGPMIL-PR para incertidumbre.
    

Sprint 6 — **Explainability + análisis clínico de errores**

- Generar heatmaps, Grad-CAM, análisis de casos FP/FN y correlación con anotaciones (si existen).
    

Sprint 7 — **Reporte final y reproducibilidad**

- Compilar resultados, generar tablas comparativas, figuras ROC, guardar environment, scripts para replicar experimentos y CRONOGRAMA final.


