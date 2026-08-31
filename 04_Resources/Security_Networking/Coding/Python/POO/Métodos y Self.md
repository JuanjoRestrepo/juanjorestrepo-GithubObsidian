---
title: "Métodos y Self"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

## MÉTODOS (Las funciones que están dentro de la clase)

Los métodos nos permiten definir funcionalidades para llamarlas desde las instancias. Es algo similar a una función. Por ejemplo ahora vamos a crear una clase que se llame gestion_archivos, y tenga dos métodos, uno de crear una carpeta y luego otro de listar archivos; y haremos la llamada a uno u otro método:
```python
import os

class gestion_archivos:
    pass

    def carpeta():
        os.mkdir("Carpeta_nueva")

    def listar():
        print(os.listdir())

gestion_archivos.listar()
```
![[Pasted image 20230112222840.png]]
## OTRO EJEMPLO
De esta forma podremos controlar el flujo de trabajo y en el constructor init se recogerán los datos que podremos usarlos en los métodos, ya que las variables se heredan mediante self:
```python
class Calculadora:
    def __init__(self, numero1, numero2):
        self.numero1 = numero1
        self.numero2 = numero2

    def sumar(self):
        resultado = (self.numero1 + self.numero2)
        print(f"El resultado de la suma es {resultado}")

    def restar(self):
        resultado = (self.numero1 - self.numero2)
        print(f"El resultado de la resta es {resultado}")

    def multiplicar(self):
        resultado = (self.numero1 * self.numero2)
        print(f"El resultado de la multiplicación es {resultado}")

numero1, numero2 = 2,3
calculo1 = Calculadora(numero1,numero2)

eleccion = input('Escribe sumar, restar o multiplicar')

if eleccion == 'sumar':
    calculo1.sumar()

elif eleccion == 'restar':
    calculo1.restar()  

elif eleccion == 'multiplicar':
    calculo1.multiplicar()
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
