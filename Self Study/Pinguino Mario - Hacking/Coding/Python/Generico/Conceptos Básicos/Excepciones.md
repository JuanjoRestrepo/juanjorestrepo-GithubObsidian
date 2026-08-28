---
title: "Excepciones"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Python, las excepciones son eventos que ocurren durante la ejecución de un programa y que interrumpen el flujo normal de instrucciones. Puedes manejar estas excepciones utilizando bloques `try`, `except`. 

----------

**Índice fuera de rango**
```python
lista = [1, 2, 3]
try:
    elemento = lista[5]
except IndexError:
    print("Error: Índice fuera de rango.")
```
![[Pasted image 20231220114147.png]]
**Tipo de dato incorrecto**
```python
try:
    numero = int("abc")
except ValueError:
    print("Error: No se puede convertir a entero.")
```
![[Pasted image 20231220114215.png]]
**Archivo no encontrado**
```python
try:
    with open("archivo_que_no_existe.txt", "r") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print("Error: Archivo no encontrado.")
```
![[Pasted image 20231220114334.png]]
**Operación no permitida**
```python
try:
    resultado = "Hola" + 5
except TypeError:
    print("Error: Operación no permitida con estos tipos de datos.")
```
![[Pasted image 20231220114434.png]]
**Uso incorrecto de una biblioteca**
```python
try:
    import biblioteca_que_no_existe
except ImportError:
    print("Error: No se pudo importar la biblioteca.")
```
![[Pasted image 20231220114530.png]]
**Interrupción del Usuario (Ctrl + C)**
```python
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Se ha interrumpido la ejecución por el usuario.")
```
![[Pasted image 20231220114651.png]]
Se encuentra dentro de un bucle infinito, que tras detenerlo con control + C, se ejecuta el print dentro de la excepción:
![[Pasted image 20231220114637.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
