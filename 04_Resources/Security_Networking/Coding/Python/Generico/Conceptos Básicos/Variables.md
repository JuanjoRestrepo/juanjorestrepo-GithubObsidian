---
title: "Variables"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con las variables podemos asignar un valor. Las variables pueden contener diferentes tipos de datos, como números, caracteres, cadenas de texto, booleanos, entre otros.

```python
# Crear una variable numérica
edad = 25

# Crear una variable de texto
nombre = "Juan"

# Crear una variable booleana
es_hombre = True
```
Luego, se pueden utilizar las variables en diferentes operaciones y expresiones. Por ejemplo, se pueden imprimir los valores de las variables en la consola con la función print:
```python
print("La edad de", nombre, "es", edad)
print("¿Es", nombre, "hombre?", es_hombre)
```
Esto producirá la salida:
```python
La edad de Juan es 25
¿Es Juan hombre? True
```
También se pueden utilizar las variables en expresiones matemáticas:
```python
# Sumar 5 a la edad actual
edad += 5

# Dividir la edad por 2 y redondear hacia abajo
edad //= 2

# Imprimir el resultado
print("La nueva edad de", nombre, "es", edad)
```
Esto producirá la salida:
```python
La nueva edad de Juan es 15
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
