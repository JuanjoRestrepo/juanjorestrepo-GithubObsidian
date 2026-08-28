---
title: "Librería Netifaces"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La biblioteca `netifaces` en Python proporciona una interfaz para acceder a la información de red del sistema operativo, como direcciones IP, máscaras de subred, puertas de enlace y otras propiedades de las interfaces de red. Aquí tienes algunos ejemplos básicos de uso de `netifaces`:

Obtener una lista de todas las interfaces de red disponibles:

```python
import netifaces

interfaces = netifaces.interfaces()
print(interfaces)
```
Y este sería el resultado:
![[Pasted image 20230617103232.png]]
## Obtener la dirección IP de una interfaz:

```python
import netifaces

interfaces = netifaces.interfaces()

print(netifaces.ifaddresses(interfaces[4])) # Ponemos 4 para acceder a la interfaz tun0 que está en posición 4 dentro de la lista.
```
Y este sería el resultado:
![[Pasted image 20230617104204.png]]
Por lo que teniendo todo esto, ya podemos acceder al valor de IP y guardarlo en una variable:
```python
import netifaces

interfaces = netifaces.interfaces()

tun0 = netifaces.ifaddresses(interfaces[4])

ip_address = tun0[2][0]['addr']
print(ip_address)
```
Y dentro de la variable ip_address ya tenemos guardada la IP:
![[Pasted image 20230617104342.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
