---
title: "Diccionarios en Bash"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

También podemos crear un diccionario en bash con su clave-valor, de la siguiente forma:
```bash
#!/bin/bash

# Declarar un diccionario
declare -A diccionario

# Agregar elementos al diccionario
diccionario["clave1"]="valor1"
diccionario["clave2"]="valor2"
diccionario["clave3"]="valor3"

# Acceder a un valor usando la clave
echo "El valor de clave2 es: ${diccionario["clave2"]}"
```
Y ahora si imprimimos esto, obtendremos el siguiente mensaje por pantalla:
![[Pasted image 20230528212611.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
