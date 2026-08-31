---
title: "1 - Variables"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Las variables en php se declaran de la siguiente forma:
```php
<?php
// Declarar una variable simple
$nombre = "Juan";

// Declarar una variable numérica
$edad = 25;

// Declarar una variable de punto flotante
$altura = 1.75;

// Declarar una variable booleana
$es_estudiante = true;

// Declarar una variable de matriz (array)
$colores = array("rojo", "verde", "azul");

// Declarar una variable nula
$nulo = null;
?>
```
Y para imprimir una variable se hace con echo:
```php
<?php
$nombre = "Mario";
echo $nombre;
?>
```
Si queremos cargar esto en el navegador, usaremos apache o algo similar:
![[Pasted image 20231216163650.png]]
Y lo podremos visualizar desde el navegador:
![[Pasted image 20231216163703.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
