
# 1. Introducción

- **Contexto general**: explica el reto del diagnóstico asistido por IA en histopatología, la importancia de modelos que trabajen con imágenes (WSI) donde solo se etiquetan a nivel _bag_ (p. ej., Slide-level), no por instancia.
    
- **Brecha/Problema**: detalla cómo los métodos actuales requieren anotaciones de nivel instancia o no escalan bien; MIL permite operar con supervisión débil.
    
- **Relevancia clínica**: conecta la decisión diagnóstica de cáncer de colon con microsatellite instability, pronóstico o subtipos moleculares.
    
- **Aporte de tu trabajo**:
    
    1. Validar MIL sobre datos de cáncer de colon (imagen/patrón estructural).
        
    2. Diseñar una arquitectura modular y extensible.
        
    3. Combinar experimentación sintética y real, justificando desde analítica de datos.
        

Cita reciente: atención para CRC usando MIL con enfoques de atención, PCA y priors clínicos
[Multiple Clustered Instance Learning for Histopathology Cancer Image Classification, Segmentation and Clustering](https://www.researchgate.net/publication/255564140_Multiple_Clustered_Instance_Learning_for_Histopathology_Cancer_Image_Classification_Segmentation_and_Clustering?utm_source=chatgpt.com)
[MUNI+1arXiv+1](https://is.muni.cz/th/uh3nv/thesis.pdf?utm_source=chatgpt.com)
[arXiv](https://arxiv.org/abs/2401.16131?utm_source=chatgpt.com).

---

# 2. Descripción del problema

## 2.1 Planteamiento del problema

- **Dataset**: detalle de imágenes histopatológicas (colon), formateados en _bags_ de parches sin etiquetas instancia.
    
- **Problema técnico**: aprender una función que prediga la etiqueta del _bag_ (ej. tumor positivo/negativo), aunque las instancias no estén etiquetadas.
    
- **Formulación MIL**: explica la asunción estándar de MIL (positividad si al menos una instancia es positiva) vs otras variantes (colectiva, contada)[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9825360/?utm_source=chatgpt.com).
    
- **Caso de aplicación**: clasificar imágenes de colon cancer—evaluar variantes como atención, graph-based MIL (p. ej. MicroMIL) para capturar heterogeneidad[arXiv](https://arxiv.org/abs/2407.21604?utm_source=chatgpt.com).
    

---

# 3. Justificación

- **Técnica**: MIL es adecuado cuando no se cuenta con anotaciones a nivel instancia, común en datasets biomédicos.
    
- **Aplicativa**: permite acelerar diagnósticos automatizados, evitando tarea intensiva de etiquetado manual.
    
- **Innovación**:
    
    - Uso de estrategias como agrupar patches en grafos (_graph-based MIL_, MicroMIL) o fusión clínica-artificial (CIMIL‑CRC)[arXiv](https://arxiv.org/abs/2401.16131?utm_source=chatgpt.com).
        
    - Arquitectura modular que permita pruebas sobre múltiples datasets (cáncer vs EEG).
        

---

# 4. Objetivos

## 4.1 Objetivo general

Desarrollar, implementar y evaluar una solución de _Multiple Instance Learning_ en imágenes histopatológicas de cáncer de colon, utilizando supervisión débil para clasificar _bags_ con alta precisión, bajo una arquitectura modular y escalable.

## 4.2 Objetivos específicos

- Realizar experimentos sintéticos controlados que validen internamente la arquitectura propuesta.
    
- Seleccionar y preparar dataset real de cáncer de colon, representado como bag de parches, con anotación Slide-level.
    
- Implementar enfoques MIL: atención, graph‑based (p. ej. MicroMIL) o PCA + priors clínicos (CIMIL‑CRC).
    
- Comparar desempeño usando métricas estándar (AUC, precisión, recall) mediante validación cruzada.
    
- Documentar el pipeline desde la preparación de datos hasta la evaluación, justificando cada paso metodológico según buenas prácticas (exploración, imputación, balanceo, etc.).