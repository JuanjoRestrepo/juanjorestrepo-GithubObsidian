---
title: "Acceder id_rsa para iniciar sesión por SSH a la máquina"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Por tanto lo que podemos hacer es extraer la ssh e iniciar sesión para que se ejecute el script por parte de root y podamos recibir la conexión:
![[wrsfgwsergrsedghdrfg.png]]
![[dsfgadgasdfgsdfg.png]]
Nos copiamos esta clave pública a un fichero y la utilizaremos para iniciar sesión, pero primero le tenemos que dar el permiso 600 para poder utilizarla:
![[rtgaergedsgd.png]]
Iniciamos la sesión con esta id_rsa y ya estamos dentro por SSH:
![[regagetargsrtgas.png]]

----------------------------------------------------------

[[MAQUINA WALDO (Path traversal y Local File Inclusion LFI para obtener clave ssh privada id_rsa para entrar con ssh)]]

[[MAQUINA TRICK]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
