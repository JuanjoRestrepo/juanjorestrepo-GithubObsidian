---
title: "1 - Hola Mundo en Java + Primeros Pasos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para imprimir un hola mundo en Java, necesitamos crear una clase que será el punto de partida; y a continuación siempre tendremos que poner la siguiente instrucción:
```java
public static void main(String[] args) {}
```
Y ya una vez con esto puesto podemos imprimir un mensaje por pantalla:
```java
public class Main {

    public static void main(String[] args) {
        System.out.println("Hola Mundo");
    }
}
```
Y ahora ya podemos imprimir un mensaje por pantalla:
![[Pasted image 20240304164649.png]]
Y si queremos imprimir otro mensaje por pantalla, podemos reutilizar la misma clase y simplemente añadimos otra línea:
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hola Mundo");
        System.out.println("Otro Mensaje");
    }
}
```
![[Pasted image 20240304165721.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
