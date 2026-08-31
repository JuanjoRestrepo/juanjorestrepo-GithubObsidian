---
title: "Ataques de transferencia de zona (AXFR)"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Los ataques de transferencia de zona, también conocidos como AXFR (siglas de "Authoritative eXtensible File Transfer Protocol") son un tipo de ataque dirigido a los servidores de nombres de dominio para obtener información sensible sobre los dominios de una organización.

----------------------------

Para esto usaremos el siguiente laboratorio:
```php
https://github.com/vulhub/vulhub/tree/master/dns/dns-zone-transfer
```
![[Pasted image 20230712155908.png]]
![[Pasted image 20230712160156.png]]
Abrimos el fichero named.conf.local y ponemos el nombre de transferencia de zona que queramos:
![[Pasted image 20230712160322.png]]
Montamos el laboratorio con docker-compose up -d:
![[Pasted image 20230712160859.png]]
Una vez desplegado, puedo hacer un ataque de transferencia de zona de tal forma que con el comando dig pueda conocer los subdominios existentes y más información:
```bash
dig axfr @127.0.0.0 pingucorp.local
```
![[Pasted image 20230712161015.png]]
#### OTRO EJEMPLO
Otro ejemplo de este ataque puede ocurrir cuando estamos ante un dominio y queremos obtener subdominios; de tal forma que podemos hacer lo siguiente:
[[MAQUINA HUNTER]]
```bash
dig axfr hunterzone.nyx @192.168.0.40
```
![[Pasted image 20231222112441.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
