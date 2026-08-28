---
title: "Ordenar y Limpiar Datos"
date: 2026-08-27
tags:
  - maestria
  - semestre-1
  - estadistica
  - apuntes
status: reference
---

## Datos faltantes y trazabilidad

Los datos faltantes pueden tener un significado propio y no deben ser imputados ni eliminados de forma automática. Para cada variable $j$ y observación $i$, se debe distinguir el valor observado $x_{ij}$ de su indicador de ausencia:

$$
m_{ij} =
\begin{cases}
1, & \text{si } x_{ij} \text{ es faltante}, \\
0, & \text{si } x_{ij} \text{ está observado}.
\end{cases}
$$

El patrón $m_{ij}$ puede ser informativo; por tanto, una categoría explícita de “faltante” o una variable indicadora puede conservar señal predictiva. La estrategia de imputación debe justificarse según el mecanismo de ausencia: MCAR, MAR o MNAR.

## Conexiones transversales

- La exploración previa de distribuciones y valores atípicos se desarrolla en [[Análisis Exploratorio de Datos]].
- Esta etapa es el prerrequisito de [[Master Data Science/Semestre 2/400ITA010 - Métodos de Aprendizaje Automático/Módulo 1 - Ciclo de construcción de un sistema de aprendizaje automático/Unidad 2 Preparacion de los datos/0.Conceptos básicos - Preparación de los datos|Preparación de los datos para aprendizaje automático]].

## Referencias verificadas

- [[Master Data Science/Bibliografía Curada y Actualización 2026|Bibliografía curada]]: NIST/SEMATECH para evaluación de calidad y supuestos estadísticos.
- [Transformaciones de datos — scikit-learn](https://scikit-learn.org/stable/data_transforms.html): ajustar imputadores, escaladores y codificadores únicamente con el conjunto de entrenamiento; después aplicar la transformación aprendida a validación y prueba para evitar fuga de información.
