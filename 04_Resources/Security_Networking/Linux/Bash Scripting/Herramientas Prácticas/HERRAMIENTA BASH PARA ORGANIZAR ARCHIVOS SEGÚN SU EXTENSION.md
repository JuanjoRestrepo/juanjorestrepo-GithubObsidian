---
title: "HERRAMIENTA BASH PARA ORGANIZAR ARCHIVOS SEGÚN SU EXTENSION"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Vamos a crear un script que ordene archivos de forma automática en función de la extensión que tengan:
```bash
#!/bin/bash

# Crear las carpetas si no existen
mkdir -p imagenes videos documentos

# Iterar sobre cada archivo en el directorio actual
for archivo in *
do
  # Obtener el nombre base del archivo sin la ruta
  nombre_base=$(basename "$archivo")

  # Obtener la extensión del archivo usando awk
  extension=$(echo "$nombre_base" | awk -F '.' '{print $NF}')

  # Mover el archivo a la carpeta correspondiente según su extensión
  case "$extension" in
    jpg|png)
      mv "$archivo" imagenes/
      echo "Movido $archivo a la carpeta imagenes"
      ;;
    mp4|mkv)
      mv "$archivo" videos/
      echo "Movido $archivo a la carpeta videos"
      ;;
    txt|doc)
      mv "$archivo" documentos/
      echo "Movido $archivo a la carpeta documentos"
      ;;
    *)
      echo "Archivo $archivo no se movió, extensión desconocida: $extension"
      ;;
  esac
done
```
También podríamos comprimir todas estas carpetas y después enviar dicho archivo comprimido a un servidor ftp:
```bash
#!/bin/bash

# Crear las carpetas si no existen
mkdir -p imagenes videos documentos

# Iterar sobre cada archivo en el directorio actual
for archivo in *
do
  # Obtener el nombre base del archivo sin la ruta
  nombre_base=$(basename "$archivo")

  # Obtener la extensión del archivo usando awk
  extension=$(echo "$nombre_base" | awk -F '.' '{print $NF}')

  # Mover el archivo a la carpeta correspondiente según su extensión
  case "$extension" in
    jpg|png)
      mv "$archivo" imagenes/
      echo "Movido $archivo a la carpeta imagenes"
      ;;
    mp4|mkv)
      mv "$archivo" videos/
      echo "Movido $archivo a la carpeta videos"
      ;;
    pdf|docx)
      mv "$archivo" documentos/
      echo "Movido $archivo a la carpeta documentos"
      ;;
    *)
      echo "Archivo $archivo no se movió, extensión desconocida: $extension"
      ;;
  esac
done

# Comprimir archivos
zip -r copia_seguridad.zip imagenes/ videos/ documentos/

# Detalles de conexión FTP
servidor='192.168.0.25'
usuario='mario-server'
clave='password123'

ruta_archivo_local=copia_seguridad.zip
archivo_remoto="/home/mario-server/copia_seguridad.zip"

# Subir archivo mediante curl
if curl -u "$usuario:$clave" -T "$ruta_archivo_local" "ftp://$servidor/$archivo_remoto"; then
  echo "Archivo subido exitosamente al servidor FTP."
  # Limpiar archivo zip local después de la subida
  rm "$ruta_archivo_local"
else
  echo "Error al subir el archivo al servidor FTP."
fi
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
