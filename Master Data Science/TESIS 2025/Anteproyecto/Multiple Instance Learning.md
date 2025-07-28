
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
2.  




---
# Fuentes:
1. https://nilg.ai/202105/an-introduction-to-multiple-instance-learning/

