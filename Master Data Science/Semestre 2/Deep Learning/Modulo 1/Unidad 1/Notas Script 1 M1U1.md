---
title: "Notas Script 1 M1U1"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---

tags: #DeepLearning #Master #Maestria #Semestre2 
# Notas Programa Ejemplo para Realizar Aprendizaje Supervisado utilizando aprendizaje profundo


[Open Colab Script1M1U1](https://colab.research.google.com/drive/1prdt5lVCpJZ-SRZHsJPP3nkjr4khIjAd#scrollTo=75rNkwWWigTj)
## Dense Layer: Inputs, Units, and Parameters

### 1. Number of Inputs:

- **First Layer:** Determined by the **dimensionality of your input data**.
    - Example: In MNIST, flattened 28x28 images result in 784 input features.
- **Subsequent Layers:** Equal to the **number of units (outputs) in the previous layer**.
    - Example: If the previous layer has 1024 units, the current layer has 1024 inputs.

### 2. Number of Units:

- **Hyperparameter:** A value you **choose** based on:
    - **Problem complexity:** More complex problems may need more units.
    - **Data size:** More data allows for larger networks without overfitting.
    - **Computational resources:** More units require more processing power.
- **Experimentation:** Trial and error helps find the optimal number. Start with reasonable values and adjust based on model performance.

### 3. Parameters:

- **Calculated, not chosen:** Determined by the **number of inputs** and **units**.
- **Formula:**

content_copy 

```
Parameters = (Number of inputs + 1) * Number of units
```

- **Significance:** Represents the **learnable weights and biases** within the layer.
    - **Weights:** Control connections between neurons in different layers.
    - **Biases:** Act as offsets for each neuron's activation.

**Example (MNIST):**

| Layer           | Number of Inputs            | Number of Units    | Parameters                 |
| --------------- | --------------------------- | ------------------ | -------------------------- |
| First (Hidden)  | 784 (from flattened images) | 1024 (chosen)      | (784 + 1) * 1024 = 803,840 |
| Second (Hidden) | 1024 (from previous layer)  | 512 (chosen)       | (1024 + 1) * 512 = 524,800 |
| Third (Output)  | 512 (from previous layer)   | 10 (for 10 digits) | (512 + 1) * 10 = 5,130     |

## Model Summary: "sequential"

| Layer (type)    | Output Shape | Param # |
| --------------- | ------------ | ------- |
| dense (Dense)   | (None, 1024) | 803,840 |
| dense_1 (Dense) | (None, 512)  | 524,800 |
| dense_2 (Dense) | (None, 10)   | 5,130   |
**Total params:** 1,333,770 (5.09 MB)  
**Trainable params:** 1,333,770 (5.09 MB)  
**Non-trainable params:** 0 (0.00 B)

**Explanation of Columns:**

- **Layer (type):** The type of layer (e.g., Dense, Convolutional) and its name.
- **Output Shape:** The shape of the output tensor produced by the layer. `(None, 1024)` means the output is a 2D tensor where the first dimension (batch size) is flexible (`None`) and the second dimension has 1024 elements.
- **Param #:** The number of trainable parameters (weights and biases) in the layer.



# Reflexiones Finales 🧠📊

## 🏆 Logros Clave
> [!SUCCESS] Éxito en Clasificación
> - **Precisión alcanzada**: $\boxed{97.78\%}$ en conjunto de prueba *(meta superada: +7.78%)*  
> - **Arquitectura efectiva**:
> ```python
> Modelo = [
>   CapaDensa(128, activación='relu'),
>   Dropout(0.3),
>   CapaDensa(64, activación='relu'),
>   CapaSalida(10, activación='softmax')
> ]
> ```
> - Técnicas clave: `ReLU` · `Dropout` · `Adam Optimizer`

---

## 💭 Reflexiones Técnicas
1. **Principio de Manifold Learning**  
   La reducción gradual de dimensionalidad (`784 → 128 → 64 → 10`) refleja cómo las redes capturan progresivamente características jerárquicas. [Documentación Manifold Learning](https://scikit-learn.org/stable/modules/manifold.html) y [[🧠 Principio de Manifold Learning]]

3. **Estabilidad del Entrenamiento**  
   - Curvas de aprendizaje convergentes  
   - Pérdida de validación < entrenamiento → *Posible efecto de regularización*

3. **Sobreajuste Controlado**  
   El Dropout (30%) demostró ser efectivo para:
   - Reducir co-adaptación de neuronas  
   - Mejorar generalización

---

## ❓ Preguntas Abiertas
> [!QUESTION]- Regularización Avanzada  
> ¿Cómo compararían técnicas como:  
> - **Batch Normalization**  
> - **L2/L1 Regularization**  
> - **Early Stopping**  
> en este contexto?

> [!QUESTION]- Escalabilidad a Imágenes Complejas  
> ¿Qué modificaciones requeriría para:  
> - **Imágenes RGB** (3 canales)  
> - **Objetos no centrados**  
> - **Fondos variables**?

---

## 💡 Comentarios y Conclusiones
```dataview
LIST "¡Las redes neuronales son máquinas de aprendizaje topológico!"
WHERE contains(file.name, "Reflexiones")


|                            🔙 Volver a                            |             Seguir a ⏭️              |
| :---------------------------------------------------------------: | :----------------------------------: |
| [[1. Unidad 1 Componentes fundamentales de las redes neuronales]] | [[Notas y Conclusiones Actividad 1]] |
