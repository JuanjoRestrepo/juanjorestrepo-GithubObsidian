---
title: "Sentencias Condicionales"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Controlar el flujo de nuestro programa con sentencias condionales:
```python
numero = 10

if numero > 0:
    print("El número es positivo")
elif numero < 0:
    print("El número es negativo")
else:
    print("El número es cero")
```
## SENTENCIA IF / IN
El uso de la estructura `if patron in texto` se utiliza para verificar si un patrón o una cadena de caracteres específica está presente dentro de otra cadena de texto:
Verificar si una palabra está presente en una oración:
```python
texto = "El perro juega en el parque"
patron = "perro"

if patron in texto:
    print("La palabra 'perro' está presente en el texto.")
else:
    print("La palabra 'perro' no está presente en el texto.")
```
Otro ejemplo:
```python
texto = "Mi número de teléfono es 123456789"
patron = "123456789"

if patron in texto:
    print("El número de teléfono está presente en el texto.")
else:
    print("El número de teléfono no está presente en el texto.")
```
Otro ejemplo más:
```python
texto = "Visita nuestro sitio web en https://www.ejemplo.com"
patron = "ejemplo"

if patron in texto:
    print("El patrón 'ejemplo' está presente en la URL.")
else:
    print("El patrón 'ejemplo' no está presente en la URL.")
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
