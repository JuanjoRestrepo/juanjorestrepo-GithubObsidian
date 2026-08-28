---
title: "MAQUINA NAGINI"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el reconocimiento con nmap:
![[Pasted image 20231014110710.png]]
Si abrimos la página en el navegador, nos encontramos con esto:
![[Pasted image 20231014110741.png]]
Hacemos fuzzing de directorios web y nos encontramos con un note.txt y un directorio de joomla:
![[Pasted image 20231014110838.png]]
Aquí vemos el directorio /joomla:
![[Pasted image 20231014111655.png]]
Y esto es el contenido del fichero note.txt donde tenemos un nuevo dominio y una mención de que se usará HTTP3:
![[Pasted image 20231014110904.png]]
Por lo que actualizamos el /etc/hosts con este nuevo dominio que hemos encontrado:
![[Pasted image 20231014113348.png]]
Pero si hacemos un curl con http3 vemos que no funciona porque tenemos que habilitarlo en el sistema:
![[Pasted image 20231014111150.png]]
Pero dentro de este repositorio de github podemos instalarlo:
https://github.com/cloudflare/quiche
Siguiendo las siguientes instrucciones, ya que esto está hecho en rust, y para ello se usa cargo porque sirve para construir paquetes que estén hecho en el lenguaje rust:
![[Pasted image 20231014112750.png]]
```bash
git clone --recursive https://github.com/cloudflare/quiche
apt install cargo
apt install cmake
cargo build --examples
cd quiche && cargo test
```
![[Pasted image 20231014112915.png]]
Nos ubicamos en la siguiente ruta:
![[Pasted image 20231014113216.png]]
Y una vez ejecutado todo lo anterior, tendremos que ejecutar la herramienta http3-client, aunque en caso de error, deberemos de usar el firefox nightly y habilitar http3 desde ahí, por lo que instalamos el firefox:
![[Pasted image 20231014114614.png]]
Y ahora sin ser root ejecutamos el ./firefox y ya lo tenemos abierto:
![[Pasted image 20231014114730.png]]
Donde debemos de escribir lo siguiente y asegurarnos que http3 está habilitado:
![[Pasted image 20231014114447.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
