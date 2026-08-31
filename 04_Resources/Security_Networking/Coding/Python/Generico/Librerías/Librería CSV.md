---
title: "Librería CSV"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Así podemos escribir de forma simple en un CSV:
```python
import csv

# 2. Escritura en un archivo CSV
datos = [
    ['Nombre', 'Apellido', 'Edad'],
    ['John', 'Doe', 25],
    ['Jane', 'Smith', 30]
]

with open('nuevos_datos.csv', 'w', newline='') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerows(datos)
```
Y este es el resultado, donde vemos que las 3 líneas se han escrito por orden:
![[Pasted image 20230531165412.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
