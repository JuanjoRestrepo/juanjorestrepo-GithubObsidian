---
title: "2 - Gestor de Paquetes YAY"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Yay es un ayudante de construcción de paquetes para Arch Linux que facilita la gestión de paquetes, incluyendo la instalación, actualización y eliminación de paquetes desde los repositorios oficiales de Arch y el Arch User Repository (AUR).

-----------------------------

Para instalar un paquete:
```bash
yay -S nombre_del_paquete
```
Para actualizar la base de datos de paquetes:
```bash
yay -Sy
```
Para actualizar todos los paquetes del sistema:
```bash
yay -Syu
```
Para eliminar un paquete:
```bash
yay -R nombre_del_paquete
```
Para buscar paquetes en los repositorios y AUR:
```bash
yay -Ss nombre_del_paquete
```
Limpiar la caché de los paquetes descargados:
```bash
yay -Sc
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
