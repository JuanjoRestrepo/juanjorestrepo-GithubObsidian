
## 📌 Concepto Clave
El **Aprendizaje de Variedades** es una técnica de reducción de dimensionalidad no lineal que asume que los datos de alta dimensión residen en una variedad (_manifold_) de menor dimensión incrustada en el espacio original. El objetivo es descubrir y mapear esta estructura subyacente para facilitar la visualización y el análisis. [Scikit-learn](https://scikit-learn.org/stable/modules/manifold.html?utm_source=chatgpt.com)​

## 🧭 Motivación
- Los conjuntos de datos de alta dimensión suelen ser difíciles de visualizar y analizar.
- Se busca una representación de menor dimensión que preserve las relaciones y estructuras importantes de los datos originales.
---

## 🔍 Métodos Principales

### 1. Isomap

<div align="center" style="margin: 20px 0;">
  <img src="Pasted%20image%2020250412180453.png" 
       alt="Arquitectura Isomap"
       style="max-width: 800px; border-radius: 8px; border: 1px solid #f0f0f0;">
</div>
Isomap extiende el escalado multidimensional (MDS) al preservar las distancias geodésicas entre todos los puntos, proporcionando una representación de menor dimensión que mantiene la estructura global de los datos. ​[Scikit-learn](https://scikit-learn.org/stable/auto_examples/manifold/plot_compare_methods.html?utm_source=chatgpt.com)

- **Mecanismo**: Combina escalado multidimensional (MDS) con distancias geodésicas
- **Ventaja**: Preserva estructura global
- **Ecuación clave**:  
  $d_G(x_i, x_j) = sumaDeAristasEnElCaminoMasCorto$

### 2. Locally Linear Embedding (LLE)

<div align="center" style="margin: 20px 0;">
  <img src="Pasted%20image%2020250412180514.png" 
       alt="Esquema LLE"
       style="max-width: 800px; border-radius: 8px; border: 1px solid #f0f0f0;">
</div>

LLE busca preservar las relaciones locales entre puntos cercanos, realizando una serie de análisis de componentes principales locales que se combinan para encontrar una incrustación no lineal. ​

- **Mecanismo**: Preserva relaciones locales mediante PCA local
- **Fórmula de reconstrucción**:  
  $min_W suma_i ||x_i - suma_j W_ij x_j||^2$

### 3. Modified LLE (MLLE)

MLLE aborda problemas de regularización en LLE utilizando múltiples vectores de peso en cada vecindario, mejorando la representación de la geometría subyacente de la variedad. ​

### 4. Hessian Eigenmapping (HLLE)

HLLE utiliza una forma cuadrática basada en el hessiano en cada vecindario para recuperar la estructura lineal local, siendo eficaz en la preservación de la geometría local. ​

### 5. Spectral Embedding (Laplacian Eigenmaps)

Este método utiliza una descomposición espectral del laplaciano del grafo generado por los datos para encontrar una representación de menor dimensión, preservando las distancias locales. ​[Scikit-learn](https://scikit-learn.org/stable/modules/manifold.html?utm_source=chatgpt.com)

### 6. Local Tangent Space Alignment (LTSA)

LTSA caracteriza la geometría local en cada vecindario mediante su espacio tangente y realiza una optimización global para alinear estos espacios tangentes, aprendiendo la incrustación. ​

### 7. Multi-dimensional Scaling (MDS)

MDS busca una representación de menor dimensión donde las distancias respeten las distancias en el espacio original de alta dimensión, modelando similitudes o disimilitudes como distancias en un espacio geométrico. ​

### 8. t-distributed Stochastic Neighbor Embedding (t-SNE)

t-SNE convierte afinidades entre puntos de datos en probabilidades conjuntas y minimiza la divergencia de Kullback-Leibler entre las distribuciones en los espacios original y de incrustación, siendo especialmente sensible a la estructura local. ​

- **Mecanismo**: Minimiza divergencia Kullback-Leibler entre distribuciones de probabilidad
- **Ventaja**: Excelente para visualizar clusters
- **Función de costo**:  
  $KL(P||Q) = suma_i suma_j p_ij log(p_ij / q_ij)$

---

## 🖼️ Visualizaciones

A continuación, se presentan visualizaciones de diferentes métodos de aprendizaje de variedades aplicados a un conjunto de datos de ejemplo:​

### Isomap

<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_005.png" alt="Isomap Embedding" width="600">
</div>​
### Locally Linear Embedding (LLE)


<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_006.png" alt="LLE Embedding" width="600">
</div>​
### Modified LLE (MLLE)

<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_007.png" alt="Modified LLE Embedding" width="600">​
</div>

### Hessian Eigenmapping (HLLE)

<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_008.png" alt="Hessian LLE Embedding" width="600">​
</div>

### Spectral Embedding

<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_009.png" alt="Spectral Embedding" width="600">
</div>​
### t-SNE

<div align="center">
<img src="https://scikit-learn.org/stable/_images/sphx_glr_plot_lle_digits_013.png" alt="t-SNE Embedding" width="600">
</div>​

---

## 📚 Referencias

- [Scikit-learn: Manifold Learning](https://scikit-learn.org/stable/modules/manifold.html)
- [Implementación de Manifold Learning con Python](https://github.com/scikit-learn/scikit-learn/tree/main/sklearn/manifold)
- [Libro: "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"](https://github.com/yanshengjia/ml-road/blob/master/resources/Hands%20On%20Machine%20Learning%20with%20Scikit%20Learn%20and%20TensorFlow.pdf)


