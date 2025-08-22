# 📊 Comparación de Picos Raman (Excel vs Detectores)

### Dataset analizado: `WE-PI-China-4-sensor 2.json`

|**Excel (Ground Truth)**|**Detectado (inspect_peaks / inspect_peaks_rsp)**|**Δ shift_cm-1**|**Δ intensidad**|
|---|---|---|---|
|1350 , 101|1349.22 , 95.11|-0.78|-5.89|
|1580 , 186|1581.10 , 175.60|+1.10|-10.40|
|2690 , 123|2693.68 , 107.79|+3.68|-15.21|

---

### ✅ Observaciones

- Los **tres picos coinciden en localización** (desviación < 4 cm⁻¹, dentro de lo aceptable en espectros Raman).
    
- La **intensidad detectada es menor** que la reportada en Excel (entre -6 y -15 unidades), probablemente por diferencias en normalización o suavizado.
    
- Ambos métodos (`inspect_peaks` y `inspect_peaks_rsp`) devolvieron **exactamente los mismos resultados** para este archivo → no hay ventaja del refinamiento en este caso.



![[Pasted image 20250821225829.png]]