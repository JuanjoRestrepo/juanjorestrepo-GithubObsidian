---
title: "Notas libro"
date: 2026-08-27
tags:
  - self-study
  - development-architecture
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# _Do not use using namespace std;_

[[Modern C++ for Absolute Beginners- A Friendly Introduction to the C++ Programming Language and C++11 to C++23 Standards.pdf#page=26&selection=73,0,100,65|Por que no usar 'using namespace std']]

Many examples on the Web introduce the entire std namespace into the current scope via the using namespace std; statement only to be able to type `cout` instead of the `std::cout`.

While this might save us from typing five additional characters, it is **wrong** for many reasons. We do not want to introduce the entire _std_ namespace into the current scope because we want to avoid name clashes and ambiguity.

**Good to remember**
> Do not introduce the entire std namespace into a current scope via the using namespace std; statement.

So, instead of this wrong approach:
```cpp
#include <iostream>

using namespace std; // do not use this

int main()
{
	cout << "Bad practice.";
}
```

Use the following:
```cpp
#include <iostream>

int main()
{
	std::cout << "Good practice.";
}
```

For calls to objects and functions residing inside the std namespace, add the `std::` prefix where needed.

---

# _Passing Arguments_
There are different ways of passing arguments to a function. Here, we will describe the three most used

[[Modern C++ for Absolute Beginners- A Friendly Introduction to the C++ Programming Language and C++11 to C++23 Standards.pdf#page=102&selection=44,0,46,16|Paso por Valor y Paso por Referencia]]


---

# _Pointers_

[[Modern C++ for Absolute Beginners- A Friendly Introduction to the C++ Programming Language and C++11 to C++23 Standards.pdf#page=51&selection=4,0,4,8|Pointers -  página 51]]

---
# _Símbolos Modificadores de Acceso UML_
[[2.DiseñoOrientadoObjetos#^uml-modifier-symbols|Ver símbolos UML]]

# _Símbolos Relaciones BBDD & EDR_


#### Class Diagram Symbols

![[UML Symbols.png]]

`Profesor o-- Curso` : Agregacion 
`Curso --> Salon ` : Asociacion


[[2. EDR RELACIONES]]

![[Pasted image 20250702173124.png]]

![[EDR Symbols.png]]


# _Mermaid Docs_
[Mermaid Sintaxis and Symbols](https://mermaid.js.org/syntax/classDiagram.html)

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Development & Architecture|Desarrollo y arquitectura]].
- Criterio de producción: Conecta el concepto con contratos explícitos, validación de entrada, pruebas automatizadas, observabilidad y despliegues reversibles.
