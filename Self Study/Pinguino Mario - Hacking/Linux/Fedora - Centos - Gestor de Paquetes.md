---
title: "Fedora - Centos - Gestor de Paquetes"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

DNF (Dandified YUM) es la versión mejorada y actualizada de yum, utilizado para la gestión de paquetes en distribuciones de Linux basadas en RPM, como Fedora y CentOS.
## Gestión de Paquetes con DNF:

El gestor de paquetes DNF es la versión mejorada y actualizada de yum; y estos son sus usos más habituales:

`dnf upgrade` - Este comando actualiza todos los paquetes del sistema a las versiones más recientes disponibles en los repositorios configurados.

`dnf distro-sync` - Este comando sincroniza los paquetes instalados con la versión disponible en los repositorios, asegurando que todos los paquetes estén en las versiones compatibles con la distribución actual.

`dnf system-upgrade` - Este comando se utiliza para actualizar el sistema operativo a una nueva versión mayor, después de descargar los paquetes necesarios con dnf system-upgrade download --releasever=<versión>.

`dnf remove` - Este comando elimina un paquete especificado del sistema, incluyendo sus archivos de configuración.

`dnf autoremove` - Este comando elimina paquetes y dependencias que ya no son necesarias en el sistema.

`dnf search` - Este comando busca paquetes en los repositorios configurados que coincidan con el término de búsqueda proporcionado.

`dnf repoquery` - Este comando permite realizar búsquedas avanzadas en los repositorios, proporcionando detalles específicos sobre los paquetes disponibles.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
