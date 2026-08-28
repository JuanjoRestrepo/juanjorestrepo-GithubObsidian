---
title: "8 - Bucles FOR"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El bucle `for` en Java es una estructura de control de flujo que permite repetir un bloque de código un número específico de veces. La sintaxis básica del bucle `for` es la siguiente:
```java
public class Main {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("En esta vuelta, el número vale: " + i);
        }
    }
}
```
La variable i recibe el número 1, y luego decimos que mientras i sea 5 o menos, se le va a ir sumando un 1 a cada vuelta:
![[Pasted image 20240304194111.png]]
#### RECORRIENDO UN ARRAY
También podemos recorrer elementos de un array de la siguiente forma:
```java
public class codigo {
    public static void main(String[] args) {
        String[] nombres = {"Mario", "Fátima", "Eustaquio"}; // Array llamado nombres

        for (String nombre : nombres) { // Recorremos cada elemento del array nombres y lo guardamos en la variable nombre
            System.out.println(nombre);
        }
    }
}
```
![[Pasted image 20240307203752.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
