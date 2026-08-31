---
title: "1 - Reglas Tabla Filter"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Con el comando iptables -L veremos todas las reglas de la tabla filter:
```bash
iptables -L
```
![[Pasted image 20240829190251.png]]
Por ejemplo si queremos denegar el tráfico ICMP de la tabla filter, lo hacemos de la siguiente forma:
```bash
iptables -t filter -A INPUT -p icmp -j DROP
```
Y ahora veremos la nueva regla creada en la tabla filter denegando el tráfico icmp:
![[Pasted image 20240829191151.png]]
Podemos borrar esta regla, primero ejecutaremos el comando `iptables -L -v --line-numbers` y después eliminamos la línea correspondiente con el comando `iptables -D INPUT 1` 
![[Pasted image 20240829192855.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
