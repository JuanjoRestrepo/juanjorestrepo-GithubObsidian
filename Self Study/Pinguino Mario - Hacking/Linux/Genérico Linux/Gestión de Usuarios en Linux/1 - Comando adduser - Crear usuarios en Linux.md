---
title: "1 - Comando adduser - Crear usuarios en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para crear un usuario, utilizamos el siguiente comando:
```
adduser pepe
```
![[Pasted image 20231119172220.png]]
Y vemos que el usuario se ha creado correctamente:
![[Pasted image 20231119172246.png]]
Y con el comando su pepe podemos convertirnos en dicho usuario:
![[Pasted image 20231119172528.png]]
Y también podemos visualizar el fichero /etc/passwd para comprobar la existencia de este usuario:
![[Pasted image 20231119173430.png]]
### ELIMINAR UN USUARIO EN LINUX
Para eliminar un usuario, usamos el comando deluser de la siguiente forma:
```
sudo pkill -9 -u pepe # Detenemos los procesos que esté usando el usuario.
deluser --remove-home pepe
```
![[Pasted image 20231119173932.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
