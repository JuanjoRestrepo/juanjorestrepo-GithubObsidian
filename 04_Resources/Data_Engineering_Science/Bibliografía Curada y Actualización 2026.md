---
title: "Bibliografía Curada y Actualización 2026"
date: 2026-08-27
tags:
  - maestria
  - bibliografia
  - ciencia-de-datos
  - referencias
status: reference
---

# Bibliografía Curada y Actualización 2026

[[Master Data Science/MOC - Master Data Science|← MOC Maestro]]

Esta bibliografía prioriza tres clases de evidencia: documentación mantenida por los proyectos que implementan los métodos, libros de editoriales académicas y artículos originales o revisiones sometidas a revisión por pares. No se usa como sustituto de la lectura crítica de cada nota; indica qué fuente consultar según el nivel de profundidad requerido.

## Estadística, EDA e inferencia

- [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/) — referencia pública institucional para métodos estadísticos, diseño experimental, análisis exploratorio y validación de supuestos.
- [An Introduction to Statistical Learning with Python (ISLP)](https://www.statlearning.com/) — edición publicada en 2023; texto de entrada con laboratorios reproducibles y cobertura de aprendizaje estadístico, SVM, deep learning y métodos no supervisados.
- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) — referencia avanzada de Hastie, Tibshirani y Friedman para fundamentos estadísticos de modelos predictivos.

## Preparación de datos y aprendizaje automático clásico

- [Transformaciones de datos — scikit-learn](https://scikit-learn.org/stable/data_transforms.html) — documentación vigente sobre ajuste y aplicación de transformadores, imputación, escalamiento, codificación y pipelines.
- [Guía de SVM — scikit-learn](https://scikit-learn.org/stable/modules/svm.html) — formulación, kernels, complejidad y recomendaciones prácticas de un proyecto mantenido por la comunidad científica.
- [Reducción de dimensión no supervisada — scikit-learn](https://scikit-learn.org/stable/modules/unsupervised_reduction.html) — guía de PCA y su composición con estimadores supervisados.
- [Principal Component Analysis — Jolliffe](https://link.springer.com/book/10.1007/b98835) — monografía de referencia para el tratamiento matemático y estadístico del PCA.
- [Principal component analysis: a review and recent developments — Jolliffe y Cadima](https://royalsocietypublishing.org/doi/10.1098/rsta.2015.0202) — revisión académica sobre propiedades, extensiones y límites interpretativos de PCA.

## Aprendizaje profundo

- [Deep Learning — Goodfellow, Bengio y Courville](https://www.deeplearningbook.org/) — texto de referencia para propagación hacia atrás, regularización, optimización, CNN y modelos secuenciales.
- [Dropout: A Simple Way to Prevent Neural Networks from Overfitting — JMLR](https://jmlr.org/papers/v15/srivastava14a.html) — artículo original para el fundamento del dropout.
- [Regularizadores de capas — Keras 3](https://keras.io/api/layers/regularizers/) — especificación vigente de penalizaciones $L_1$, $L_2$ y actividad.
- [Dropout — Keras 3](https://keras.io/api/layers/regularization_layers/dropout/) — comportamiento de entrenamiento e inferencia de la capa.
- [EarlyStopping — Keras 3](https://keras.io/api/callbacks/early_stopping/) — contrato actual del callback, monitorización y restauración de pesos.
- [Capas convolucionales — Keras 3](https://keras.io/api/layers/convolution_layers/) y [capas recurrentes — Keras 3](https://keras.io/api/layers/recurrent_layers/) — APIs oficiales para Conv1D/2D/3D, SimpleRNN, GRU y LSTM.

## Regla de uso en las notas

1. Utilizar libros y artículos para definiciones, supuestos, demostraciones y límites de validez.
2. Utilizar documentación oficial para comportamiento de librerías y recomendaciones operativas que pueden cambiar por versión.
3. Registrar la fuente junto a la afirmación técnica; evitar convertir una API concreta en una afirmación matemática general.
4. Antes de usar una transformación, imputación, PCA o selección de hiperparámetros, separar entrenamiento, validación y prueba para evitar fuga de información.

