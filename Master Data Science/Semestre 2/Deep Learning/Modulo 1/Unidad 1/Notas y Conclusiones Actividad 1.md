---
title: "Notas y Conclusiones Actividad 1"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---


[Open Colab Script2M1U1](https://colab.research.google.com/drive/1Ss1oKEWPTyXMb-ck3nt9qXzXaEghmqRf#scrollTo=lbFjnVac01qz)
[GitHub Script2M1U1](https://github.com/JuanjoRestrepo/Master-Data-Science/blob/main/Semestre%202/Deep%20Learning/Modulo%201/Unidad%201/Actividad%201/Script2M1U1.ipynb)

# 🧪 Evaluación de Tasas de Aprendizaje en Red Neuronal con Keras

---

## 🎯 Objetivo

Evaluar el impacto de diferentes tasas de aprendizaje (`learning rate`) sobre el desempeño de una red neuronal multicapa optimizada mediante búsqueda aleatoria de hiperparámetros. El análisis considera métricas de precisión (`accuracy`), comportamiento de la función de pérdida (`loss`) y estabilidad del entrenamiento en cada escenario.

---

## ⚙️ Hiperparámetros Óptimos Seleccionados

Los siguientes hiperparámetros fueron seleccionados tras ejecutar una búsqueda aleatoria con `RandomizedSearchCV`:

- **Arquitectura de la red**:
    - Capa 1: `256 neuronas`
    - Capa 2: `128 neuronas`
    - Capa 3: `64 neuronas`
- **Función de activación**: `ReLU`
- **Dropout**: `0.3`
- **Épocas**: `40`
- **Accuracy**: `0.8106`

**Observación**:  
La configuración combina profundidad para modelar relaciones complejas y regularización moderada (_dropout_) para evitar sobreajuste.

---

## 📊 Comparación del Rendimiento por Learning Rate

|**Learning Rate**|**Test Accuracy**|**Observación**|
|---|---|---|
|0.0001|0.6392|Convergencia lenta. Mejora constante pero no alcanza alta precisión.|
|0.01|0.8222|**Mejor desempeño**. Equilibrio entre estabilidad y velocidad de convergencia.|
|0.1|0.2800|Red inestable. Pérdida cae abruptamente sin aprendizaje efectivo.|
|1.0|0.1000|Explosión del gradiente. Modelo diverge.|
|10.0|0.1000|Comportamiento errático. Colapso total desde el inicio.|

> ✅ Se concluye que `0.01` es el valor óptimo para esta arquitectura, maximizando la precisión y manteniendo un entrenamiento estable.


**Conclusión clave**:  
El _learning rate_ de **0.01** maximiza la precisión sin comprometer estabilidad.



---

## 📈 Análisis Visual del Comportamiento por *LR*

### 🟦 **Learning Rate = 0.0001**

- **Accuracy**: Progresión lenta pero consistente. Validación supera entrenamiento (posible convergencia parcial).
- **Loss**: Disminución continua y estable.
- **Conclusión**: Aprendizaje seguro pero insuficiente. Ideal para entrenamientos largos.

### 🟩 **Learning Rate = 0.01**

- **Accuracy**: Mejora rápida en entrenamiento y validación. Curvas paralelas y suaves.
- **Loss**: Disminución estable sin sobreajuste.
- **Conclusión**: Parámetro óptimo. Balance ideal.

### 🟥 **Learning Rate = 0.1**

- **Accuracy**: Estancamiento en 28% (sin aprendizaje).
- **Loss**: Caída abrupta seguida de estancamiento.
- **Conclusión**: _Learning rate_ puede ser un poco alto.

### 🟧 **Learning Rate = 1.0**

- **Accuracy**: Oscilaciones erráticas. Accuracy bajo, con valor del 10%.
- **Loss**: Explosión inicial y colapso.
- **Conclusión**: Explosión del gradiente.

### 🟨 **Learning Rate = 10.0**

- **Accuracy**: 10% (equivalente a predicción aleatoria).
- **Loss**: Valores extremos sin recuperación.
- **Conclusión**: Inutilizable.

---

## 🧠 Síntesis Final

- **Hiperparámetro crítico**: _Learning rate_ (determina éxito/fracaso del entrenamiento).
- **Configuración óptima**:
    - LR = 0.01
    - Arquitectura de la Red: 256 → 128 → 64 + ReLU
    - Dropout = 0.3
- **Generalización**: La configuración es óptima, gracias a que existe una regularización y profundidad equilibrada.

> La mejor precisión en el conjunto de prueba se alcanzó con `learning_rate = 0.01`, con un valor de **82.22%**.


---
## 💡 Recomendaciones

- Incluir técnicas de **decaimiento del learning rate** (`ReduceLROnPlateau`, `ExponentialDecay`) para automatizar la adaptación durante el entrenamiento.
- Incorporar **batch normalization** para mejorar la estabilidad ante tasas altas.
- Explorar optimizadores más avanzados (`AdamW`, `RMSprop`, `Lookahead`) y comparar su desempeño.
