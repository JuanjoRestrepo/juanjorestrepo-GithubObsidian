---
title: "SMBclient"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Smbclient es un cliente de línea de comandos para el protocolo de intercambio de archivos de red Server Message Block (SMB). Este protocolo se utiliza comúnmente para compartir archivos e impresoras entre dispositivos en una red local.

Smbclient permite a los usuarios conectarse a servidores SMB y acceder a recursos compartidos como si estuvieran en una unidad local de su computadora. Con smbclient, los usuarios pueden explorar recursos compartidos, descargar y cargar archivos, crear y eliminar directorios, y realizar otras operaciones de archivos a través de la red.

Smbclient es una herramienta muy útil para los administradores de redes y los usuarios avanzados que necesitan trabajar con archivos y recursos compartidos en una red de Windows. También es compatible con sistemas operativos basados en Unix y Linux.
## EJECUTAR COMANDOS CON SMBCLIENT
Por ejemplo vamos a suponer que nos encontramos con estos recursos compartidos:
![[Pasted image 20230213104857.png]]
Pues con smbclient podemos acceder dentro de un recurso compartido con las credenciales correspondientes:
![[Pasted image 20230213105508.png]]
## LISTAR RECURSOS COMPARTIDOS CON UNA NULL SESSION CON SMBCLIENT
Podemos listar los recursos compartidos sin proporcionar credenciales haciendo uso de una null session:
![[Pasted image 20230420110349.png]]
## CONECTARNOS RECURSO COMPARTIDO SMB SIN CREDENCIALES
Podríamos hacerlo simplemente especificando el nombre del recurso compartido al que nos queramos conectar:
![[Pasted image 20230420110733.png]]
También podemos subir archivos con el comando put, por ejemplo voy a subir un documento txt:
![[Pasted image 20230420110901.png]]
Si lo quisiera descargar utilizaría el comando get:
![[Pasted image 20230420111148.png]]
Puede ser muy útil acceder con rpclient al objetivo para obtener más información del sistema. [[Rpcclient y Enum4linux]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
