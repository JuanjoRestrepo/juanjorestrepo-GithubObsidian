---
title: "Constructor"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La finalidad del constructor es llamar automáticamentre al crear un objeto, permitiendo enviar datos desde el principio a los métodos:
```
class Galleta:
    chocolate = False

    def __init__(self, SABOR, COLOR):
        self.sabor = SABOR
        self.color = COLOR
        print(f"Se acaba de crear una galleta {self.color} y {self.sabor}.")

galleta_1 = Galleta("marrón", "amarga")
galleta_2 = Galleta("blanca", "dulce")
```
![[Pasted image 20230112224822.png]]
La información viaja de la siguiente manera:
![[Pasted image 20230112225526.png]]
Ahora veremos el funcionamiento con una herramienta que convierte el texto en minúscula o mayúsculas, de tal forma que podremos elegir el método (función) que queramos ejecutar:

```
class conversion:
    chocolate = False

    def __init__(self, SABOR, COLOR):
        self.sabor = SABOR
        self.color = COLOR

    def mayuscula(self):
        print("Convertimos a mayúscula: ", self.sabor.upper())

    def minuscula(self):
        print("Este texto saldrá en minúscula: ", self.sabor.lower())

MiConversion = conversion("DULCE", "marron")
MiConversion.mayuscula() # Aquí llamamos al método que queramos (a una función u otra)
```
![[Pasted image 20230113103158.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
