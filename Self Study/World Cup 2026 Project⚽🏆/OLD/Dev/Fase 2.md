# Feature Engineering (clave del proyecto)

En el siguiente paso vamos a construir:
- fuerza de equipos (Elo o aproximación)
- forma reciente (últimos N partidos)
- promedio de goles
- diferencial de rendimiento
- localía
- historial entre equipos (opcional avanzado)

Se construye el **Notebook 02 — Feature Engineering + construcción del dataset de modelado**  
(con lógica profesional, no básica)

---

# Notebook 02 — Feature Engineering + construcción del dataset de modelado

- Features sin fuga de información
- Ratings dinámicos
- Dataset listo para modelar

La idea es que este notebook genere un dataset final de modelado con:
- rating Elo dinámico,
- forma reciente,
- rendimiento acumulado,
- descanso entre partidos,
- historial entre selecciones,
- contexto del torneo,
- target `win / draw / loss`.

