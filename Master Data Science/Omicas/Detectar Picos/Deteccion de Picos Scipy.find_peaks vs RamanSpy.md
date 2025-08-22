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

airflow@b5fdfb5d9e4e:/opt/airflow/project$ python test_inspect_peaks.py 🔹 13. Procesando: WE-PI-China-4-sensor 2.json Saved plot to: /opt/airflow/project/logs/inspect_peaks_WE-PI-China-4-sensor_2.png ✅ Número de picos detectados: 3 📊 Ruta del plot generado: /opt/airflow/project/logs/inspect_peaks_WE-PI-China-4-sensor_2.png shift_cm-1 intensity centroid area fwhm raw_index left_base_idx right_base_idx 0 1349.224006 95.113307 997.440077 13349.459654 47.038644 1296 257 1392 1 1581.098078 175.604053 1585.469210 9234.143066 39.438504 1536 1392 1640 2 2693.678212 107.789200 2527.380726 17054.023837 62.936478 2690 1640 3077 



Comparado con el 

airflow@b5fdfb5d9e4e:/opt/airflow/project$ python ETL/Silver/show_peaks.py 

=== Picos detectados === 
🔹 inspect_peaks:
shift_cm-1 intensity 
1349.224006 95.113307 
1581.098078 175.604053 
2693.678212 107.789200 

🔹 inspect_peaks_rsp:
shift_cm-1 intensity 
1349.224006 95.113307 
1581.098078 175.604053 
2693.678212 107.789200