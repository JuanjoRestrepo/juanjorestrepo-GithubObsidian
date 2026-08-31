---
title: "2 - Imágenes en PHP"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para incluir imágenes en php, lo haríamos de la siguiente forma:
```php
<?php
$nombre = "Mario";
$imagen_url = "pinguino.jpg";  // Reemplaza con la ruta real de tu imagen

echo "<h1>Hola, $nombre!</h1>";
echo "<img src='$imagen_url' alt='Imagen de $nombre'>";
?>
```
Dejamos la imagen en el mismo directorio:
![[Pasted image 20231216164047.png]]
Y la visualizamos en el navegador:
![[Pasted image 20231216164101.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
