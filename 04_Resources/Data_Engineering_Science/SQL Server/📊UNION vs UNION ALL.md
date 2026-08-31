---
title: "📊UNION vs UNION ALL"
date: 2026-08-27
tags:
  - self-study
  - data-science-engineering
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# Diferencia entre `UNION` y `UNION ALL` en SQL Server

En SQL Server, ambos operadores se utilizan para combinar los resultados de dos o más consultas `SELECT` en un solo conjunto de resultados. Sin embargo, tienen una diferencia fundamental en cómo manejan los datos duplicados y el rendimiento.

## Resumen Rápido

| Característica     | `UNION`                                           | `UNION ALL`                                 |
| :----------------- | :------------------------------------------------ | :------------------------------------------ |
| **Duplicados**     | Los **elimina** (devuelve filas únicas)           | Los **mantiene** (devuelve todas las filas) |
| **Rendimiento**    | Más **lento** (filtra/ordena)                     | Más **rápido** (solo une)                   |
| **Uso de Memoria** | Mayor uso (comparar filas para hallar duplicados) | Menor uso (no compara filas)                |


---

## Explicación Detallada

### 1. `UNION`
Este operador combina los conjuntos de resultados y aplica un proceso similar a un `DISTINCT`. Si una fila aparece en ambas consultas, solo se mostrará una vez en el resultado final.

- **Ideal para:** Cuando necesitas una lista de valores únicos y no te importa el costo extra de procesamiento.

### 2. `UNION ALL`
Simplemente une los resultados tal como vienen. Si la Consulta A tiene 5 filas y la Consulta B tiene 5 filas, el resultado tendrá 10 filas, incluso si son idénticas.

- **Ideal para:** Cuando sabes que no habrá duplicados o cuando necesitas ver toda la información sin importar la repetición. **Es la opción recomendada por defecto por su velocidad.**

---

## Ejemplo Práctico
Imagina que tienes dos tablas de clientes:

**Tabla_A** 

| ID  | Nombre |
| :-- | :----- |
| 1   | Juan   |
| 2   | Maria  |

**Tabla_B**

| ID  | Nombre |
| :-- | :----- |
| 2   | Maria  |
| 3   | Pedro  |

### Resultado con `UNION`:
```SQL
SELECT Nombre FROM Tabla_A
UNION
SELECT Nombre FROM Tabla_B;
```

| ID  | Nombre |
| :-- | :----- |
| 1   | Juan   |
| 2   | Maria  |
| 3   | Pedro  |

**Resultado:** Juan, Maria, Pedro (3 filas).


### Resultado con `UNION ALL`:
```SQL
SELECT Nombre FROM Tabla_A
UNION ALL
SELECT Nombre FROM Tabla_B;
```

| ID | Nombre |
| :-- | :-- |
| 1 | Juan |
| 2 | Maria |
| 2 | Maria |
| 3 | Pedro |

**Resultado:** Juan, Maria, **Maria**, Pedro (4 filas).


## ⚠️ Reglas de Estructura
Para que funcionen, debes cumplir:
1. Mismo **número de columnas**.
2. **Tipos de datos** compatibles en el mismo orden.
3. El nombre de las columnas finales será el del **primer SELECT**.

> [!TIP] Tip de Rendimiento
> Si no te importa ver duplicados, usa siempre `UNION ALL`. Es significativamente más rápido en bases de datos grandes.

#SQL #Database #SqlServer

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Data Science & Engineering|Ciencia e ingeniería de datos]].
- Criterio de producción: Preserva linaje, esquemas y calidad de datos; separa datos crudos, validados y listos para consumo antes de modelar o publicar.
