
# 🧠 ¿Qué es Multiple Instance Learning (MIL)?
- **MIL** es un enfoque de _aprendizaje supervisado débilmente etiquetado_ donde **las etiquetas se asignan a conjuntos (bags)** en vez de a instancias individuales
- Bajo el **supuesto estándar**:
	- Un _bag negativo_ contiene únicamente instancias negativas
	- Un _bag positivo_ contiene al menos una instancia positiva

---
# Terminología
- **Instancia**: elemento individual (imagen, fragmento de texto, conformación molecular, etc.). Es un `data point`
- **Bag**: conjunto de instancias.
- **Etiqueta del bag**: conocida para el conjunto completo, no para cada instancia.
- Una instancia positiva dentro de un bag positivo se denomina comúnmente **witness** (testigo)[](https://www.mdpi.com/2079-9292/12/20/4323?utm_source=chatgpt.com)
---
# ✅ Ejemplo clásico (Detección de Cáncer)
- Una imagen (bag) contiene múltiples regiones (instancias).
- **Imagen positiva** → al menos una región con cáncer.
- **Imagen negativa** → ninguna región con cáncer.
- No se sabe cuál región es responsable, *solo el bag está etiquetado como* ***positivo/negativo***.
---

# 📊 Aprendizaje en MIL

1. **Clasificación a nivel de instancia**: se entrena una función $f(x)$ que asigna una probabilidad o score a cada instancia
2. **Agregado (pooling)**: combinar scores/embeddings para obtener una representación del bag:
	- _Max pooling_
	- _Mean pooling_
	- _Attention-based pooling_ (muy utilizado actualmente)
3. **Clasificación final del bag**: aplicando un clasificador al embedding agregado.


[[CLASE 9 Redes Neuronales Convolucionales (CNN) - (marzo 31 2023)### Capas Pooling|Capas Pooling en Redes Neuronales]]
[[Redes Convolucionales#Padding, strides, max pooling y stacking en las REDES CONVOLUCIONALES|Capas Pooling Clase Redes Convolucionales 2025]]
- Analizar el contenido de una imagen **por bloques o regiones**
- Se usa para **extraer la información más representativa** de las mismas
- Similar a los strides
	- Reduce la cantidad de datos **entre una capa y otra**, para **facilitar el procesamiento** imágenes y el **entrenamiento de la red**
	- **Reduce la cantidad de datos y preserva la información**
- 

---
# 🧩 Tipos de métodos MIL

## 1. _Instance-space (IS)_:
- Clasificación desde el nivel instancia y luego agregación mediante asunción MI estándar, colectiva (suma/average) o máxima/mínima
- Ejemplos:
	- **mi-SVM** y **MI-SVM** (extensiones de SVM para MIL) 
	- **EM-DD** (Diverse Density con Expectation-Maximization).
	- **RSIS**, **MIL-Boost**, **mi‑Net** (red neuronal MIL)

## 2. _Bag-space (BS)_:
- Trata cada bag como entidad completa y entrena un clasificador sobre la similitud entre bags (p.ej. kNN, SVM sobre distancias de bag)

## 3. _Embedded-space (ES)_:
- Mapea cada bag a un solo embedding (“meta-instancia”) y entrena sobre él; pooling + red neuronal es típico

---
# 🔬 Aplicaciones comunes

- **Imagen médica (histopatología)**: 
	- Bag = imagen completa, 
	- instancias = parches; 
	- solo se etiqueta el diagnóstico general
- **Química computacional**: Moléculas con múltiples conformaciones como instancias y molécula etiquetada como activa o no.
- **NLP (Document Classification)**: Documentos compuestos por múltiples páginas o párrafos; sólo se conoce la etiqueta del documento.
- **Audio/Video weak labels**: etiquetas a nivel de clip/video sin segmentación temporal precisa 
- **Marketing, series temporales**: se conoce un total agregado, pero no el detalle por componente o periodo.

---
## 🧠 Ventajas de MIL

- Reduce **costos de anotación**: no requiere etiquetar cada instancia.
- Refleja escenarios reales donde solo hay etiquetas a nivel agregado o más elevado.
- Ideal para aprendizaje débil o semi-supervisado (etiquetas difusas)
---
## 📌 Técnicas modernas

- **mi-Net**: red neuronal que estima score para cada instancia antes de agregación mil-pooling (max, mean, log‑sum‑exp) 
- **DSMIL** (Dual-stream Self‑Attention MIL): primero max‑pool para encontrar la instancia más activada, luego atención auto-regresiva para atención fina sobre todas instancias
- **Attention-aware Multiple-Instance Neural Network**: aprendizaje end‑to‑end con un operador de pooling basado en atención espacial entrenable, mejor alineación de instancias clave y representación de bag 
- **CAP (Cross-Attention Pooling)**: diseñado para _verificación MIL_, usa atención cruzada (query‑bag) para mejorar precisión y explicabilidad
---

## 📚 Comparativa rápida de métodos

|Enfoque|Nivel de etiqueta|Pooling típico|Aplicabilidad actual|
|---|---|---|---|
|Instance-space|Instancia oculta|Max/Mean/Mil-pooling|EM-DD, mi-SVM, mi-Net (deep learning)|
|Embedded-space|Bag completo|Embedding + red neuronal|mi‑Net, atención basada, DSMIL, CAP|
|Bag-space|Bag completo|Similitud entre bags|kNN- / SVM-bag-level|

---
🔄 Diagrama de flujo de datos en MIL (Mermaid)

```mermaid
flowchart TD
  graph TD
  A(Bag con instancias) --> B1(Instancia 1)
  A --> B2(Instancia 2)
  A --> B3(Instancia 3)
  B1 --> C1(Embedding instancia 1)
  B2 --> C2(Embedding instancia 2)
  B3 --> C3(Embedding instancia 3)
  C1 --> D(Pooling: max/mean/atención)
  C2 --> D
  C3 --> D
  D --> E(Embedding del Bag)
  E --> F(Clasificador final)
  F --> G(Predicción del Bag)


```






---

# 📚 Referencias

1. **NILG.AI**. _An Introduction to Multiple Instance Learning_ (Paulo Maia, 2021). [https://nilg.ai/202105/an-introduction-to-multiple-instance-learning](https://nilg.ai/202105/an-introduction-to-multiple-instance-learning)

2. **Wikipedia**. _Multiple Instance Learning_. https://en.wikipedia.org/wiki/Multiple_instance_learning
    
3. **Papers with Code**. _Multiple Instance Learning Benchmarks and Papers_. https://paperswithcode.com/task/multiple-instance-learning
    
4. **MDPI Electronics Journal**. _A Comprehensive Review on Multiple Instance Learning_. https://www.mdpi.com/2079-9292/12/20/4323
    
5. **Medium – One Minute ML**. _Multiple Instance Learning – One Minute Introduction_ (Jeffrey Boschman). https://medium.com/one-minute-machine-learning/multiple-instance-learning-one-minute-introduction-c1a382936105
    
6. **arXiv (DSMIL)**. _Dual-stream Maximum Self-attention Multi-instance Learning_. [https://arxiv.org/abs/2006.05538](https://arxiv.org/abs/2006.05538)
    
7. **arXiv (Multiple Instance Verification)**. _Multiple Instance Verification_ (2024). [https://arxiv.org/abs/2407.06544](https://arxiv.org/abs/2407.06544)
    
8. **MDPI Encyclopedia**. _Multiple-Instance Learning Methods_. https://encyclopedia.pub/entry/50741