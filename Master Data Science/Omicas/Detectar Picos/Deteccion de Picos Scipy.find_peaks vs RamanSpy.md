
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



### 1. A partir del archivo que tienes, los bloques clave son:

- **Lectura y normalización de columnas**
    - *Código*: `df = pd.DataFrame(data)` + renombrado `shift_cm1` → `shift_cm-1`.
    - *Objetivo*: garantizar que `x` y `y` existan.

- **Suavizado (Savitzky–Golay)**
	- *Código*: `y_sg = savgol_filter(y, smoothing_window, polyorder)` (o su manejo si `smoothing_window` inválido).
	- *Técnica*: filtro de polinomio local que preserva forma de picos mejor que un simple promedio.
	- *Parámetro importante*: `smoothing_window` (debe ser impar) y `polyorder`.

- **Baseline (ALS implementado localmente)**
	- *Código*: `baseline = baseline_als(y_sg, lam=baseline_lam, p=baseline_p, niter=10)` (función `baseline_als` en tu archivo).
	- *Técnica*: ALS — resuelve un sistema lineal penalizando la curvatura del baseline; robusto para espectros químicos. Parámetros `lam` (fuerza de suavizado) y `p` (asimetría: cuánto penaliza puntos por encima vs debajo).

- **Señal corregida y shift positivo**
	- *Código*: `y_corr = y_sg - baseline` y `y_corr_shift = y_corr - np.nanmin(y_corr)` si hay negativos.
	- *Motivo*: muchos detectores (y definiciones de prominencia) asumen señales no-negativas.

- **Detección de picos (Scipy)**
	- *Código*: `peaks_idx, props = find_peaks(y_corr_shift, prominence=prominence, distance=distance, height=height, **find_peaks_kwargs)`
	- *Algoritmo*: `find_peaks` usa criterios locales sobre amplitud/vecindad; `prominence` mide cuánto sobresale un pico respecto a sus valles vecinos (más robusto que altura bruta).
	- *Parámetros críticos*:
	    - `prominence`: umbral relativo al ruido. En tu código se calcula por defecto como `max(np.nanstd(y_corr_shift)*3, 1e-9)` o variantes.
	    - `distance`: separación mínima en puntos entre picos.
	    - `height`: altura mínima absoluta opcional.

- **Refinamiento del ápice**
    - Código: `parabolic_interpolation(x, y_corr_shift, idx)` — devuelve apex sub-muestra (x_apex, y_apex).
    - Técnica: ajuste parabólico con el punto y sus vecinos para desplazar el pico a una posición más precisa entre muestras discretas.

- **Cálculo centroid/área**
    - Código: `peak_centroid_area` usa `np.trapz` (integración numérica) sobre la ventana de base izquierda/derecha.
    - Técnica: área bajo la curva y centro de masa dentro de la base del pico.

- **FWHM estimado**
    - Código: `fwhm_from_peak` estimación por recorrido hasta la mitad del máximo y linear interpolation para obtener posición de media altura.

- **Resultado**
    - DataFrame con: `shift_cm-1` (apex sub-muestra), `intensity` (apex refinado), `centroid`, `area`, `fwhm`, `raw_index`, `left_base_idx`, `right_base_idx`.



```python
  

```