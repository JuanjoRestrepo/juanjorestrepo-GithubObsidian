---
title: "0 -  Primeros Pasos con Powershell"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

### **Comandos Básicos**

- **`Get-Help`**: Muestra la ayuda de PowerShell. Por ejemplo, `Get-Help Get-Process` proporciona información sobre el comando `Get-Process`.
- **`Get-Process`**: Muestra una lista de procesos en ejecución.
- **`Get-Service`**: Muestra una lista de servicios en el sistema.
- **`Get-Command`**: Muestra todos los comandos disponibles.

### . **Navegar por el Sistema de Archivos**

- **`Get-Location`**: Muestra el directorio actual.
- **`Set-Location <ruta>`**: Cambia al directorio especificado.
- **`Get-ChildItem`**: Muestra archivos y carpetas en el directorio actual (similar a `ls` en Linux).

### **Manipulación de Archivos**

- **`New-Item -Path <ruta> -ItemType File -Name <nombre>`**: Crea un nuevo archivo.
- **`Remove-Item <ruta>`**: Elimina un archivo o carpeta.
- **`Copy-Item <ruta-origen> <ruta-destino>`**: Copia un archivo o carpeta.
### **Uso de Variables**

- **`$miVariable = "Hola, PowerShell!"`**: Asigna un valor a una variable.
- **`$miVariable`**: Muestra el contenido de la variable.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
