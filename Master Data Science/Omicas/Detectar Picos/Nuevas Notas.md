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



