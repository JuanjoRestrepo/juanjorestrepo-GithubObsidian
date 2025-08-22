
# 1) Resumen rápido del flujo general (aplicable a ambas)

Cada implementación sigue esencialmente estos pasos:

1. **Lectura del JSON** → crear arrays `x` (shift cm⁻¹) y `y` (intensidad).
2. **Suavizado** del espectro (reduce ruido de alta frecuencia).
3. **Remoción de baseline** (corrige señal continua/offset).
4. **Preparación / desplazamiento** (asegurar que la señal esté positiva para detección).
5. **Detección de picos** con un detector (Scipy `find_peaks` o Ramanspy).
6. **Refinamiento / cálculo de métricas**: posición sub-muestra, centroid, área, FWHM, left/right bases, prominencia.
7. **Salida**: DataFrame con columnas útiles y (opcional) guardar gráfico.

---

# 1. `inspect_peaks.py`

## Usamos `find_peaks`

```python
  # --- Cargar JSON ---
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)


    if df.empty:
        meta = {"error": "empty"}
        return (pd.DataFrame(), {}, meta) if return_meta else (pd.DataFrame(), {})

  
    # Normalizar columna shift
    if "shift_cm1" in df.columns and "shift_cm-1" not in df.columns:
        df = df.rename(columns={"shift_cm1": "shift_cm-1"})

    if "shift_cm-1" not in df.columns:
        raise KeyError("No se encontró 'shift_cm-1' ni 'shift_cm1' en el JSON")

  
    x = np.asarray(df["shift_cm-1"], dtype=float)
    y = np.asarray(df["intensity"], dtype=float)

  

    # --- Suavizado ---

    if smoothing_window >= len(y):

        smoothing_window = len(y) - 1 if len(y) % 2 == 0 else len(y)

    if smoothing_window % 2 == 0:

        smoothing_window += 1

    y_smooth = savgol_filter(y, window_length=smoothing_window, polyorder=polyorder)
```