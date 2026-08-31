---
title: "MAQUINA MINEFIELD"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Hacemos el escaneo con nmap:
![[Pasted image 20240119113924.png]]
Esto es lo que corre por el puerto 80:
![[Pasted image 20240119113956.png]]
Y hay una ruta llamada hotelcal:
![[Pasted image 20240119114412.png]]
Y dentro de hotelcal hay un panel de login:
![[Pasted image 20240119114437.png]]
En este panel, si probamos con admin:admin funciona:
![[Pasted image 20240119114507.png]]
Y vemos que existe una cuenta de administrador:
![[Pasted image 20240119114631.png]]
Si hacemos clic en delete e interceptamos la petición con burp suite, vemos que no se produce ningún tipo de validación, donde se genera un enlace que al ejecutarlo se borra la cuenta con id 1, que es la del administrador:
![[Pasted image 20240119114836.png]]
Nos creamos una cuenta:
![[Pasted image 20240119114948.png]]
La tenemos aquí:
![[Pasted image 20240119115000.png]]
Y vemos que al borrar esta cuenta, en burp suite vemos lo mismo de antes pero que se borra el admin_id=2:
![[Pasted image 20240119115114.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
