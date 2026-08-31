
## 1) Chequeos inmediatos (hazlos ya)

1. Verifica que **imagen** y **máscara** correspondan exactamente (mismo patch, mismo nombre base).
2. Averigua si la máscara es:
    - _etiquetada en un solo canal (valores 0,1,2...)_ o
    - _RGB con paleta/colores indexados_ — esto determina cómo la conviertes a clases.
3. Extrae los valores únicos de la máscara y guarda el resultado (te dice qué clases hay).
4. Genera un CSV maestro con: `patch_filename, slide_id, patient_id, x_ini, y_ini, width, height, slide_label` — así tienes metadatos para todo.


---

## 1) Qué significan las líneas principales de salida

- `Labels loaded: 155 slides`  
    Se cargó el Excel `wsi_labels.xlsx` y contiene 155 filas (una por WSI). Eso te da el `slide_id → patient_id, Gleason_primary, Gleason_secondary`.
    
- `Total image files: 18783`  
    Hay **18.783 parches** en la carpeta `images` (coincide con las estadísticas SICAPv2 que mencionabas: ~18.783 parches).
    
- `scanning images: 100% ...`  
    El script inspeccionó todos los parches y máscaras (acciones: comprobó tamaño, si hay tejido, si existe máscara, extrajo modo y valores únicos).
    
- `Manifest saved to /content/dataset_manifest.csv`  
    Se creó `dataset_manifest.csv` con una fila por parche e información clave (nombre de archivo, slide_id, coordenadas, tamaño, si contiene tejido, si la máscara existe, modo de la máscara, resumen de valores en la máscara, Gleason del slide).
    
- `Mask palettes summary saved to /content/mask_palettes_summary.json`  
    JSON con resúmenes (paletas o valores únicos) de las máscaras para inspección posterior.
    
- `Missing masks: 0 / 18783`  
    Todas las imágenes tienen su correspondiente máscara — buen dato (no hay pares imagen/máscara faltantes).

# Manifest.csv

Muestra del `manifest` (columnas importantes):

- `patch_filename`, `mask_filename`: nombres de fichero.
    
- `slide_id`, `patient_id`: metadatos por WSI.
    
- `x_ini`, `y_ini`, `width`, `height`: coordenadas y tamaño del parche.
    
- `has_tissue`: indicador simple (True/False) si el parche contiene tejido según heurística HSV.
    
- `mask_mode`: modo de la imagen de la máscara (p.ej. `L`, `P`, `RGB`).
    
- `mask_summary`: JSON con `unique_values` o `palette` de la máscara.
    
- `Gleason_primary`, `Gleason_secondary`: etiquetas a nivel de WSI tomadas del Excel.

## Masks

`Unique mask modes in dataset: ['L']`  
Todas las máscaras están en modo `L` (escala de grises / un solo canal).  
Eso implica que las máscaras **son imágenes con valores enteros por píxel** (p. ej. 0, 3, 4, 5) y **no** vienen como mapa de colores indexado (`P`) o RGB.  
En tu caso, `mask_summary` mostró `{"unique_values": [0, 3, 4, 5]}`, así que **las máscaras usan los valores 0, 3, 4 y 5** para codificar clases.


`Count patches with tissue: 18783`  
La heurística de detección de tejido consideró que todos los parches tienen tejido (puede ocurrir, según cómo generaron los parches en SICAPv2).


---
# Mapeo de las clases

## 2) Interpretación de `unique_values = [0,3,4,5]`

- `0` casi siempre representa **fondo/no-tejido** (espacios en blanco, background).
    
- Los valores `3, 4, 5` probablemente son **clases anotadas** — en SICAPv2 suelen codificar distintos grados o tipos (por ejemplo: Gleason 3, Gleason 4, Gleason 5 o subclases).  
    **Importante**: NO asumas mapeo exacto sin confirmar con la documentación oficial del dataset o el README de SICAPv2. El mapeo (qué número = qué etiqueta) suele estar en la página del dataset o en los metadatos. Revisa `SICAPv2` README o `mask_palettes_summary.json`.


---

5) ¿Qué hago ahora por ti?

Puedo:

(1) Generarte la celda B completa para Colab que extrae embeddings con ResNet-50 (preprocesado correcto, batch, guardado en HDF5 por slide o por parche).

(2) Generarte la celda para construir bag_manifest.csv (slide-level labels) y splits por paciente (train/val/test estratificados).

(3) Generarte la celda para entrenar ABMIL (Ilse et al.) usando los embeddings guardados (loop de entrenamiento + cálculo de AUC/F1 + checkpointing).

Mi recomendación práctica: Primero B (embeddings) y a continuación (2) splits. ¿Te genero ya la celda B lista para pegar en Colab?

---

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - Master Data Science]]
- **Dominio**: Master Data Science
