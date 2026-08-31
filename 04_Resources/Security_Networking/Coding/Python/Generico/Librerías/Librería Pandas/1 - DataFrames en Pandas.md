---
title: "1 - DataFrames en Pandas"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Un DataFrame es una estructura de datos tabular que se utiliza para almacenar y manipular datos en filas y columnas. Por ejemplo de esta manera, donde tenemos un diccionario y queremos estructurar la información:
```python
import pandas as pd

data = {'Nombre': ['Manzana', 'Naranja', 'Pera', 'Limón'], 
        'Precio': [25, 30, 22, 27], 
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']}

df = pd.DataFrame(data)

print(df)
```
Y si imprimimos esto la información se mostrará de esta manera:
![[Pasted image 20230407073854.png]]
También podemos guardar un dataframe dentro de un archivo .csv:
```python
import pandas as pd

data = {'Nombre': ['Manzana', 'Naranja', 'Pera', 'Limón'], 
        'Precio': [25, 30, 22, 27], 
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']}

df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datos_frutas.csv', index=False)

print("DataFrame guardado en datos_frutas.csv")
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
