
## 1) Chequeos inmediatos (hazlos ya)

1. Verifica que **imagen** y **máscara** correspondan exactamente (mismo patch, mismo nombre base).
2. Averigua si la máscara es:
    - _etiquetada en un solo canal (valores 0,1,2...)_ o
    - _RGB con paleta/colores indexados_ — esto determina cómo la conviertes a clases.
3. Extrae los valores únicos de la máscara y guarda el resultado (te dice qué clases hay).
4. Genera un CSV maestro con: `patch_filename, slide_id, patient_id, x_ini, y_ini, width, height, slide_label` — así tienes metadatos para todo.