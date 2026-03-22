

La dirección correcta es abandonar la clasificación directa como modelo principal y pasar a un modelo de goles. La búsqueda de hiperparámetros puede venir después, pero no antes de tener una formulación correcta del problema.

Thought for 8s

Sí. **Poisson es el salto correcto**. Y sobre hiperparámetros, mi decisión es esta:

> **No haría una búsqueda exhaustiva todavía.**  
> Haría primero un **Poisson baseline bien formulado**, y luego una **tuning corta y dirigida** solo si hace falta.

La razón es simple: el problema principal no era falta de ajuste fino, sino que el modelo estaba atacando el objetivo de forma indirecta. La mejora real va a venir de **modelar goles** y después derivar win/draw/loss.

---

# Decisión técnica

## Lo que sí haremos

Mantener tu modelo actual como **baseline comparativo**, pero pasar a un modelo principal basado en goles:

- predecir `homeScore`
- predecir `awayScore`
- derivar probabilidades de:
    - home win
    - draw
    - away win

Eso es mucho más natural para fútbol.

---

# Lo que recomiendo implementar

## 1) Modelo principal

Usar **dos modelos Poisson**:

- uno para goles del local
- otro para goles del visitante

Con eso obtienes tasas esperadas:

- `lambdaHome`
- `lambdaAway`

Luego calculas la matriz de marcadores posibles y de ahí sacas las probabilidades de resultado.

---

## 2) Ajuste fino, pero solo el necesario

Aquí sí conviene una búsqueda pequeña, no enorme.

### Buscar solo esto:

- `alpha` de regularización del Poisson
- posible **peso temporal** de partidos recientes
- si usas un modelo alternativo, unos pocos hiperparámetros básicos

### No buscar todavía:

- grids grandes
- ensambles complejos
- demasiados modelos a la vez

Eso sería costo alto con ganancia marginal.


---

# Qué sí puede mejorar mucho el modelo

## A. Ponderación temporal

Los partidos recientes deben pesar más que los antiguos.

Eso suele mejorar bastante en fútbol, porque el estado de una selección cambia con el tiempo.


## B. Corrección para marcadores bajos

Si el draw sigue débil, el siguiente ajuste natural es una corrección tipo **Dixon-Coles**, que mejora la modelación de resultados de baja anotación.

Ese ajuste es especialmente útil cuando hay muchos 0-0, 1-0, 1-1, 0-1.

## C. Evaluación adecuada

Ya no nos vamos a quedar solo con accuracy.

Vamos a evaluar dos niveles:

### Nivel 1: goles

- MAE de goles
- Poisson deviance

### Nivel 2: resultado final

- log loss
- balanced accuracy
- recall de draw




## Fase siguiente
No crearía otro notebook innecesario si quieres mantener el repo limpio.  
Haría una **sección nueva dentro del Notebook 03** o una extensión clara del flujo actual para:

1. entrenar Poisson para goles
2. convertir goles esperados en probabilidades de resultado
3. comparar contra tu modelo actual
4. decidir si hace falta Dixon-Coles o tuning corto


