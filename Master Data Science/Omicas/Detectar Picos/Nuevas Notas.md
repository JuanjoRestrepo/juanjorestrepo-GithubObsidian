# Detección de Picos Raman: Notas Técnicas 📝

Este documento resume la lógica, los bloques y las decisiones de diseño de los dos módulos que usamos para detectar picos en espectros Raman.

- `ETL/Silver/inspect_peaks_rsp.py` — **Versión rápida / orientada a RamanSPy** (ahora con un fallback seguro)
    
- `ETL/Silver/inspect_peaks.py` — **Versión completa y precisa** (ALS baseline, interpolación, centroide, FWHM)
    

---

## Índice

1. Resumen Ejecutivo
    
2. `inspect_peaks_rsp.py` — Bloques, Explicación y Parámetros
    
3. `inspect_peaks.py` — Bloques, Explicación y Parámetros
    
4. Diferencias Clave y Cuándo Usar Cada Uno
    
5. Recomendaciones para Comparar con la Literatura
    
6. Extensiones Útiles (Opciones Futuras)
    

---

## 1. Resumen Ejecutivo

- Si tu prioridad es **detectar picos** para **comparar posiciones** con la literatura, la mejor base es `inspect_peaks.py` porque:
    
    - Usa una **ALS baseline** robusta.
        
    - Usa **interpolación parabólica** para la posición sub-muestra.
        
    - Calcula el **centroide**, el **área** y el **FWHM**.
        
- `inspect_peaks_rsp.py` es útil para pruebas rápidas y, si RamanSPy está disponible y su API es compatible, puede usar funciones de esa librería. El nuevo script intenta usar RamanSPy y, si no puede, usa `scipy` para un comportamiento reproducible.
    

---

## 2. `inspect_peaks_rsp.py` (Rápido: Bloques y Explicaciones)

**Propósito:** Detectar picos, generar un gráfico, devolver `peaks_df` y `meta`. Intenta usar RamanSPy si está instalado.

### Bloques Clave

1. **Imports y `LOG_DIR`**
    
    - `savgol_filter`, `find_peaks` de `scipy.signal` como fallback.
        
    - `LOG_DIR` es `/opt/airflow/project/logs` por defecto; allí se guardan los PNG.
        
2. **Firma de la Función**
```python
def inspect_peaks_rsp(json_path, plot=False, return_meta=False,
                      smoothing_window=15, polyorder=3,
                      prominence=None, distance=None, height=None)
```



- `smoothing_window` debe ser impar y menor que `len(y)`.
    
- `prominence` y `distance` controlan la sensibilidad.
    

3. **Carga y Normalización**
    
    - Lee JSON → `DataFrame`.
        
    - Acepta `shift_cm-1` o `shift_cm1`.
        
4. **Suavizado**
    
    - `savgol_filter(y, window_length, polyorder)`.
        
    - Ajustes: `window_length` impar y menor que `len(y)`.
        
5. **Baseline (Simple)**
    
    - `baseline = np.min(y_smooth)` (rápido).
        
    - Produce `y_corr_shift = y_smooth - baseline`.
        
6. **Heurística de Parámetros**
    
    - `prom = 3 * std(y_corr_shift)` por defecto (o `prominence` explícito).
        
    - `distance = max(1, int(len(x)*0.002))` por defecto.
        
7. **Detección**
    
    - `find_peaks(y_corr_shift, prominence=prom, distance=dist, height=height)`.
        
    - Para cada pico reporta: `shift_cm-1`, `intensity`, `raw_index`, `prominence`.
        
8. **Gráfico**
    
    - Dibuja la curva `y_corr_shift` + puntos rojos para los picos.
        
    - Guarda `inspect_peaks_{basename}.png` (sin `.json` en el nombre).
        
9. **Retorno**
    
    - `peaks_df`, `reference_peaks` (placeholder `{}`), `meta` (si `return_meta=True`).
        

---

## 3. `inspect_peaks.py` (Completo: Bloques y Explicaciones)

**Propósito:** Detección precisa y reproducible; proporciona métricas detalladas por pico.

### Bloques Clave

1. **Imports y `LOG_DIR`**
    
    - `baseline_als`, `parabolic_interpolation`, `peak_centroid_area`, `fwhm_from_peak`.
        
    - `matplotlib.use("Agg")` para modo sin interfaz gráfica (`headless`).
        
2. **Función `baseline_als(y, lam, p, niter)`**
    
    - **Asymmetric Least Squares:** resuelve un sistema penalizado para estimar una línea base curva.
        
    - `lam` controla la suavidad; `p` define la asimetría (penaliza los picos).
        
3. **Función `parabolic_interpolation(x, y, idx)`**
    
    - Ajusta una parábola con el punto y sus vecinos para encontrar el ápice sub-muestra.
        
    - Mejora la precisión de `shift_cm-1`.
        
4. **Función `peak_centroid_area(x, y, left_idx, right_idx)`**
    
    - Integra el área vía `np.trapz` y calcula el centroide por `∫ x*y / ∫ y`.
        
5. **Función `fwhm_from_peak(x, y, peak_idx)`**
    
    - Encuentra los puntos de corte a media altura y devuelve el FWHM en unidades de `x`.
        
6. **`inspect_peaks` (Cuerpo)**
    
    - **Suavizado:** `savgol_filter` (control de ventana impar).
        
    - **Baseline:** `baseline_als(y_sg, lam, p)`.
        
    - **Shift:** si hay valores negativos, desplaza para que sean positivos.
        
    - **Heurísticas:** `prominence = 3*std(...)` si no se proporciona.
        
    - `find_peaks(..., **find_peaks_kwargs)` para obtener `peaks_idx` y `props`.
        
    - **Para cada pico:**
        
        - `parabolic_interpolation` para el ápice.
            
        - `left_base`/`right_base` desde `props` o heurística.
            
        - `centroid`, `area`, `fwhm`.
            
        - Añade una fila: `shift_cm-1, intensity, centroid, area, fwhm, raw_index, left_base_idx, right_base_idx`.
            
    - Guarda el gráfico (con el centroide dibujado) y el nombre sin `.json`.
        
    - Devuelve `peaks_df`, `reference_peaks`, `meta` (cuando `return_meta=True`).
        

---

## 4. Diferencias Clave (Resumen Práctico)

- **Baseline:** `min(y)` (rápido) vs **ALS** (robusto).
    
- **Posición:** índice discreto (`x[idx]`) vs **interpolación parabólica** (sub-muestra).
    
- **Métricas:** solo prominencia vs prominencia + centroide + área + FWHM.
    
- **Uso:** `rsp`/rápido para pruebas; `inspect_peaks.py` para análisis definitivo y comparación con la literatura.
    

---

## 5. Recomendaciones para Comparar con la Literatura

- **Fija los parámetros** antes de procesar un lote (anota `smoothing_window`, `baseline_lam`, `prominence`, `distance`).
    
- Usa `inspect_peaks.py` para obtener un `shift_cm-1` refinado (ápice interpolado).
    
- Define una **tolerancia** (p. ej., ±5 cm⁻¹ o ±10 cm⁻¹) para hacer coincidir los picos con los reportados en la literatura.
    
- Reporta además el **`area` y `fwhm`** para caracterizar si el pico corresponde a lo esperado (posición + forma).
    
- Guarda la **`meta`** por archivo para trazabilidad.
    

---

## 6. Extensiones Útiles (Próximos Pasos)

- **Ajuste por formas de pico** (Gauss/Lorentz) usando `scipy.optimize.curve_fit` en ventanas `left_base`/`right_base`.
    
- Un módulo `compare_with_literature.py` que:
    
    - carga un CSV con picos de referencia,
        
    - para cada pico detectado busca coincidencias dentro de una tolerancia,
        
    - reporta las coincidencias, los desplazamientos y los marcadores de alerta.

- Exportar los resultados por lote a CSV / tabla SQL (ya tienes `save_peaks.py` → integrarlo).


