---
title: "MÁQUINA BÚSQUEDA"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vemos los puertos 80 y 22 abiertos:
![[Pasted image 20230802192141.png]]
Si abrimos el navegador, vemos que se aplica virtual hosting:
![[Pasted image 20230802192242.png]]
Lo cambiamos en el /etc/hosts:
![[Pasted image 20230802192316.png]]
Y accedemos a la web:
![[Pasted image 20230802192343.png]]
Miramos esta versión vulnerable de searcher:
![[Pasted image 20230802192732.png]]
Y en github encontramos un repositorio para explotar una vulnerabilidad:
```python
https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection
```
![[Pasted image 20230802192755.png]]
Ejecutamos el exploit poniendo la URL y nuestra IP de máquina atacante:
![[Pasted image 20230802192843.png]]
Y si estamos escuchando con netcat por el puerto 9001, que estará por defecto escuchando porque ya viene configurado en el script, ya estaremos dentro:
![[Pasted image 20230802192859.png]]
Si miramos el repositorio del git, vemos un archivo llamado config con unas credenciales:
![[Pasted image 20230802200228.png]]
Probamos estas credenciales para ejecutar el comando sudo -l y vemos que funciona:
```bash
jh1usoih2bkjaspwe92
```
![[Pasted image 20230802200317.png]]
Vemos que podemos insertar un comando al ejecutar este script, además de mostrarnos que podemos ejecutar cualquiera de los tres comandos con docker; y confirmamos con el comando hostname -I, viendo que tenemos varias interfaces de red que pertenecen posiblemente a contenedores de docker:
![[Pasted image 20230802200600.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
