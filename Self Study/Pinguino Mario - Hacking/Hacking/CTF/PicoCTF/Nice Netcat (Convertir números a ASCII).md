---
title: "Nice Netcat (Convertir números a ASCII)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Tenemos este reto donde nos dicen que escuchemos con netcat a una determinada dirección por el puerto 7449:
![[Pasted image 20230409213645.png]]
Por tanto nos podemos a la escucha de esta dirección e imprimimos la respuesta por pantalla, donde recibimos una serie de números:
![[Pasted image 20230409213726.png]]
Si consultamos en chatgpt como convertir una secuencia de números a ASCII podemos ver que nos genera un script de bash, donde solo tenemos que añadir los números obtenidos anteriormente a la variables numeros:
![[Pasted image 20230409213827.png]]
Creamos el script con dichas modificaciones:
![[Pasted image 20230409213857.png]]
Lo ejecutamos y ya tenemos la conversión hecha y la flag:
![[Pasted image 20230409213921.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
