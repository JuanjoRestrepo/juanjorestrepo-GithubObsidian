---
title: "3 - Subir Imágenes a Dockerhub o Guardarlas en Local"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Debemos ejecutar estos 3 comandos:
```bash
docker commit 33268dd332ef laboratorio2
docker login
docker tag laboratorio3 maalfer/laboratorio3:latest
docker push maalfer/laboratorio3:latest
```
Y lo tenemos:
![[Pasted image 20240320175435.png]]
Si queremos exportar una imagen en local, utilizaremos docker save y docker load. Por ejemplo, vamos a exportar la imagen upload:
```bash
docker save -o upload.tar upload:latest
```
![[Pasted image 20240327133655.png]]
Ahora si queremos importar esta imagen, utilizamos el comando docker load -i:
```bash
docker load -i upload.tar
```
![[Pasted image 20240327133739.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
