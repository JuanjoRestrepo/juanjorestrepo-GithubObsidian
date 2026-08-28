---
title: "TCPdump - Interceptar Tráfico de Red (Sniffing)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

`tcpdump` es una poderosa herramienta de línea de comandos que permite a los usuarios capturar y analizar el tráfico de red en sistemas basados en Unix. 

---------------------------
### Capturar todo el tráfico en una interfaz de red:
Para capturar el tráfico que ocurre en una interfaz de red, ejecutamos el siguiente comando:
```bash
tcpdump -i eth0
```
![[Pasted image 20231224230723.png]]
### Filtrar el tráfico por protocolo:
Indicamos que capture sólo el tráfico de un determinado protocolo de la siguiente forma:
```bash
tcpdump -i eth0 icmp
```
Nos hacemos un ping a nosotros mismos desde otro equipo y habremos capturado el tráfico del protocolo ICMP:
![[Pasted image 20231224231141.png]]

### Guardar la salida en un archivo:
Guardamos el tráfico registrado de la siguiente forma:
```bash
tcpdump -i eth0 -w trafico.pcap
```
![[Pasted image 20231224231317.png]]
### Leer un archivo de captura:
Para leer el contenido de un archivo pcap lo hacemos de la siguiente forma:
```bash
tcpdump -r trafico.pcap
```
![[Pasted image 20231224231410.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
