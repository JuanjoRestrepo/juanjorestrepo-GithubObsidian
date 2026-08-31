---
title: "Blackstone - Generar Informes Automáticos"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Clonamos el repositorio:
![[Pasted image 20240426092449.png]]
Y procedemos con la instalación:
![[Pasted image 20240426092558.png]]
Es posible que nos generar algún error, por lo que debemos de ejecutar manualmente el siguiente archivo para instalar XAMPP:
![[Pasted image 20240426095746.png]]
Ahora hacemos otra vez la instalación y ya accedemos con las credenciales blackstone:blackstone:
![[Pasted image 20240426100403.png]]
Ya estamos dentro:
![[Pasted image 20240426100444.png]]
Vamos a la parte de audited client y luego add client:
![[Pasted image 20240426100656.png]]
Y ahora si lo añadimos, ya tenemos el nuevo cliente:
![[Pasted image 20240426100849.png]]
Para crear un nuevo informe, vamos a la parte de reports y luego a Add report:
![[Pasted image 20240426100935.png]]
Y añadimos el nombre de la empresa:
![[Pasted image 20240426101113.png]]
En esta parte pondremos el host correspondiente:
![[Pasted image 20240426101411.png]]
Si le damos en manage vulnerabilities veremos la base de datos con las vulnerabilidades que podemos escoger:
![[Pasted image 20240426101606.png]]
Y vamos cargando las vulns y damos en add vulns:
![[Pasted image 20240426102015.png]]
Y ahora se nos habrán cargado en esta máquina:
![[Pasted image 20240426102031.png]]
Editamos alguna de ellas y vamos añadiendo imagen por imagen:
![[Pasted image 20240426103540.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
