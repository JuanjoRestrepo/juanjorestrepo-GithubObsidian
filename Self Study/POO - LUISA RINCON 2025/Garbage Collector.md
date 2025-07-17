---
tags:
  - POO
  - OOP
  - CPP
fecha: 2025-07-17
---

En C++, el ==recolector de basura== (garbage collector o GC) no es una característica inherente como en otros lenguajes como Java o C#. 

**C++ tradicionalmente depende de la gestión manual de memoria por parte del programador**, utilizando `new` y `delete` para asignar y liberar memoria, o mediante técnicas como RAII (Resource Acquisition Is Initialization) y punteros inteligentes para automatizar la liberación de recursos.

Aunque existe soporte para la recolección de basura en el **estándar de C++, no es obligatorio implementarlo** y, de hecho, **ha sido eliminado en la versión más reciente, C++23.**


## El problema de la memoria en C++:

- **Gestión manual:** En C++, el programador es responsable de liberar la memoria que ya no se necesita. Si no se libera correctamente, se producen fugas de memoria (**memory leaks**), donde la memoria asignada no se puede volver a utilizar y eventualmente puede llevar a que la aplicación se quede sin memoria.
- **Punteros colgantes (dangling pointers):** Si se libera la memoria a la que apunta un puntero y luego se intenta acceder a esa memoria, se produce un puntero colgante. Esto puede causar comportamientos inesperados y errores difíciles de depurar.

## ¿Por qué no hay garbage collection en C++ por defecto?

- **Control:** C++ se centra en el control y rendimiento, y la gestión manual de memoria permite al programador optimizar el uso de recursos de forma precisa.
- **Rendimiento:** La recolección de basura puede introducir *pausas inesperadas en la ejecución* del programa, lo que puede ser problemático en aplicaciones de tiempo real o de alto rendimiento. *El GC puede ser costoso en términos de rendimiento* y puede causar problemas de latencia



