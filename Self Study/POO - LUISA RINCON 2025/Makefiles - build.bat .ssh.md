---
tags:
  - CPP
  - POO
  - OOP
fecha: 2025-06-29
---

## 🧰 Makefile vs. build script (`build.sh`)

- **Makefile**    
    - Es un **sistema de construcción declarativo**: defines **qué** se debe hacer y **cómo** (reglas, dependencias), y `make` decide cuándo es necesario ejecutar cada paso        
    - *Ventajas*:
        - Solo recompila lo necesario (eficiencia).
        - Facilita gestionar múltiples archivos y reglas complejas.
            
- **Script (build.sh)**
    - Es **imperativo y secuencial**: ejecuta paso a paso sin lógica de dependencias.
    - Bueno para proyectos pequeños con uno o pocos archivos.
    - Más simple de entender y directo.
        

---

## 🔄 ¿Por qué usar Makefile en lugar de un script?

1. **Eficiencia**: recompila solo lo cambiado.
2. **Escalabilidad**: ideal para proyectos con múltiples módulos.
3. **Mantenimiento más limpio**: separa lógica de compilación y ejecución.
4. Combinable con `make run`, `make clean`, `make test`, etc.
    

---

## 📦 ¿Y CMake?

- Es un **generador de sistemas de construcción**: escribe tus reglas en `CMakeLists.txt`, y CMake crea Makefiles ó proyectos para Ninja, Xcode, Visual Studio, etc. [earthly.dev+3stackoverflow.com+3es.wikipedia.org+3](https://stackoverflow.com/questions/25789644/what-is-the-difference-between-using-a-makefile-and-cmake-to-compile-the-code?utm_source=chatgpt.com).
    
- *Ventajas*:
    - **Multiplataforma**: mismo archivo fuente, múltiples plataformas sin duplicación.
    - Maneja dependencias complejas, pruebas, empaquetado y out-of-source builds [es.wikipedia.org](https://es.wikipedia.org/wiki/CMake?utm_source=chatgpt.com).
    - Moderno y ampliamente adoptado: usado por proyectos como LLVM, KDE, OpenCV [incredibuild.com](https://www.incredibuild.com/blog/cmake-vs-make?utm_source=chatgpt.com).
- Inconvenientes: sintaxis algo más compleja, requiere entender dos niveles: CMake y el sistema subyacente (`make`, `ninja`…).
    

---

## 🗺️ Resumen comparativo

|Herramienta|Ideal para…|Pros|Contras|
|---|---|---|---|
|**build.sh / .bat**|Scripts simples, un solo archivo fuente|Fácil, directo, cero lógica de dependencias|Recompila todo siempre, no escala bien|
|**Makefile**|Proyectos C/C++ con varias fuentes|Efficient recompilation, flexible|Puede complicarse y depender de entorno plataforma|
|**CMake**|Proyectos multiplataforma o con dependencias|Genera los archivos correctos en cada plataforma|Curva de aprendizaje, más complejo|

---

## ✅ ¿Qué deberías usar?

- **Proyecto pequeño y local** → usa `build.sh`.
- **Proyecto con varios archivos y compilación incremental** → usa Makefile.
- **Proyecto que crecerá, soportará varias plataformas o IDEs** → considera CMake.