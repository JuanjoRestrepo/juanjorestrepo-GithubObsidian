---
tags:
  - POO
  - "#Encapsulamiento"
---



Es un concepto que consiste en proteger los elementos de una clase como:
- Métodos
- Variables

Como por ejemplo, no quiero que el desarrollador no pueda acceder a una contraseña, debo protegerla.

Estos son:
- **Private:** que se puede acceder solo desde sus clases
- **Public:** que se puede acceder desde cualquier lugar

No existe como tal en Python como en C++ o Java que admiten tipos de acceso, pero para declararlo es usando un guion bajo

```Python
class MiClase:
    def __init__(self):
        self._atributo_privado = "Valor"
```

Para atributos muy muy privados, ponemos dos guiones.
```Python
class MiClase:
    def __init__(self):
        self.__atributo_privado = "Valor"
```

## ¿Por qué usar Encapsulamiento?
---
Porque nos permite ocultar cierta complejidad interna que hay dentro de la clase y también protege los atributos cuando los ponen como privados.

### ¿Cómo accedemos a los datos encapsulados?
Utilizamos los Getters y Setters

- **Getter**: es un método que te usamos para acceder a un atributo muy privado
- **Setter**: es un método que se utiliza para modificar o establecer el valor de un atributo privado

También existen métodos privados
```Python
class MiClase:
    def __init__(self):
        self._atributo_privado = "Valor"

    def __hablar(self):
        print("hola, como estas")

objeto = MiClase()
print(objeto.__hablar)
```

En este caso, no deja correr porque el método hablar, esta como muy muy privado. Pero si se pone solamente privado, si ejecuta:

```Python
class MiClase:
    def __init__(self):
        self._atributo_privado = "Valor"

    def _hablar(self):
        print("hola, como estas")

objeto = MiClase()
print(objeto.__hablar)
# OUTPUT
# hola, como estas
```

## Getters y Setters
---

1. Getter
```Python
class Persona:
    def __init__(self, nombre, edad):
        # Atributos privados
        self.__nombre = nombre
        self.__edad = edad

    def get_nombre(self):
        return self.__nombre # Getter
		# Nos permite acceder al nombre
  
juan = Persona("Juan", 23)
nombre = juan.get_nombre()
print(nombre)
# OUTPUT
# Juan

```

Ponemos nombre y edad como atributos privados y al momento de retornarlos, nos devuelve el nombre haciendo uso del getter

2. Setter
```Python
class Persona:
    def __init__(self, nombre, edad):
        self.__nombre = nombre
        self.__edad = edad

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, new_nombre):
        self.__nombre = new_nombre # Setter

  
juan = Persona("Juan", 23)
nombre = juan.get_nombre()
print(nombre)

juan.set_nombre("Pepito")
nombre = juan.get_nombre()
print(nombre)
```

El setter nos permite modificar el atributo privado. En este caso, cambiamos el valor del nombre de `juan` por `pepito`

