---
title: "4 - Bucle FOR"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Un bucle se haría de esta fortma:
```php
<?php
for ($i = 0; $i < 5; $i++) {
    echo "Iteración $i <br>";
}
?>
```
![[Pasted image 20231216164435.png]]
### OTRO EJEMPLO
```php
<?php
for ($i = 1; $i <= 10; $i++) {
    echo $i . "<br>";
}
?>
```
En este ejemplo:

- La variable `$i` se inicializa en 1.
- La condición es `$i` debe ser menor o igual a 10.
- Después de cada iteración, incrementamos el valor de `$i` en 1 usando `$i++`.
![[Pasted image 20231216164546.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
