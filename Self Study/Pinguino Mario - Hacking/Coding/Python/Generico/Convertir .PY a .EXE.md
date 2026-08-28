---
title: "Convertir .PY a .EXE"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

### **PASO Nº 1 - Instalar pyinstaller**

### PASO Nº 2 - Ubicar la terminal en la misma ubicación que el archivo py y ejecutar este comando: pyinstaller --clean --onefile --windowed archivo_python.py

### PASO Nº 3 - Si el archivo tiene alguna imagen, ponerla en la misma ubicación que el archivo .exe

# CONVERTIR .PY → .BAT

Lo primero será tener ubicado nuestro script de Python y un bloc de notas:

![[Pasted image 20221217101452.png]]

A continuación, abrimos el bloc de notas y por un lado escribimos la ruta absoluta de donde tenemos el ejecutable de python en el sistema; y luego a continuación donde tenemos el script de Python que queramos convertir a .bat:

![[Pasted image 20221217101501.png]]

Y lo guardamos con extensión .bat:

![[Pasted image 20221217101510.png]]
Ahora ya tenemos el fichero .bat creado:
![[Pasted image 20221217101518.png]]
Hacemos doble clic en él y se habrá ejecutado el código de Python, que en este caso era un mkdir:
![[Pasted image 20221217101526.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
