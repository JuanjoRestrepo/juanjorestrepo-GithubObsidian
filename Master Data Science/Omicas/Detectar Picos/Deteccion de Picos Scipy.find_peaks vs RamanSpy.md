
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



```python
  

```