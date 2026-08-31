---
title: "Notas libro Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow de Aurélien Géron"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---



# 🧠 Batch Normalization (BN)

## ¿Qué es?

Batch Normalization es una técnica introducida por Sergey Ioffe y Christian Szegedy en 2015 para mejorar la estabilidad y velocidad del entrenamiento de redes neuronales profundas. Consiste en normalizar las activaciones de cada capa utilizando la media y desviación estándar del mini-batch actual. [Medium](https://medium.com/%40ngneha090/batch-normalization-in-deep-learning-5f200f6f7733?utm_source=chatgpt.com)

## ¿Por qué es útil?

- **Reduce el _internal covariate shift_**: minimiza los cambios en la distribución de las activaciones internas durante el entrenamiento.
    
- **Acelera el entrenamiento**: permite usar tasas de aprendizaje más altas.
    
- **Actúa como regularizador**: reduce la necesidad de técnicas como Dropout.
    
- **Mejora la estabilidad**: mitiga problemas de gradientes que desaparecen o explotan.[GeeksforGeeks+1arXiv+1](https://www.geeksforgeeks.org/what-is-batch-normalization-in-deep-learning/?utm_source=chatgpt.com)
    

## ¿Cómo funciona?

Para cada mini-batch B={x1,x2,...,xm}B = \{x_1, x_2, ..., x_m\}B={x1​,x2​,...,xm​}, se realizan los siguientes pasos:

1. **Calcular la media del mini-batch**:
    
    μB=1m∑i=1mxi\mu_B = \frac{1}{m} \sum_{i=1}^{m} x_iμB​=m1​i=1∑m​xi​
2. **Calcular la varianza del mini-batch**:
    
    σB2=1m∑i=1m(xi−μB)2\sigma_B^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_B)^2σB2​=m1​i=1∑m​(xi​−μB​)2
3. **Normalizar**:
    
    x^i=xi−μBσB2+ϵ\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}x^i​=σB2​+ϵ​xi​−μB​​
    
    Donde ϵ\epsilonϵ es un pequeño valor para evitar divisiones por cero.
    
4. **Escalar y desplazar**:
    
    yi=γx^i+βy_i = \gamma \hat{x}_i + \betayi​=γx^i​+β
    
    Donde γ\gammaγ y β\betaβ son parámetros aprendibles que permiten al modelo restaurar la capacidad de representación si es necesario.
    

## ¿Dónde se aplica?

BN se puede aplicar antes o después de la función de activación en cada capa oculta. En muchos casos, si se añade una capa de BN como la primera capa de la red, no es necesario estandarizar el conjunto de entrenamiento previamente. La capa de BN se encargará de ello durante el entrenamiento.

## ¿Qué sucede durante la inferencia?

Durante la inferencia, no se utilizan las estadísticas del mini-batch actual. En su lugar, se emplean las medias y varianzas acumuladas durante el entrenamiento para normalizar las activaciones. Esto asegura que las predicciones sean determinísticas y consistentes.

## Beneficios adicionales

- **Permite redes más profundas**: facilita el entrenamiento de redes con muchas capas.
    
- **Reduce la sensibilidad a la inicialización**: el modelo es menos dependiente de la inicialización de pesos.
    
- **Mejora la generalización**: actúa como una forma de regularización, ayudando a prevenir el sobreajuste.[Dive into Deep Learning](https://d2l.ai/chapter_convolutional-modern/batch-norm.html?utm_source=chatgpt.com)
