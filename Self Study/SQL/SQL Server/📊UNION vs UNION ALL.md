
# Diferencia entre `UNION` y `UNION ALL` en SQL Server

En SQL Server, ambos operadores se utilizan para combinar los resultados de dos o más consultas `SELECT` en un solo conjunto de resultados. Sin embargo, tienen una diferencia fundamental en cómo manejan los datos duplicados y el rendimiento.

## Resumen Rápido

|**Característica**|**UNION**|**UNION ALL**|
|---|---|---|
|**Duplicados**|Los **elimina** (solo devuelve filas distintas).|Los **mantiene** (devuelve todas las filas).|
|**Rendimiento**|Más **lento** (requiere un proceso de filtrado/ordenado).|Más **rápido** (solo "pega" los resultados).|
|**Uso de memoria**|Mayor (debe comparar filas para hallar duplicados).|Menor (no necesita comparar nada).|

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
| ID | Nombre |
| :--- | :--- |
| 1 | Juan |
| 2 | Maria 


**Tabla_B** | ID | Nombre | | :--- | :--- | | 2 | Maria | | 3 | Pedro |

### Resultado con `UNION`:
```SQL
SELECT Nombre FROM Tabla_A
UNION
SELECT Nombre FROM Tabla_B;
```
**Resultado:** Juan, Maria, Pedro (3 filas).

### Resultado con `UNION ALL`:
```SQL
SELECT Nombre FROM Tabla_A
UNION ALL
SELECT Nombre FROM Tabla_B;
```
**Resultado:** Juan, Maria, **Maria**, Pedro (4 filas).
