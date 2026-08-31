---
tags:
  - POO
  - "#Decoradores"
---



En Python un decorador es una función especial que decora a otra. Por ejemplo, si yo tengo una función que dice 'hablar' y tengo otra función que decora a esa función, es porque esta ultima agrega otra función a la de 'hablar'.

En otras palabras, la función hablar dice hola y la otra función lo que hace es agregar un código extra a la que ya existía, que es la hola. 

Ejecuta la función hablar y luego agrega otro código adicional para decorarla.

## Ejemplo
---
```Python
def decorador(funcion):
    def funcion_modificada():
        print("Antes de llamar a la funcion")
        funcion()
        print("Despues de llamar a la funcion")
    return funcion_modificada

  
def saludo():
    print("Hola Juanjo")

saludo_modificado = decorador(saludo) # Esto ahora pasa a ser una funcion
saludo_modificado()
```

Sin embargo, existe una manera mas fácil para definir un decorador y esto es utilizando un arroba `@`

```Python
def decorador(funcion): #aqui esta el decorador
    def funcion_modificada():
        print("Antes de llamar a la funcion")
        funcion()
        print("Despues de llamar a la funcion")
    return funcion_modificada

# def saludo():
#     print("Hola Juanjo")

# saludo_modificado = decorador(saludo) # Esto ahora pasa a ser una funcion
# saludo_modificado()

  
@decorador #esto es un decorador
def saludo():
    print("Hola Juanjo que mas")

saludo()
```

De esa manera, usando el arroba le estamos indicando al desarrollador que eso es un decorador.

En resumen, el decorador toma una función y le agrega funcionalidad antes o después de ejecutarla, para al final devolver la función modificada.

# Decorador Property
---
Las propiedades nos permiten definir getters, setters y deleters, es decir, que también podemos eliminar valores, método, etc...

Para definirlo en python usamos: `@property`

```Python
class Persona:
    def __init__(self, nombre, edad):
        self.__nombre = nombre
        self.__edad = edad


    @property
    def nombre(self):
        return self.__nombre

  
juan = Persona("Juan", 23)
nombre = juan.nombre
print(nombre)
```


```Python
class Persona:
    def __init__(self, nombre, edad):
        self.__nombre = nombre
        self.__edad = edad

    @property # Decorador 1
    # Accede a la propiedad
    def nombre(self):
        return self.__nombre

    @nombre.setter# Decorador
    # Modifica a la propiedad
    def nombre(self, new_nombre):
        self.__nombre = new_nombre

    @nombre.deleter# Decorador
    # Elimina valores de la propiedad
    def nombre(self):
        del self.__nombre

juan = Persona("Juan", 23)
nombre = juan.nombre
print(nombre)

juan.nombre = "Pepe"
nombre = juan.nombre
print(nombre)

del juan.nombre
nombre = juan.nombre
print(nombre)
```