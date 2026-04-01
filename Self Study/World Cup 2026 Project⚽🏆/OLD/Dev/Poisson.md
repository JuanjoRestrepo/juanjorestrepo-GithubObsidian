
# Poisson Goal Model

Modelamos:

- $\lambda_{home} = E[goles\_home]$
- $\lambda_{away} = E[goles\_away]$

Luego:

$$
P(score = i,j) = Poisson(i, \lambda_{home}) \cdot Poisson(j, \lambda_{away})
$$

Y de ahí:

- $Win → i>j$
- $Draw → i=j$
- $Loss → i<j$

---

Con tus resultados, yo **no seguiría combinando clasificadores por intuición**. Ya tienes una señal clara:

- **LogisticRegression** sigue siendo el mejor modelo global en `accuracy` y `logLoss`.
- **Poisson** es mejor cuando miras el problema de forma más futbolística, porque mejora el equilibrio entre clases y captura mejor los empates.
- El **gated ensemble** sí mejora `balancedAccuracy` y `F1` frente a Logistic, pero no mejora `logLoss`, así que como modelo final para simulación todavía no es la mejor pieza.

La decisión más sólida es esta: **usar LogisticRegression solo como benchmark discriminativo y construir el modelo principal sobre una base generativa de goles, pero mejorada**. En la literatura clásica y reciente de predicción de fútbol, el enfoque estándar sigue siendo modelar goles y no solo clases: Dixon-Coles propone un modelo de goles con ataque, defensa y ventaja de local, y además corrige la dependencia en marcadores bajos como 0-0, 0-1, 1-0 y 1-1. Extensiones recientes siguen usando modelos bivariados de Poisson o Dixon-Coles para predicción y simulación de torneos.

También hay una línea muy consistente en usar **ratings dinámicos o evolución temporal de fortalezas**. El trabajo con Elo y ordered logit mostró valor real de ratings derivados del histórico, y modelos más recientes incorporan fuerzas dinámicas de equipo o de jugador, precisamente porque en fútbol la fortaleza cambia con el tiempo. Eso encaja con tu proyecto mejor que seguir apilando clasificadores estáticos.

## Mi recomendación final

### Qué haría ahora

1. **Conservaría tu Notebook 03 actual como benchmark.**
2. **No seguiría afinando el híbrido 70/30.**
3. **Subiría el nivel del modelo Poisson**, porque es el camino más alineado con el estado del arte para fútbol:
    - agregar explícitamente **fuerza ofensiva y defensiva**,
    - usar una corrección tipo **Dixon-Coles** o un modelo bivariado para la dependencia de marcadores bajos,
    - y luego **calibrar probabilidades** antes de simular el Mundial.

### Por qué esa ruta es la correcta para tu objetivo

Tu objetivo inicial no era solo clasificar partidos; era construir algo digno de CV/GitHub/LinkedIn y útil para simular el Mundial 2026. Para eso, lo importante no es solo la clase correcta, sino que las **probabilidades estén bien calibradas** y que el modelo represente bien los **marcadores bajos**, que son críticos en fútbol. Scikit-learn documenta la calibración como una capa separada para mejorar la calidad de probabilidades de clasificación, y eso es exactamente lo que te conviene si vas a alimentar una simulación de torneo.

## En concreto, la siguiente iteración debería ser esta

### Opción recomendada

**Notebook 02**
- añadir un par de features defensivas y de simetría que ya discutimos,
- mantener el enfoque temporal,
- y dejar el dataset listo para un modelo de goles más fuerte.

**Notebook 03**
- reemplazar el Poisson simple por una versión con:
    - ataque local,
    - defensa rival,
    - ventaja de local,
    - corrección para bajos marcadores,
    - calibración final de probabilidades.

### Qué no haría todavía

- no seguiría aumentando complejidad del ensemble;
- no movería a stacking real todavía;
- no intentaría meter más clasificadores sin antes arreglar el modelo de goles.  
    Eso sería más ingeniería que ganancia estadística.


> La mejor jugada ahora es hacer que Poisson sea el modelo principal, pero con defensa y dependencia de marcadores bajos; luego calibrar probabilidades y usar eso para la simulación del torneo.


