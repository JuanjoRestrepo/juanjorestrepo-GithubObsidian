---
title: "MÁQUINA GRILLO"
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
![[Pasted image 20240428233253.png]]
Esto corre por el puerto 80:
![[Pasted image 20240428233306.png]]
Viendo el código fuente vemos el usuario melanie:
![[Pasted image 20240428233321.png]]
Por lo que hacemos fuerza bruta al puerto 22 con hydra:
```bash
melanie:trustno1
```
![[Pasted image 20240501131143.png]]
Estamos dentro:
![[Pasted image 20240501131125.png]]
Y vemos un archivo que genera claves id_rsa:
![[Pasted image 20240501125322.png]]
Generamos una clave ssh:
![[Pasted image 20240501125417.png]]
Y esta clave pública generada con puttygen la podemos exportar:
```bash
sudo /usr/bin/puttygen id_rsa.pub -O public-openssh -o /root/.ssh/authorized_keys
```
![[Pasted image 20240501125631.png]]
Y ahora desde esta propia máquina podemos acceder como root por ssh sin proporcionar contraseña:
![[Pasted image 20240501125734.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
