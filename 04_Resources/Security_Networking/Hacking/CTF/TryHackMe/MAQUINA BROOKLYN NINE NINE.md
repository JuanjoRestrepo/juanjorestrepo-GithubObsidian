---
title: "MAQUINA BROOKLYN NINE NINE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo de nmap:
![[Pasted image 20230705123221.png]]
Lo primero será ver la página web que corre detrás del puerto 80, pero si hacemos fuzzing o cualquier otra comprobación, no encontramos nada:
![[Pasted image 20230705123030.png]]

Vemos que el puerto 21 tiene habilitado el acceso como anonymous, por lo que entramos y nos encontramos con un .txt:
![[Pasted image 20230705120437.png]]
Y este es el contenido del fichero, donde nos encontramos con un usuario llamado Jake:
![[Pasted image 20230705120509.png]]
Ahora con este usuario Jake vamos a hacer un ataque de fuerza bruta con hydra, donde vemos que nos encuentra la contraseña de este usuario:
```bash
jake:987654321
```
![[Pasted image 20230705121837.png]]
Entramos vía SSH:
![[Pasted image 20230705121942.png]]
Si hacemos un sudo -l podemos ver que podemos ejecutar como root el comando /usr/bin/less:
![[Pasted image 20230705122203.png]]
Por tanto ejecutamos el comando less sobre la flag de root y vemos su contenido:
```bash
sudo /usr/bin/less /root/root.txt
```
![[Pasted image 20230705122733.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
