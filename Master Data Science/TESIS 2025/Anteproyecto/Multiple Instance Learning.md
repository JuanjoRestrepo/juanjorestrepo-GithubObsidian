
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


---
# Fuentes:
1. https://nilg.ai/202105/an-introduction-to-multiple-instance-learning/

