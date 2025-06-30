---
tags:
  - POO
  - Poliformismo
---



**polimorfismo** es el uso de un solo símbolo para representar múltiples tipos diferentes

- Poli: Muchas
- Morfismo: formas

Muchas formas

En la programación orientada a objetos, el polimorfismo es la provisión de una interfaz única para entidades de diferentes tipos.

Se puede clasificar el polimorfismo en dos grandes clases:

- **Polimorfismo dinámico** (o **polimorfismo paramétrico**) es aquel en el que el código no incluye ningún tipo de especificación sobre el tipo de datos sobre el que se trabaja. Así, puede ser utilizado a todo tipo de datos compatible.
- **Polimorfismo estático** (o **polimorfismo _ad hoc_**) es aquél en el que los tipos a los que se aplica el polimorfismo deben ser explícitos y declarados uno por uno antes de poder ser utilizados.

### Ejemplo en Python:
---
```Python
class Gato():
    def sonido(self):
        return "Miau"

class Perro():
    def sonido(self):
        return "Guau"

def hacer_sonido(animal):
    print(animal.sonido())

gato = Gato()
perro = Perro()

hacer_sonido(gato)
hacer_sonido(perro)

#print(gato.sonido())
#print(perro.sonido())
```

En lenguajes estáticos como C++ o Java, yo no puedo llamar un método igual dos o mas veces, como el de sonido, por mas que sean de diferentes clases

Para eso tendría que crear otro método.

Sino, deberán ser clases que hereden de otra para que si o si utilicen el mismo método, como aquí:

```Python
class Animal()
    def sonido(self):
        pass

class Gato(Animal):
    def sonido(self):
        return "Miau"

class Perro(Animal):
    def sonido(self):
        return "Guau"

def hacer_sonido(animal):
    print(animal.sonido())

gato = Gato()
perro = Perro()

hacer_sonido(gato)
hacer_sonido(perro)
```

### Polimorfismo sobrecarga (No existe en Python)
---
### En Java por ejemplo:

```Java
class Escrito
{
	public void Escribe(){
		Console.WriteLine("No tengo parametros");
	}
	public void Escribe(int numero){
		Console.WriteLine("Numero: " + numero.ToString() );
	}
	public void Escribe(int numero, string texto){
		Console.WriteLine(
		"Numero: " + numero.ToString() 
		+ ", Texto: " + texto );
	}
	public void Escribe(int numero, string texto, DateTime fecha){
		Console.WriteLine(
		"Numero: " + numero.ToString() 
		+ ", Texto: " + texto 
		+ ", Fecha: " + fecha.ToString() );
	}
}
```

Lo que permite esto es que me permite crear una clase que tenga un mismo método, pero que dependiendo de los parámetros que se le pasen, se comporta de diferente forma.

Esto en Python no se necesita hacer. Porque python tiene la posibilidad de adaptarse al tipo de dato

```Python
def recorrer(elemento):
	for item in elemento:
		print(f"El elemento actual es: {item}")

lista = [1,2,3,4]
lista2 = ["maquina", "como", "andas"]

recorrer(lista)
recorrer(lista2)

# OUTPUT
# El elemento actual es: 1, 2, 3, 4
# El elemento actual es: m, a, q, u, i, n, a
```


[Duck Typing](https://www.youtube.com/watch?v=9-qZHRxd_g8)
[Lógica de Polimorfismo con MINECRAFT](https://www.youtube.com/watch?v=bblFTvuk4pY)
