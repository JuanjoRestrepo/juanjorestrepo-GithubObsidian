---
title: "5 - Estilos en React"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será importar el archivo styles.css dentro del main.tsx:
![[Pasted image 20240707235442.png]]
Y a su vez este styles.css se aplica sobre todo nuestro proyecto que está en index.html:
![[Pasted image 20240707235531.png]]
Por ejemplo, si creamos los siguientes estilos sobre el body, se aplicará a la web:
![[Pasted image 20240707235624.png]]
![[Pasted image 20240707235631.png]]
### ESTILOS CSS PARA UN COMPONENTE EXCLUSIVAMENTE
Podemos también conseguir que el estilo CSS sólo se aplique a un componente y no a todo el código, y eso lo hacemos creando un archivo CSS, por ejemplo llamado PrimerComponente.css, y ahí definimos los estilos:
![[Pasted image 20240707235943.png]]
Y a continuación dentro de PrimerComponente.tsx podremos importar este .css:
![[Pasted image 20240708000019.png]]
Y veremos que de esta otra forma hemos aplicado también los estilos:
![[Pasted image 20240708000037.png]]
También se puede crear un directorio llamado styles y ahí guardar todos los estilos:
![[Pasted image 20240708000259.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
