---
title: "Parámetros vs Hiperparametros"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---

En Machine Learning, es fundamental entender la diferencia entre **parámetros** e **hiperparámetros**, ya que influyen directamente en el rendimiento del modelo.

---

## 🔹 1. Parámetros del Modelo  
Los **parámetros** son los valores internos que el modelo **aprende automáticamente** a partir de los datos durante el entrenamiento. Estos valores definen cómo el modelo hace predicciones y varían en cada ejecución.

### ✅ Características  
- **Se ajustan durante el entrenamiento** mediante algoritmos de optimización (Ej: Gradiente Descendiente).
- **Son aprendidos a partir de los datos** y dependen del conjunto de entrenamiento.

### 📌 Ejemplos:
- **Pesos ($w$) y sesgos $\b$** en redes neuronales o regresión lineal.
- **Coeficientes de un árbol de decisión** después de entrenarlo.
- **Centroides en K-Means** (posiciones finales después del ajuste).

---

## 🔹 2. Hiperparámetros  
Los **hiperparámetros** son valores **definidos por el usuario antes del entrenamiento** y afectan **cómo** el modelo aprende. No se ajustan automáticamente, sino que deben seleccionarse cuidadosamente para mejorar el desempeño del modelo.

### ✅ Características  
- **Se configuran antes de entrenar el modelo**.
- **No se aprenden automáticamente**; se ajustan mediante técnicas como *Grid Search* o *Random Search*.
- **Afectan el rendimiento y la capacidad de generalización**.

### 📌 Ejemplos:
- **Tasa de aprendizaje ($\alpha$)** en redes neuronales.
- **Número de árboles** en un *Random Forest*.
- **Número de vecinos** en *K-Nearest Neighbors (KNN)*.
- **Cantidad de capas y neuronas** en redes neuronales.
- **Parámetro de regularización ($\lambda$)** en regresión logística o SVM.

---

## 🔍 Comparación Rápida

| Característica        | Parámetros  | Hiperparámetros |
|----------------------|------------|----------------|
| **Definición**       | Se aprenden durante el entrenamiento | Se fijan antes del entrenamiento |
| **Ejemplos**         | Pesos en redes neuronales, coeficientes en regresión | Tasa de aprendizaje, número de capas en redes neuronales |
| **Ajuste**          | Automático (mediante optimización) | Manual o por búsqueda automatizada |
| **Impacto**         | Directo en la predicción | Directo en el desempeño del modelo |

---

## 🎯 ¿Cómo Ajustar los Hiperparámetros?
Para encontrar la mejor configuración, se pueden usar técnicas como:
- **Grid Search** → Prueba combinaciones de hiperparámetros de forma exhaustiva.
- **Random Search** → Selecciona valores aleatorios dentro de un rango definido.
- **Optimización Bayesiana** → Encuentra los mejores hiperparámetros usando modelos probabilísticos.

En *Python (Scikit-Learn)*, se puede usar `GridSearchCV` o `RandomizedSearchCV` para optimizar hiperparámetros de forma automática. 🚀

---

💡 **Conclusión**: Mientras que los **parámetros** son aprendidos automáticamente por el modelo, los **hiperparámetros** deben ser ajustados manualmente para mejorar el rendimiento. ¡Escogerlos correctamente puede marcar la diferencia en tu proyecto de Machine Learning! 🔥


[[Hyperparameter Tuning - Búsqueda de Hiperparametros]]
