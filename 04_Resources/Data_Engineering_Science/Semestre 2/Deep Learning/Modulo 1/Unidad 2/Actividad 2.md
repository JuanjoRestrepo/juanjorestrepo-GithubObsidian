---
title: "Actividad 2"
date: 2026-08-27
tags:
  - maestria
  - semestre-2
  - deep-learning
  - apuntes
status: reference
---


## Análisis del comportamiento de los algoritmos de optimización en Script1M1U2.ipynb

**Introducción:**

El presente análisis se centra en el comportamiento de tres algoritmos de optimización: Gradiente Descendente (GD), Gradiente Descendente con Momentum (GD_M) y ADAM, aplicados al entrenamiento de una red neuronal profunda en el script `Script1M1U2.ipynb`. El objetivo es identificar las ventajas y desventajas de cada algoritmo, comprender su impacto en la convergencia y precisión del modelo, y extraer conclusiones que guíen la selección del optimizador adecuado para diferentes escenarios.

**Gradiente Descendente (GD):**

GD es el algoritmo de optimización más básico, que actualiza los pesos del modelo en la dirección opuesta al gradiente de la función de costo. Si bien es simple de implementar y tiene un bajo costo computacional por iteración, su convergencia puede ser lenta, especialmente en funciones de costo complejas con numerosos mínimos locales. Además, GD es sensible a la tasa de aprendizaje, lo que requiere una cuidadosa sintonización para evitar oscilaciones o estancamiento en el proceso de optimización.

En el script `Script1M1U2.ipynb`, GD puede exhibir una convergencia más lenta en comparación con los otros optimizadores, particularmente si la función de costo presenta una topología compleja. Esto se debe a su incapacidad para "escapar" de mínimos locales y su dependencia de una tasa de aprendizaje constante.

**Gradiente Descendente con Momentum (GD_M):**

GD_M introduce el concepto de "momentum", que simula la inercia de una bola rodando por una colina. El momentum ayuda a acelerar la convergencia al acumular la información de las actualizaciones previas, permitiendo al algoritmo superar mínimos locales y avanzar más rápidamente hacia el mínimo global. Además, GD_M es menos sensible a la tasa de aprendizaje que GD, lo que facilita su ajuste.

En el script, GD_M debería mostrar una convergencia más rápida que GD y una mejor precisión en el conjunto de prueba. El momentum ayuda a acelerar el proceso de optimización y a evitar el estancamiento en mínimos locales, lo que conduce a un modelo más robusto y generalizable.

**ADAM (Adaptive Moment Estimation):**

ADAM es un algoritmo de optimización adaptativo que combina las ventajas del momentum con la adaptación de la tasa de aprendizaje para cada parámetro del modelo. Esto permite una convergencia rápida y un ajuste automático de la tasa de aprendizaje, lo que lo convierte en un optimizador robusto y eficiente para una amplia gama de problemas.

En el script `Script1M1U2.ipynb`, ADAM suele ser el optimizador con mejor rendimiento, logrando una convergencia rápida y una alta precisión en el conjunto de prueba. Su capacidad para adaptar la tasa de aprendizaje y su robustez lo hacen una opción ideal para problemas complejos con múltiples parámetros.

**Comparación de los optimizadores:**

|Optimizador|Velocidad de convergencia|Precisión|Robustez|Complejidad|
|---|---|---|---|---|
|GD|Lenta|Baja|Baja|Baja|
|GD_M|Media|Media|Media|Media|
|ADAM|Rápida|Alta|Alta|Alta|

**Conclusiones:**

La elección del optimizador adecuado depende del problema específico y de los requisitos de rendimiento. GD es una opción simple para problemas sencillos con funciones de costo convexas, mientras que GD_M ofrece una convergencia más rápida y una mayor robustez en escenarios más complejos. ADAM es el optimizador más avanzado, que combina las ventajas del momentum con la adaptación de la tasa de aprendizaje, lo que lo convierte en una opción ideal para problemas complejos con múltiples parámetros.

En el script `Script1M1U2.ipynb`, ADAM destaca por su rendimiento superior, logrando una convergencia rápida y una alta precisión en el conjunto de prueba. Sin embargo, es importante considerar la complejidad de su implementación y la necesidad de ajustar sus hiperparámetros.

**Recomendaciones:**

- Para problemas sencillos con funciones de costo convexas, GD puede ser una opción viable.
- Para problemas más complejos con mínimos locales, GD_M ofrece una convergencia más rápida y una mayor robustez.
- Para problemas de gran escala con múltiples parámetros, ADAM es el optimizador recomendado por su eficiencia y adaptabilidad.

En la práctica, es recomendable experimentar con diferentes optimizadores y ajustar sus hiperparámetros para encontrar la configuración óptima para cada problema específico.

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - Semestre 2]]
- **Dominio**: Master Data Science — Semestre 2
