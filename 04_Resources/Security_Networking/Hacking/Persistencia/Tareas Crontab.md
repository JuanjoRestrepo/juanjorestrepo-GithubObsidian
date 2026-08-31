---
title: "Tareas Crontab"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Comprobamos los procesos del sistema con el siguiente comando:
```
ps -ead
```
Y vemos que el crontab se está ejecutando:
![[Pasted image 20230801104244.png]]
Pero perdemos la conexión al poco tiempo:
![[Pasted image 20230801105214.png]]
Por lo que si entramos otra vez y rápidamente creamos en crontab una tarea para que se cree un servidor http que aloje los archivos del directorio de la máquina víctima con python:
```bash
echo "* * * * * cd /home/student/ && python -m SimpleHTTPServer" > cron # Esto en caso de usar python 2.
```
![[Pasted image 20230801104952.png]]
Una vez fuera, si lanzamos un nmap vemos el puerto 8000 abierto:
![[Pasted image 20230801105339.png]]
Y podemos obtener una flag:
![[Pasted image 20230801105408.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
