---
title: "HERRAMIENTA BASH PARA CREAR COPIA DE SEGURIDAD Y SUBIRLA A SERVIDOR SSH"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```bash
#!/bin/bash

# Nombre del archivo ZIP
zip_file="escritorio.zip"

# Usuario y servidor SSH
ssh_user="mario"
ssh_server="192.168.0.44"

# Ruta en el servidor SSH donde se copiará el archivo ZIP
remote_path="/home/mario/Escritorio/"

# Comprimir el escritorio en un archivo ZIP
zip -r "$zip_file" .

# Copiar el archivo ZIP al servidor SSH
scp "$zip_file" "$ssh_user@$ssh_server:$remote_path"

# Verificar el estado de la operación de copia
if [ $? -eq 0 ]; then
  echo "El archivo ZIP se ha copiado correctamente al servidor SSH."
else
  echo "Ha ocurrido un error al copiar el archivo ZIP al servidor SSH."
fi
 
rm "$zip_file"
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
