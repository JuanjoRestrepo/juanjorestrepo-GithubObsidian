---
title: "11 - Funciones"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Java, las funciones se definen mediante la creación de métodos. Un método es un bloque de código que realiza una tarea específica y puede ser invocado (llamado) desde otro lugar en el programa.
```java
public class FuncionesBasicas {

    // Definición de una función para sumar dos números enteros
    public static int sumar(int a, int b) {
        return a + b;
    }

    // Definición de una función para multiplicar dos números enteros
    public static int multiplicar(int a, int b) {
        return a * b;
    }

    public static void main(String[] args) {
        // Llamada a las funciones y almacenamiento del resultado
        int resultadoSuma = sumar(5, 3);
        int resultadoMultiplicacion = multiplicar(4, 6);

        // Impresión de los resultados
        System.out.println("El resultado de la suma es: " + resultadoSuma);
        System.out.println("El resultado de la multiplicación es: " + resultadoMultiplicacion);
    }
}
```
![[Pasted image 20240319104759.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
