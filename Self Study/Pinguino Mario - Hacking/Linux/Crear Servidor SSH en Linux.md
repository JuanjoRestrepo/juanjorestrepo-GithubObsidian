---
title: "Crear Servidor SSH en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Instalamos openssh-server:
```bash
apt install openssh-server
```
![[Pasted image 20230930100523.png]]
Ahora con el siguiente comando comprobamos que el servicio esté corriendo:
```bash
systemctl status ssh
```
![[Pasted image 20230930100558.png]]
Y ahora podemos entrar vía SSH de forma automática [[Configuración SSH Automático]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
