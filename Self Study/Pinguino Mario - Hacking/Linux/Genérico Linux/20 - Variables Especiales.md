---
title: "20 - Variables Especiales"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En Linux, las variables especiales como `$?`, `$#`, y `$@` son utilizadas en scripts de shell para obtener información sobre el resultado de comandos.

**$? (Variable de Estado):**
Esta variable almacena el estado de salida del último comando ejecutado. Un valor de 0 generalmente indica que el comando se ejecutó correctamente, mientras que un valor diferente de 0 indica un error o fallo en la ejecución del comando:
![[Pasted image 20231119175849.png]]
Y por ejemplo, si ejecutamos un comando correctamente, mostrará la salida 0:
![[Pasted image 20231119175917.png]]
**$# (Número de Argumentos):**
Representa la cantidad de argumentos que se pasaron al script. Es útil para determinar cuántos argumentos se proporcionaron al script. Por ejemplo, dentro de un script añadimos la variable:
![[Pasted image 20231119180135.png]]
Y ahora si le pasamos dos argumentos al script, veremos cómo nos muestra el número 2:
![[Pasted image 20231119180159.png]]
**$@ (Todos los Argumentos):**
Esta variable representa todos los argumentos proporcionados al script. Cada argumento es tratado como una palabra separada.
![[Pasted image 20231119180302.png]]
Y nos imprimirá los argumentos proporcionados:
![[Pasted image 20231119180321.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
