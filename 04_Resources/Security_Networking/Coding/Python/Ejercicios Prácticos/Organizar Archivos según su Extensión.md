---
title: "Organizar Archivos según su Extensión"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```python
import os
import shutil

documentos_dir = 'documentos'
fotos_dir = 'fotos'
videos_dir = 'videos'
musica_dir = 'musica'

if not os.path.exists(documentos_dir):
    os.makedirs(documentos_dir)
if not os.path.exists(fotos_dir):
    os.makedirs(fotos_dir)
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)
if not os.path.exists(musica_dir):
    os.makedirs(musica_dir)

extensiones_documentos = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx')
extensiones_fotos = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
extensiones_videos = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
extensiones_musica = ('.mp3', '.wav', '.aac', '.flac', '.ogg')

archivos = []
for f in os.listdir():
    archivos.append(f)

def mover_archivo(archivo, destino):
    shutil.move(archivo, destino)

for archivo in archivos:
    if archivo.endswith(extensiones_documentos):
        mover_archivo(archivo, documentos_dir)
    elif archivo.endswith(extensiones_fotos):
        mover_archivo(archivo, fotos_dir)
    elif archivo.endswith(extensiones_videos):
        mover_archivo(archivo, videos_dir)
    elif archivo.endswith(extensiones_musica):
        mover_archivo(archivo, musica_dir)

print("Organización de archivos completada.")
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
