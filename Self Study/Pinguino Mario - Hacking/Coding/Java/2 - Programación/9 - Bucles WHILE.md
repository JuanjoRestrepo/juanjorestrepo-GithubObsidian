---
title: "9 - Bucles WHILE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Java, el bucle `while` se utiliza para repetir un bloque de código mientras una condición sea verdadera. La estructura básica del bucle `while` es la siguiente:
```java
public class Main {
    public static void main(String[] args) {
        int contador = 1;

        while (contador <= 5) {
            System.out.println("Número: " + contador);
            contador++;
        }
    }
}
```
![[Pasted image 20240304194708.png]]
En este ejemplo, el bucle `while` se ejecutará mientras la variable `contador` sea menor o igual a 5. En cada iteración, se imprime el valor de `contador` y se incrementa en 1. El bucle terminará cuando `contador` alcance el valor 6.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
