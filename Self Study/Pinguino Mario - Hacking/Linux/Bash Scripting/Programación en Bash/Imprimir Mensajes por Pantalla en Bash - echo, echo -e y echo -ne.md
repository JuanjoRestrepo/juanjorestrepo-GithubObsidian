---
title: "Imprimir Mensajes por Pantalla en Bash - echo, echo -e y echo -ne"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

**echo**
No interpreta secuencias de escape y no permite un control preciso sobre la salida.
```bash
echo "Hola, mundo"
```
**echo -e**
Permite interpretar secuencias de escape en el texto, como `\n` para nueva línea o `\t`
para tabulación. Puede ser útil cuando deseas formatear la salida de una manera específica. Aunque bash ya interpreta los saltos de línea de forma automática, pero esto es útil cuando usamos por ejemplo colores:
```bash
echo -e "Línea 1\nLínea 2"
```
**echo -n**
Suprime la impresión de la nueva línea al final del texto. Es útil cuando deseas imprimir en la misma línea o controlar de manera precisa dónde aparece la nueva línea:
```bash
echo -n "Esto se imprimirá sin nueva línea"
echo " y esto estará en la misma línea."
```
![[Pasted image 20231206104510.png]]
**echo -ne**
También podemos combinar parámetros, como echo -ne, que se utiliza para evitar imprimir la nueva línea al final del texto y para habilitar la interpretación de secuencias de escape:
```bash
echo -ne "Esto es un ejemplo sin nueva línea al final: \tFormato tabulado"
```
![[Pasted image 20231206104935.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
