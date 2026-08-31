
# 5) Entregables que debes mantener (y cómo estructurarlos)

- `data/` (raw, processed, manifest versioned) + `DATA_LICENSE.md`.
    
- `notebooks/` para EDA y ejemplo reproducible (no usar notebooks para entrenamiento pesado).
    
- `src/` con: `makePatches.py`, `extractEmbeddings.py`, `trainMil.py`, `evaluate.py`.
    
- `experiments/` con cada experimento → `metadata.json` (git hash, seed, params).
    
- `reports/` con tablas, figuras y análisis estadístico.
    
- `environment.yml` / Dockerfile + `README.md` con instrucciones reproducibles.

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - Master Data Science]]
- **Dominio**: Master Data Science
